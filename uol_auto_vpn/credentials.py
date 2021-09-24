import json
from collections import defaultdict
from pathlib import Path

__all__ = [
    "CredentialsException", "CredentialsServiceException", "CredentialsKeyException", "CredentialsValueException",
    "credentials_manager_from_str", "PlainTextCredentials", "KeyringCredentials", "registry", "_CredentialsManager"
]


class CredentialsException(Exception):
    """Default exception for CredentialsManager"""
    def __init__(self, message, *args):
        super().__init__(message, *args)


class CredentialsServiceException(CredentialsException):
    """Default exception for Service errors within CredentialsManager"""
    pass


class CredentialsKeyException(CredentialsException):
    """Default exception for Key errors within CredentialsManager"""
    pass


class CredentialsValueException(CredentialsException):
    """Default exception for Value errors within CredentialsManager"""
    pass


class _CredentialsManager:
    """Base class with get, set, delete functionality for credentials."""
    def __init__(self) -> None:
        self._name = self.__class__.__name__
        self._store = defaultdict(dict)

    def _check(self, service: str, key: str = None, value: str = None):
        # Check service exists, if it does check key exists, if it does check assigned values are equal
        if service is not None:
            if service not in self._store:
                raise CredentialsServiceException(f"Credentials service '{service}' does not exist.")
            if key is not None:
                if key not in self._store[service]:
                    raise CredentialsKeyException(f"Credentials key '{key}' does not exist.")
                if value is not None and self._store[service][key] != value:
                    raise CredentialsValueException(f"Credentials value '{value}' does not equal stored value.")

    def set(self, service: str, key: str, value: str) -> None:
        try:
            self._store[service][key] = value
        except Exception as e:
            raise CredentialsException(str(e))

    def __setitem__(self, service: str, _: str):
        raise CredentialsKeyException(
            f"Please pass key and service to __setitem__ operator [] i.e. {self._name}[service][key] = value"
        )

    def get(self, service: str, key: str) -> str:
        self._check(service, key=key)
        try:
            return self._store[service][key]
        except Exception as e:
            raise CredentialsException(str(e))

    def __getitem__(self, service: str):
        return _CredentialsManagerGetterSetterDeleterProxy(self, service)

    def delete(self, service: str, key: str) -> bool:
        """"""
        self._check(service, key=key)
        try:
            return self._store[service].pop(key, None) is not None
        except Exception as e:
            raise CredentialsException(str(e))

    def __repr__(self):
        raise CredentialsException(f"Cannot log {self._name}")

    def __len__(self):
        raise CredentialsException(f"Cannot expose {self._name} length")

    def contains(self, service, key):
        try:
            self.get(service, key)
        except CredentialsException:
            return False
        return True

    def test(self, fail_okay=False) -> bool:
        """Raises error if fail_okay=false and keyring isn't operational else returns is_operational boolean"""
        is_operational = False
        try:
            import uuid
            service, key, value = f"{self._name}-TestService-{str(uuid.uuid4())}", "testing", "functionality"

            def raise_on_fail(original, new, is_deleted):
                if original != new:
                    raise CredentialsValueException(f"Values are not equal in {self._name} tests")
                if not is_deleted:
                    raise CredentialsException(f"Could not delete entries in {self._name} tests")

            # Test functionality
            self.set(service, key, value)
            returned_value = self.get(service, key)
            deleted = self.delete(service, key)
            raise_on_fail(value, returned_value, deleted)

            # Test operators
            self[service][key] = value
            returned_value = self[service][key]
            deleted = self[service].__delitem__(key)
            raise_on_fail(value, returned_value, deleted)

            is_operational = True
        except IOError as e:
            if fail_okay:
                return is_operational
            raise CredentialsException(str(e))
        return is_operational


class _CredentialsManagerGetterSetterDeleterProxy:
    def __init__(self, credentials_manager: _CredentialsManager, service: str):
        self._credentials_manager = credentials_manager
        self._service = service

    def __getitem__(self, key: str):
        return self._credentials_manager.get(self._service, key)

    def __setitem__(self, key: str, value: str):
        self._credentials_manager.set(self._service, key, value)

    def __delitem__(self, key: str):
        return self._credentials_manager.delete(self._service, key)

    def __repr__(self):
        raise CredentialsException("Cannot log CredentialsManagerGetterSetterDeleterProxy")

    def __len__(self):
        raise CredentialsException("Cannot expose CredentialsManagerGetterSetterDeleterProxy")


