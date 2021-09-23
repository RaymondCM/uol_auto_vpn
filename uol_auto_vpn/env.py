import json
import keyring

from . import root

env_file = root / "env.json"
keyring_service = "uol_auto_vpn"


def delete_env():
    try:
        env_file.unlink()
    except Exception as e:
        print(e)


def update_env(json_data):
    with env_file.open("w") as json_file:
        json.dump(json_data, json_file, indent=4)


def load_env():
    server = "https://remote.lincoln.ac.uk"
    username = None
    password = "keyring"

    # Get defaults if file exists or create default file
    if env_file.is_file():
        with env_file.open("r") as json_file:
            data = json.load(json_file)
            server = data["SERVER"]
            username = data["USERNAME"]
            password = data["PASSWORD"]
    else:
        update_env({"SERVER": server, "USERNAME": username, "PASSWORD": password})

    # Set username in keyring for first time if none
    if username is None and password == "keyring":
        temp = input("Please enter your University email: ")

        username = temp if '@' in temp else None
        if username is not None:
            try:
                keyring.delete_password(keyring_service, username)
            except Exception as e:
                pass
            update_env({"SERVER": server, "USERNAME": username, "PASSWORD": password})

    # Try to get password from keyring
    if username is not None and password == "keyring":
        password = keyring.get_password(keyring_service, username)
        if password is None:
            getter = input
            try:
                import getpass
                getter = getpass.getpass
            except ImportError:
                pass
            password = getter(f"Please enter your password for {username}: ")
            password = None if len(password) < 3 else password
            try:
                keyring.set_password("uol_auto_vpn", username, password)
            except Exception as e:
                pass

    return server, username, password
