"""
This tool handles reading and editing the database. Modis uses the JSON protocol to store
data to ensure easy accessibility.
"""

import json
import logging
import os
from collections import OrderedDict

from modis.tools import config

logger = logging.getLogger(__name__)

cache = {}


def get(server, module_name, path=None):
    """Get a specific database entry belonging to a module.

    Args:
        server (str): Server ID of desired server, edits global module database if not specified.
        module_name (str): Name of module to edit database entry of.
        path (list): List of strings describing the path to the desired database entry.

    Returns:
        entry: The retrieved database entry.
    """

    global cache

    entry = cache["servers"][server]["modules"][module_name]

    if not path:
        return entry

    for key in path:
        entry = entry[key]
    return entry


def edit(server, module_name, value, path=None):
    """Edit a specific datapoint belonging to a module.

    Args:
        server (str): Server ID of desired server, edits global module database if not specified.
        module_name (str): Name of module to edit the database entry of.
        value: Value to change the database entry to.
        path (list): List of strings describing the path to the desired database entry.
    """

    global cache

    if path:
        entry = cache["servers"][server]["modules"]
        for key in path[:-1]:
            entry = entry[key]
        entry[path[-1]] = value
    else:
        cache["servers"][server]["modules"][module_name] = value

    push()


def pull():
    """

    Returns:

    """

    logger.debug("Pulling database from file")

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


def push(new_data=None):
    """Update the data.json file.

    Args:
        new_data (dict): The updated data.json dict.
    """

    logger.debug("Pushing database to file")

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
