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

from modis.tools import config

logger = logging.getLogger(__name__)

cache = {}


def get():
    """Read the data.json file and updates the cache"""

    logger.debug("Reading data")

    global cache

    if not os.path.exists(config.DATAFILE):
        # data.json does not exist
        logger.warning("data.json file not found. An empty one will be created.")
        _create(config.ROOT_TEMPLATE)
        return

    with open(config.DATAFILE, 'r') as file:
        try:
            cache = json.load(file)
            invalid_datafile = False
        except FileNotFoundError:
            invalid_datafile = True
    if invalid_datafile or not _validate(cache):
        # data.json is not a valid current Modis data file
        logger.warning("data.json file is outdated or invalid. A new one will be created and the old file will be renamed to data.json.old")

        # Don't overwrite existing files
        num = 1
        while os.path.exists(config.DATAFILE + ".old" + str(num)):
            num += 1
        os.rename(config.DATAFILE, config.DATAFILE + ".old" + str(num))
        _create(config.ROOT_TEMPLATE)


def write(new_data=None):
    """Update the data.json file.

    Args:
        new_data (dict): The updated data.json dict.
    """

    logger.debug("Writing data")

    global cache

    if not os.path.exists(config.DATAFILE):
        # data.json does not exist
        logger.warning("data.json file not found. An empty one will be created.")
        _create(config.ROOT_TEMPLATE)
        return

    if new_data:
        cache = new_data

    with open(config.DATAFILE, 'w') as file:
        json.dump(_sort(cache), file, indent=2)


def _create(template):
    """Create a new data.json file from the template.

    Args:
        template (dict): The template dict to create data.json with.
    """

    logger.info("Creating new data.json")

    global cache

    cache = template

    with open(config.DATAFILE, 'w') as file:
        json.dump(cache, file, indent=2)


def _validate(_dict):
    """Check if the current data is in the right format.

    Args:
        _dict (dict): The data dictionary to validate.
    """

    if "keys" not in _dict:
        return False
    if "discord_token" not in _dict["keys"]:
        return False
    return True


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
