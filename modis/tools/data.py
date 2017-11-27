"""
This tool handles reading and saving data. Modis uses the JSON protocol to store
data to ensure easy accessibility.

This tool also contains the templates for the data structure of both the root
structure and the structure for each server.
"""

import json
import logging
import os
from collections import OrderedDict

from modis.tools.config import DATAFILE, ROOT_TEMPLATE

logger = logging.getLogger(__name__)

cache = {}


def create(template):
    """Create a new data.json file from the template.

    Args:
        template (dict): The template dict to create data.json with.
    """

    global cache

    cache = template

    with open(DATAFILE, 'w') as file:
        json.dump(cache, file, indent=2)


def get():
    """Read the data.json file.

    Returns:
        data (dict): data.json parsed into a dict.
    """

    logger.debug("Getting data.json")

    global cache

    if not os.path.exists(DATAFILE):
        logger.warning("data.json not found. An empty one was created.")
        create(ROOT_TEMPLATE)
        return cache

    with open(DATAFILE, 'r') as file:
        cache = json.load(file)
        return cache


def write(new_data=None):
    """Update the data.json file.

    Args:
        new_data (dict): The updated data.json dict.
    """

    logger.debug("Writing data.json")

    global cache

    if not os.path.exists(DATAFILE):
        logging.CRITICAL("data.json not found. An empty one was created.")
        create(ROOT_TEMPLATE)
        return

    if new_data:
        cache = new_data
    cache = _sort(cache)

    with open(DATAFILE, 'w') as file:
        json.dump(cache, file, indent=2)


def _sort(_dict):
    """Recursively sort all elements in a dictionary.

    Args:
        _dict (dict): The dictionary to sort.

    Returns:
        sorted_dict (OrderedDict): The sorted data dict.
    """

    newdict = {}

    for i in _dict.items():
        if type(i[1]) is dict:
            newdict[i[0]] = _sort(i[1])
        else:
            newdict[i[0]] = i[1]

    # TODO check if it should be _compare_type(type(item[1]), type(item[0]))
    return OrderedDict(sorted(newdict.items(), key=lambda item: (_compare(type(item[1])), item[0])))


def _compare(_type):
    """Give the order of the type for the dictionary.

    Args:
        _type (type): The type to compare.

    Returns:
        order (int): 1=dict/OrderedDict, 0=other
    """

    if _type in [dict, OrderedDict]:
        return 1

    return 0