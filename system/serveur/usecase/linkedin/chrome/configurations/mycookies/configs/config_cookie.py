import json
import os

from usecase.linkedin.chrome.configurations.mycookies.get_cookies import get_cookies


def config_cookie(driver):
    driver.get("https://www.linkedin.com")

    driver.add_cookie({
        "name": "lang",
        "value": "v=2&lang=fr-fr",
        "domain": ".linkedin.com",
        "path": "/",
    })



