from __future__ import division, absolute_import, print_function

import json
import os
import pathlib
import time
from threading import Event

from selenium import webdriver
from selenium.webdriver import DesiredCapabilities

data_set = Event()

ROOT = pathlib.Path(__file__).parent
SERVER = "https://remote.lincoln.ac.uk"
USERNAME = None
PASSWORD = None

if (ROOT / "env.json").is_file():
    with (ROOT / "env.json").open("r") as json_file:
        data = json.load(json_file)
        SERVER = data["SERVER"]
        USERNAME = data["USERNAME"]
        PASSWORD = data["PASSWORD"]


class Browser:
    def __init__(self, detach=False, driver_exe=None):
        self.opts = webdriver.ChromeOptions()
        self.opts.add_experimental_option("detach", detach)
        if driver_exe is None:
            driver_exe = (ROOT / "chromedriver-linux").resolve()
        self.driver = webdriver.Chrome(executable_path=str(driver_exe), chrome_options=self.opts)
        self.url = self.driver.command_executor._url
        self.session_id = self.driver.session_id


def run_browser():
    browser = Browser()

    opts = webdriver.ChromeOptions()
    opts.add_argument("--headless")
    opts.add_argument(f"user-data-dir={ROOT}")
    driver = webdriver.Remote(command_executor=browser.url, desired_capabilities=DesiredCapabilities.CHROME, options=opts)
    driver.close()
    driver.session_id = browser.session_id
    driver.get(SERVER)
    time.sleep(1)

    if USERNAME:
        driver.find_element_by_xpath('//*[@id="userNameInput"]').send_keys(USERNAME)
    if PASSWORD:
        driver.find_element_by_xpath('//*[@id="passwordInput"]').send_keys(PASSWORD)
    time.sleep(1)
    if USERNAME and PASSWORD:
        driver.find_element_by_xpath("//*[@id='submitButton']").click()

    while browser.session_id:
        cookies = {v['name']: v['value'] for v in driver.get_cookies()}
        vpn_cookie = cookies.get("webvpn", None)
        if vpn_cookie:
            browser.driver.close()
            command = f"sudo openconnect --cookie={vpn_cookie} {SERVER}"
            print(f"VNP cookie extracted running it with: \n\n{command}\n\nOpening Terminal\n")
            os.system(f"gnome-terminal -e 'bash -c \"{command}; echo \"Closing Terminal\";sleep 10\"'")
            break
        time.sleep(0.5)


if __name__ == '__main__':
    run_browser()
