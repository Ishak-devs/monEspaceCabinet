import json
import os


def config_cookie(driver, uid):
    driver.get("https://www.linkedin.com")

    driver.add_cookie({
        "name": "lang",
        "value": "v=2&lang=fr-fr",
        "domain": ".linkedin.com",
        "path": "/",
    })

    cookie_path = f"usecase/linkedin/cookies/cookie_{uid}.json"
    if os.path.exists(cookie_path):
        with open(cookie_path, "r") as f:
            li_at = json.load(f)
        driver.add_cookie(li_at)
        print ("Session restaurée via cookie.")

