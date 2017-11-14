"""Read and write json data."""

import json as _json
import os as _os
from collections import OrderedDict

_dir = _os.path.dirname(_os.path.realpath(__file__))
_datafile = "{}/../data.json".format(_dir)

version = "0.3 pre-release"


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
