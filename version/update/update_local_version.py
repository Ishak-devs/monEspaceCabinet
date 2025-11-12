import os
from version.local.local_version import LOCAL_VERSION_FILE

def update_local_version(new_version: str):
    version_path = LOCAL_VERSION_FILE

    os.makedirs(os.path.dirname(version_path), exist_ok=True)
    with open(version_path, "w") as f:
        f.write(new_version)

        