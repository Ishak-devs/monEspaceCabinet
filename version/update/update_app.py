import shutil
import sys
import subprocess


def update_app(download_url, GITHUB_TOKEN=None):
    from version.download.downloader import download_new_version
    new_exe = download_new_version(download_url)

    if new_exe:
        current_exe = sys.executable       

        shutil.move(new_exe, current_exe)

        subprocess.Popen([current_exe])
        sys.exit(0)