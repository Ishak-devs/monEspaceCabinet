import json
import os

from usecase.linkedin.chrome.mycookies.configs.config_cookie import config_cookie


def get_cookies(driver, uid):

    config_cookie(driver)

    cookie_path = f"usecase/linkedin/cookies/cookie_{uid}.json"
    if os.path.exists(cookie_path):
        with open(cookie_path, "r") as f:
            li_at = json.load(f)
        driver.add_cookie(li_at)
        print ("Session restaurée via cookie.")