class KeyringStore:
    def __init__(self, service):
        try:
            import keyring
            import keyring.errors as errors
            self._service = service
            self._keyring = keyring
            self._errors = errors
        except ImportError:
            raise CredentialsException("Cannot use Keyring as CredentialsManager it is not installed.")

    def __setitem__(self, key: str, value: str):
        self._keyring.set_password(self._service, key, value)

    def __getitem__(self, key: str):
        return self._keyring.get_password(self._service, key)

    def __repr__(self):
        raise CredentialsException("Cannot log Credentials")

    def __len__(self):
        raise CredentialsException("Cannot expose Credentials length")

    def __delitem__(self, key):
        self._keyring.delete_password(self._service, key)

    def pop(self, key, default=None):
        if key in self:
            ret = self[key]
            del self[key]
            return ret
        return default

    def __contains__(self, key):
        return self._keyring.get_password(self._service, key) is not None


class KeyringCredentials(_CredentialsManager):
    def __init__(self):
        super().__init__()
        self._store = {}

    def _create_missing_service(self, service):
        if service not in self._store:
            self._store[service] = KeyringStore(service)

    def set(self, service: str, key: str, value: str) -> None:
        self._create_missing_service(service)
        super().set(service, key, value)

    def get(self, service: str, key: str) -> str:
        self._create_missing_service(service)
        return super().get(service, key)

    def delete(self, service: str, key: str) -> bool:
        self._create_missing_service(service)
        return super().delete(service, key)


class PlainTextStore:
    def __init__(self, service, path):
        self._path = path
        self._service = service

    def _write_data(self, data):
        # Remove empty services
        data = {service: kv for service, kv in data.items() if bool(kv)}
        # Only write if data not empty otherwise remove file if exists
        if bool(data):
            with self._path.open("w") as json_file:
                json.dump(data, json_file, indent=4)
        elif self._path.is_file():
            self._path.unlink()

    def _read_file(self):
        if not self._path.is_file():
            return {}
        with self._path.open("r") as json_file:
            return json.load(json_file)

    def _get_file(self, key, missing_ok=False):
        data = self._read_file()
        if self._service not in data:
            raise CredentialsServiceException(f"Service '{self._service}' does not exist")
        if not missing_ok and key not in data[self._service]:
            raise CredentialsKeyException(f"Key '{key}' does not exist for self._service '{self._service}'")
        return data[self._service].get(key, None)

    def _set_file(self, key, value):
        data = self._read_file()
        if self._service not in data:
            data[self._service] = {}
        data[self._service][key] = value
        self._write_data(data)

    def _del_file(self, key, default=None):
        data = self._read_file()
        deleted_value = None
        if self._service in data:
            deleted_value = data[self._service].pop(key, default)
            self._write_data(data)
        return deleted_value

    def __setitem__(self, key: str, value: str):
        self._set_file(key, value)

    def __getitem__(self, key: str):
        return self._get_file(key)

    def __delitem__(self, key: str):
        self._del_file(key)

    def __repr__(self):
        raise CredentialsException("Cannot log Credentials")

    def __len__(self):
        raise CredentialsException("Cannot expose Credentials length")

    def pop(self, key, default=None):
        if key in self:
            ret = self[key]
            del self[key]
            return ret
        return default

    def __contains__(self, key):
        return self._get_file(key, missing_ok=True) is not None


class PlainTextCredentials(_CredentialsManager):
    """Plain text credentials manager that stores in the default directory (same as this file)"""
    def __init__(self):
        super().__init__()
        self._store = {}
        self.path = Path(__file__).parent / f".{Path(__file__).name}.{self._name}"

    def _create_missing_service(self, service):
        if service not in self._store:
            self._store[service] = PlainTextStore(service, self.path)

    def set(self, service: str, key: str, value: str) -> None:
        self._create_missing_service(service)
        super().set(service, key, value)

    def get(self, service: str, key: str) -> str:
        self._create_missing_service(service)
        return super().get(service, key)

    def delete(self, service: str, key: str) -> bool:
        self._create_missing_service(service)
        return super().delete(service, key)


def credentials_manager_from_str(manager: str):
    """Return a credentials manager from string, if kind doesn't exist on the system raise a CredentialsException"""
    if manager not in registry:
        raise CredentialsException(f"No '{manager}' manager exists. Select from: {', '.join(registry.keys())}.")
    return registry[manager]()


'''Store of {Name: CredentialManager} of supported credential managers'''
registry = {x().__class__.__name__.lower().replace('credentials', ''): x for x in [
    KeyringCredentials, PlainTextCredentials
]}
