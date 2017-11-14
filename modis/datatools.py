"""Read and write json data."""

import json as _json
import os as _os
from collections import OrderedDict

import requests

_dir = _os.path.dirname(_os.path.realpath(__file__))
_datafile = "{}/../data.json".format(_dir)

version = "0.3"


def has_data() -> bool:
    """
    Checks whether or not a data.json file has been created

    Returns:
        exists (bool): True if a data file exists, False otherwise
    """

    return _os.path.exists(_datafile)


def get_data() -> dict:
    """
    Get the current data dict of Discord from the data.json file

    Returns:
        data (dict): Parsed data.json file
    """

    with open(_datafile, 'r') as file:
        return _json.load(file)


def write_data(data: dict):
    """
    Write the data to the data.json file

    Args:
        data (dict): The updated data dictionary for Modis
    """

    sorted_dict = sort_recursive(data)

    with open(_datafile, 'w') as file:
        _json.dump(sorted_dict, file, indent=2)


def sort_recursive(data: dict):
    """
    Recursively sorts all elements in a dictionary

    Args:
        data (dict): The dictionary to sort

    Returns:
        sorted_dict (OrderedDict): The sorted data dict
    """

    newdict = {}

    for i in data.items():
        if type(i[1]) is dict:
            newdict[i[0]] = sort_recursive(i[1])
        else:
            newdict[i[0]] = i[1]

    return OrderedDict(sorted(newdict.items(), key=lambda item: (compare_type(type(item[1])), item[0])))


def compare_type(t):
    """
    Gives the order of the type for the dictionary

    Args:
        t (type): The type to compare

    Returns:
        1 for (dict, OrderedDict), 0 otherwise
    """
    if t in [dict, OrderedDict]:
        return 1

    return 0


def compare_latest_version():
    """
    Compare the current version to the latest on GitHub

    Returns version (tuple): of form (int, string):
        -1: If the current version is behind the latest
         0: If the current version is the latest
         1: If the current version is ahead of the latest
    """

    latest_release = requests.get("https://api.github.com/repos/Infraxion/Modis/releases/latest").json()
    # For when there's only one release
    if "message" not in latest_release or latest_release["message"] == "Not Found":
        latest_release = requests.get("https://api.github.com/repos/Infraxion/Modis/releases").json()[0]

    release_version_name = ""
    release_version = []
    if "tag_name" in latest_release:
        release_version_name = latest_release["tag_name"]
        release_version = release_version_name.split('.')
    current_version = version.split('.')

    for vi in range(len(release_version)):
        if len(current_version) > vi:
            if current_version[vi] > release_version[vi]:
                return 1, release_version_name
            elif current_version[vi] < release_version[vi]:
                return -1, release_version_name
        else:
            return -1, release_version_name

    return 0, release_version_name


def log_compare_version(logger):
    """Logs the version comparison to the given logger"""
    state, latest_version = compare_latest_version()
    if state < 0:
        logger.info("A new version of Modis is available (v{})".format(latest_version))
    elif state == 0:
        logger.info("You are running the latest version of Modis (v{})".format(latest_version))
    else:
        logger.info("You are running a preview version of Modis (v{} pre-release)".format(latest_version))
