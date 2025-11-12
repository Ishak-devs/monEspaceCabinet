import shutil
import os

def copy_new_version(inner_folder, extract_dir="temp_update", zip_path="develop.zip"):

    try:
        src = os.path.join(extract_dir, inner_folder)
        shutil.copytree(src, ".", dirs_exist_ok=True)
        print("file updated!")

        os.remove(zip_path)
        shutil.rmtree(extract_dir)
        print("Copie terminée")

    except Exception as e:
        print(f"Copie error: {e}")