import requests
import zipfile
import os

def download_and_extract(url, headers, zip_path="develop.zip", extract_dir="temp_update"):
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    with open(zip_path, "wb") as f:
        f.write(response.content)
    print("download complete")

    with zipfile.ZipFile(zip_path, "r") as z:
        z.extractall(extract_dir)
    print("extraction complete")

    inner_folder = next(
        (f for f in os.listdir(extract_dir) if f.startswith("Ishak-devs-ERP")),
        None
    )
    return inner_folder