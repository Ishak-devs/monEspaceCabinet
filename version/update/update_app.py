from authozization.github.token import get_token_github
from .download_and_extract import download_and_extract
from .copy_new_version import copy_new_version
from version.update.update_local_version import update_local_version
import requests
from base64 import b64decode
import threading
import os


def update_app():

    def worker():
        token = get_token_github()
        if not token:
            return

        url = "https://api.github.com/repos/Ishak-devs/ERP/zipball/develop"
        headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json"
        }


        url_version = "https://api.github.com/repos/Ishak-devs/ERP/contents/version/version.txt?ref=develop"
        resp = requests.get(url_version, headers=headers)
        if resp.status_code == 200:
            data = resp.json()
            version_str = b64decode(data['content']).decode().strip()
            print(f"Local version updated to {version_str}")    
                
        inner_folder = download_and_extract(url, headers)
        if inner_folder:        

            copy_new_version(inner_folder)
            update_local_version(version_str)

            print(f"Local version mis à jour !")
        os._exit(0)


    threading.Thread(target=worker, daemon=True).start()