from version.local.local_version import get_local_version
from version.remote.remote_version import get_remote_version

def compare_version():
    print('compare')
    local_version = get_local_version()
    remote_version = get_remote_version()

    print('local_version:', local_version)
    print('remote_version:', remote_version)

    if not remote_version or not local_version:
        print("Verification de mise à jour impossible.")
        return False
    
    try:

        local_parts = tuple(map(int, local_version.split('.')))
        remote_parts = tuple(map(int, remote_version.split('.')))
        return remote_parts > local_parts
    except Exception as e:
        print('Error comparing version:', e)
        return False