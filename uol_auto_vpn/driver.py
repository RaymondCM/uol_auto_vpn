import sys
from io import BytesIO
from pathlib import Path
from urllib.request import urlopen
from zipfile import ZipFile

from selenium import webdriver
from selenium.webdriver import DesiredCapabilities

from . import root

driver_folder = root / "drivers"
driver_profile = driver_folder / "profile"
driver_file = driver_folder / "chromedriver"
driver_profile.mkdir(parents=True, exist_ok=True)


def download_driver(driver_url, destination=driver_folder) -> Path:
    resp = urlopen(driver_url)
    zipfile = ZipFile(BytesIO(resp.read()))
    zipfile.extractall(destination)
    if driver_file.is_file():
        driver_file.chmod(0o755)
    return driver_file if driver_file.is_file() else None


def get_driver() -> Path:
    if driver_file.is_file():
        return driver_file
    platform = {'linux': 'linux64', 'linux2': 'linux64', 'linux3': 'linux64', 'win32': 'win32', 'cygwin': 'win32',
                'darwin': 'mac64'}.get(sys.platform, 'linux64')
    return download_driver(f"https://chromedriver.storage.googleapis.com/93.0.4577.63/chromedriver_{platform}.zip")


class Browser:
    def __init__(self, detach=False):
        self.opts = webdriver.ChromeOptions()
        self.opts.add_experimental_option("detach", detach)
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
        driver = webdriver.Remote(command_executor=self.url, desired_capabilities=DesiredCapabilities.CHROME,
                                  options=opts)
        driver.close()
        driver.session_id = self.session_id
        return driver
