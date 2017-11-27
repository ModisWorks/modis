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

from modis.common import WORK_DIR, DATAFILE, ROOT_TEMPLATE, SERVER_TEMPLATE


logger = logging.getLogger(__name__)

data = {}


def create(template):
    """Create a new data.json file from the template.

    Args:
        template (dict): The template dict to create data.json with.
    """

    global data

    data = template

    with open(DATAFILE, 'w') as file:
        json.dump(data, file, indent=2)


def get():
    """Read the data.json file.

    Returns:
        data (dict): data.json parsed into a dict.
    """

    logger.debug("Getting data.json")

    global data

    if not os.path.exists(DATAFILE):
        logger.CRITICAL("data.json not found. An empty one was created.")
        create(ROOT_TEMPLATE)
        return data

    with open(DATAFILE, 'r') as file:
        data = json.load(file)
        return data


def write(new_data=None):
    """Update the data.json file.

    Args:
        new_data (dict): The updated data.json dict.
    """

    logger.debug("Writing data.json")

    global data

    if not os.path.exists(DATAFILE):
        logging.CRITICAL("data.json not found. An empty one was created.")
        create(ROOT_TEMPLATE)
        return

    if new_data:
        data = new_data
    data = _sort(data)

    with open(DATAFILE, 'w') as file:
        json.dump(data, file, indent=2)


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
