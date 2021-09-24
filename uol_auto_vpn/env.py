import json
import re
from typing import Callable

from uol_auto_vpn.credentials import registry, _CredentialsManager
from uol_auto_vpn import _config, _service_name


def _email_validation(email):
    if re.match(r"^[^@]+@[^@]+\.[^@]+$", email) is not None:
        return True
    print(f"'{email}' is not a valid email!")
    return False


def _web_address_validation(address):
    if re.match(r"(https?:\/\/)?(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)",
                address) is not None:
        return True
    print(f"'{address}' is not a valid web address!")
    return False


def _password_validation(password):
    if len(password) > 3:
        return True
    print(f"Password must be greater than 3 characters")
    return False


def _default_input(msg, valid_options=None, default=None, validator=None, private=None):
    options = ''
    if default:
        options = f" <[{default}]>"
    if valid_options:
        valid_options = [str(v) for v in valid_options]
        options = f" <{', '.join([f'[{v}]' if v == default else v for v in valid_options])}>"

    get_input = input
    if private is None and any([t in msg.lower() for t in ['pass', 'password', 'confidential', 'secret']]):
        private = True  # if private is none i.e. try to detect if input should be protected

    if private:
        import getpass
        get_input = getpass.getpass

    selection = None
    while selection is None:
        response = get_input(f"{msg}{options}:") or default

        validation = True
        if isinstance(validator, Callable):
            validation = validator(response)

        if validation:
            if valid_options and response in valid_options:
                selection = response
                break
            if not valid_options or response == default:
                selection = response
                break

        print(f"Please enter a valid selection" + "{}".format((' not \'' + response + '\'') if not private else ''))

    return selection


def _setup():
    if not _config.exists():
        options = {str(i + 1): k for i, k in enumerate(registry.keys())}
        no_selection_value = "none"  # something that isn't in the registry keys
        options[str(len(options.keys()) + 1)] = no_selection_value
        options_str = '\n\t'.join([f"{k}) {v}" for k, v in options.items()])
        print(
            "This is the first time UoL auto VPN has been ran!"
            "\nHow would you like your credentials to be remembered? You can reset this at anytime with the -r flag."
            f"\n\n\t{options_str}\n"
        )

        credentials_manager = None
        while not options.get(credentials_manager, None) == no_selection_value:
            credentials_manager = _default_input("Please enter your selection", options.keys(), default=str(1))

            # Allow no credentials manager
            if options.get(credentials_manager, None) == no_selection_value:
                break

            # Test credentials manager is supported
            if registry[options[credentials_manager]]().test(fail_okay=True):
                credentials_manager = options[credentials_manager]
                break

            print("Selection is not supported on your system.")

        with _config.open("w") as json_file:
            json.dump({"credentials_manager": credentials_manager}, json_file, indent=4)

    with _config.open("r") as json_file:
        credentials_manager = json.load(json_file)["credentials_manager"]

    return credentials_manager


# Some defaults and validation schemas
_defaults = {'server': "https://remote.lincoln.ac.uk"}
_validators = {'server': _web_address_validation, 'username': _email_validation, 'password': _password_validation}
_options = {'server': None, 'username': None, 'password': None}


def reset_env():
    # Perform various cleanup operations
    # App config
    if _config.exists():
        _config.unlink()
    # Credential manager config
    from uol_auto_vpn.credentials import PlainTextCredentials
    if PlainTextCredentials().test(fail_okay=True):
        _plain_text_file = PlainTextCredentials().path
        if _plain_text_file.exists():
            _plain_text_file.unlink()
    from uol_auto_vpn.credentials import KeyringCredentials
    if KeyringCredentials().test(fail_okay=True):
        for opt in _options:
            if KeyringCredentials().contains(_service_name, opt):
                KeyringCredentials().delete(_service_name, opt)


def load_env():
    credentials_manager_str = _setup()
    credentials_manager = registry.get(credentials_manager_str, None)
    options = _options

    # Attempt to read
    if credentials_manager is not None:
        credentials_manager = credentials_manager()
        for option in options.keys():
            if credentials_manager.contains(_service_name, option):
                options[option] = credentials_manager.get(_service_name, option)

    # Fill in null values from terminal
    for option in options.keys():
        if options[option] is None:
            options[option] = _default_input(
                f"Please enter {option}",
                valid_options=None,
                default=_defaults.get(option, None),
                validator=_validators.get(option, None)
            )
            if credentials_manager is not None:
                credentials_manager.set(_service_name, option, options[option])

    return options["server"], options["username"], options["password"]
