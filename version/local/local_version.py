import os
from treatment.path_ressources import ressources_path

LOCAL_VERSION_FILE = ressources_path("ressources/version.txt")

def get_local_version():
    if os.path.exists(LOCAL_VERSION_FILE):
        with open(LOCAL_VERSION_FILE, "r") as f:
            return f.read().strip()
    return "0.0"