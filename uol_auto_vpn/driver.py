import logging
import sys
from io import BytesIO
from pathlib import Path
from urllib.request import urlopen
from zipfile import ZipFile

from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from webdriver_manager.chrome import ChromeDriverManager

from uol_auto_vpn import _root

driver_folder = _root / "drivers"
driver_profile = driver_folder / "profile"
platform = {'linux': 'linux64', 'linux2': 'linux64', 'linux3': 'linux64', 'win32': 'win32', 'cygwin': 'win32',
            'darwin': 'mac64'}.get(sys.platform, 'linux64')
driver_profile.mkdir(parents=True, exist_ok=True)


def remove_tree(f: Path):
    if f.is_file():
        f.unlink()
    else:
        for child in f.iterdir():
            remove_tree(child)
        f.rmdir()


def get_driver() -> Path:
    return ChromeDriverManager(path=str(driver_folder), log_level=logging.NOTSET).install()


class Browser:
    def __init__(self, detach=False):
        self.opts = webdriver.ChromeOptions()
        self.opts.add_experimental_option("detach", detach)
        self.opts.add_argument(f"user-data-dir={driver_profile}")
        self.opts.add_argument("window-size=600x600")
        driver = get_driver()
        if driver is None:
            raise ValueError("Chrome Driver has not been installed on this machine")
        self.driver = webdriver.Chrome(executable_path=str(get_driver()), chrome_options=self.opts)
        self.url = self.driver.command_executor._url
        self.session_id = self.driver.session_id

    def open(self):
        opts = webdriver.ChromeOptions()
        opts.add_argument("--headless")
        opts.add_argument(f"user-data-dir={driver_profile}")
        opts.add_argument("window-size=600x600")
        driver = webdriver.Remote(command_executor=self.url, desired_capabilities=DesiredCapabilities.CHROME,
                                  options=opts)
        driver.set_window_size(600, 600)
        driver.close()
        driver.session_id = self.session_id
        return driver
