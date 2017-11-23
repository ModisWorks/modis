import requests

VERSION = "0.4.0"


def get():
    """Compare the current version to the latest on GitHub.

    Returns:
        name (str): The name of the latest version
    """

    # Get version info from GitHub
    r = requests.get("https://api.github.com/repos/Infraxion/Modis/releases/latest").json()
    if "message" not in r or r["message"] == "Not Found":
        r = requests.get("https://api.github.com/repos/Infraxion/Modis/releases").json()[0]

    # Parse version info
    if "tag_name" in r:
        version_name = r["tag_name"]
        version_tag = version_name.split('.')
        return version_tag
    else:
        return []


def compare():
    """Compare the current version to the latest on GitHub.

    Returns:
        comparison (int): -1=behind, 0=latest, 1=ahead
    """
    current_version = VERSION.split('.')
    release_version = get()

    for vi in range(len(release_version)):
        if len(current_version) > vi:
            if current_version[vi] > release_version[vi]:
                return 1
            elif current_version[vi] < release_version[vi]:
                return -1
        elif release_version[vi] != "0":
            return -1

    return 0


def get_str():
    """
    Get the version comparison info.

    Returns:
        version_str (str): A friendly response detailing the current version
    """

    latest = get()
    state = compare()
    if state == -1:
        return "A new version of Modis is available (v{})".format(latest)
    elif state == 0:
        return "You are running the latest version of Modis (v{})".format(VERSION)
    elif state == 1:
        return "You are running a preview version of Modis (v{} pre-release)".format(VERSION)
