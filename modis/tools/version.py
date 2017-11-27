"""
This tool checks GitHub for the latest version of Modis and can produce the name
of the current official version and the difference between that version and the
version currently being used.
"""

import logging
import requests

logger = logging.getLogger(__name__)

VERSION = "0.4.0"


def get():
    """Compare the current version to the latest on GitHub.

    Returns:
        version (list): The latest live version numbers
    """

    logger.debug("Checking version...")

    # Get version info from GitHub
    try:
        r = requests.get("https://api.github.com/repos/Infraxion/Modis/releases/latest").json()
        if "message" not in r or r["message"] == "Not Found":
            r = requests.get("https://api.github.com/repos/Infraxion/Modis/releases").json()[0]
    except requests.ConnectionError:
        logger.warning("Could not connect to GitHub for version info")
        return []

    # Parse version info
    if "tag_name" in r:
        version_name = r["tag_name"]
        version_tag = version_name.split('.')
        return version_tag
    else:
        return []


def compare(release_version):
    """Compare the current version to the latest on GitHub.

    Args:
        release_version (list): The latest live version numbers

    Returns:
        comparison (int): -1=behind, 0=latest, 1=ahead
    """

    current_version = VERSION.split('.')

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
    state = compare(latest)
    if state == -1:
        return "A new version of Modis is available (v{})".format(latest)
    elif state == 0:
        return "You are running the latest version of Modis (v{})".format(VERSION)
    elif state == 1:
        return "You are running a preview version of Modis (v{} pre-release)".format(VERSION)
