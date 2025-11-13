import requests

def compare_version_and_update():
    print('compare')

    remote_version = "https://github.com/Ishak-devs/ERP/releases/latest"
    response = requests.get(remote_version)
    latest_version = response.json()["tag_name"]
    print('remote_version:', remote_version)
    current_version = "https://api.github.com/repos/Ishak-devs/ERP/contents/version/version.txt?ref=develop"

    if latest_version > current_version:
        download_url = response.json()["assets"][0]["browser_download_url"]
        return True, download_url
    return False, None