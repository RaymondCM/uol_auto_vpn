from __future__ import division, absolute_import, print_function

import os
import time

from uol_auto_vpn.driver import Browser, delete_driver
from uol_auto_vpn.env import load_env, reset_env


def cli():
    import argparse

    parser = argparse.ArgumentParser(description='Auto connect to UoL VPN')
    parser.add_argument('-r', '--reset', action='store_true',  default=False, help="Reset Application")

    args = parser.parse_args()

    if args.reset:
        reset_env()
        delete_driver()

    run_browser()


def run_browser():
    server, username, password = load_env()
    browser = Browser()
    driver = browser.open()

    try:
        driver.get(server)

        time.sleep(1)
        if username:
            driver.find_element_by_xpath('//*[@id="userNameInput"]').send_keys(username)
        if password:
            driver.find_element_by_xpath('//*[@id="passwordInput"]').send_keys(password)

        time.sleep(1)
        if username and password:
            driver.find_element_by_xpath("//*[@id='submitButton']").click()

        while browser.session_id:
            cookies = {v['name']: v['value'] for v in driver.get_cookies()}
            vpn_cookie = cookies.get("webvpn", None)
            if vpn_cookie:
                browser.driver.close()
                command = f"sudo openconnect --cookie={vpn_cookie} {server}"
                print(f"VNP cookie extracted running it with: \n\n{command}\n\nOpening Terminal\n")
                command_wrap = f"echo Running {command}; " \
                               f"echo ; " \
                               f"{command}; " \
                               f"echo Closing Terminal; " \
                               f"sleep 5"
                os.system(f"gnome-terminal -e 'bash -c \"{command_wrap}\"'")
                # from subprocess import call
                # command = ["sudo", "openconnnect", f"--cookie={vpn_cookie}", f"{server}"]
                # print(f"VNP cookie extracted running it with: \n\n{' '.join(command)}\n\nOpening Terminal\n\n")
                # call(command)
                break
            time.sleep(0.5)
    finally:
        driver.quit()


if __name__ == '__main__':
    cli()
