import logging

import json

import os
from collections import OrderedDict

logger = logging.getLogger(__name__)

_dir = os.getcwd()
datafile = "{}/data.json".format(_dir)

template = {
    "log_level": "INFO",
    "keys": {
        "discord_token": ""
    },
    "servers": {}
}


def get():
    """
    Get the current data dict of Discord from the data.json file

    Returns:
        data (dict): Parsed data.json file
    """

    logger.debug("Getting data.json")

    if os.path.exists(datafile):
        with open(datafile, 'r') as file:
            return json.load(file)
    else:
        write(template)
        return template


def write(data):
    """
    Write the data to the data.json file

    Args:
        data (dict): The updated data dictionary for Modis
    """

    logger.debug("Writing data.json")

    data = _sort(data)

    with open(datafile, 'w') as file:
        json.dump(data, file, indent=2)


def _sort(data):
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
            newdict[i[0]] = _sort(i[1])
        else:
            newdict[i[0]] = i[1]

    return OrderedDict(sorted(newdict.items(), key=lambda item: (_compare_type(type(item[1])), item[0])))


def _compare_type(t):
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
