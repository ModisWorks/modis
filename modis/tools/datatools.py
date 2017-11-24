"""
This tool handles reading and saving data. Modis uses the JSON protocol to store
data to ensure easy accessibility.

This tool also contains the templates for the data structure of both the root
structure and the structure for each server.
"""

import logging
import os
import json
from collections import OrderedDict

from modis.cache import WORK_DIR

DATAFILE = "{}/data.json".format(WORK_DIR)
ROOT_TEMPLATE = {
    "log_level": "INFO",
    "keys": {
        "discord_token": ""
    },
    "servers": {}
}
SERVER_TEMPLATE = {
    "prefix": "!",
    "activation": {},
    "commands": {}
}

logger = logging.getLogger(__name__)
data_soft = {}


def create():
    """Create a new data.json file from the template."""

    write(ROOT_TEMPLATE)


def get():
    """Read the data.json file.

    Returns:
        data (dict): data.json parsed into a dict.
    """

    logger.debug("Getting data.json")

    if not os.path.exists(DATAFILE):
        logging.CRITICAL("data.json not found. An empty one was created.")
        create()

    global data_soft
    with open(DATAFILE, 'r') as file:
        data_soft = json.load(file)
        return data_soft


def write(data):
    """Update the data.json file.

    Args:
        data (dict): The updated data.json dict.
    """

    logger.debug("Writing data.json")

    data = _sort(data)

    with open(DATAFILE, 'w') as file:
        json.dump(data, file, indent=2)


def _sort(data):
    """Recursively sort all elements in a dictionary.

    Args:
        data (dict): The dictionary to sort.

    Returns:
        sorted_dict (OrderedDict): The sorted data dict.
    """

    newdict = {}

    for i in data.items():
        if type(i[1]) is dict:
            newdict[i[0]] = _sort(i[1])
        else:
            newdict[i[0]] = i[1]

    def _compare_type(t):
        """Give the order of the type for the dictionary.

        Args:
            t (type): The type to compare.

        Returns:
            order (int): 1=dict/OrderedDict, 0=other
        """

        if t in [dict, OrderedDict]:
            return 1

        return 0
    # TODO check if it should be _compare_type(type(item[1]), type(item[0]))
    return OrderedDict(sorted(newdict.items(), key=lambda item: (_compare_type(type(item[1])), item[0])))
