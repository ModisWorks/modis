"""THE DATABASE HANDLER

This tool handles reading and editing of the data.json database. Modis uses the JSON protocol to store data to ensure easy readability and accessibility. The various functions in this file make it easy for modules to read and edit the database, and also provides an easy way to expand into more complex database technologies such as mongodb in the future.
"""

import json
import logging
import os
from collections import OrderedDict
import typing

from modis.tools import config

logger = logging.getLogger(__name__)

# Create the cache object
cache: typing.Dict[str, typing.Any] = {}
# The cache dict is an exact copy of database.json, but stored in RAM. It makes it much easier for modules and framework to access the database without requiring disk reads and writes every time.

# TODO Implement exception handling


def get(guild: int,
        module: str,
        path: typing.List[str] = None) -> typing.Any:
    """Gets a database entry.

    Retreives a specific database entry belonging to a module. Under normal usage, this and `data.edit()` should be the only functions you need.

    Args:
        guild (int): Guild ID of the guild data to read.
        module (str): Module name of the module data to read.
        path (list): List of strings describing the path to the desired database entry.

    Returns:
        The retrieved database entry.
    """

    global cache

    entry = cache["guilds"][str(guild)]["modules"][module]

    if not path:
        return entry

    for key in path:
        entry = entry[key]
    return entry


def edit(guild: int,
         module: str,
         value,
         path: typing.List[str] = None) -> None:
    """Edits a database entry.

    Edits a specific database entry belonging to a module. Under normal usage, this and `data.get()` should be the only functions you need.

    Args:
        guild (int): Guild ID of the guild data to edit.
        module (str): Module name of the module data to edit.
        value: Value to change the database entry to.
        path (list): List of strings describing the path to the desired database entry.
    """

    global cache

    if path:
        entry = cache["guilds"][str(guild)]["modules"]
        for key in path[:-1]:
            entry = entry[key]
        entry[path[-1]] = value
    else:
        cache["guilds"][guild]["modules"][module] = value

    push()


def pull() -> None:
    """Updates cache from disk

    Updates the `cache` object with the current state of the data.json file.
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


def push(new_data: dict = None) -> None:
    """Updates disk from cache

    Updates the data.json file with the current state of the `cache` object.

    Args:
        new_data (dict): A custom dict to set data.json to. This argument is DANGEROUS and you could easily destroy your data.json if you're not careful.
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


def _create(_template: dict) -> None:
    """Creates a new data.json file.

    Creates a new data.json file from the template defined in modis.tools.config, or uses the `template` argument to create a custom data.json file.

    Args:
        _template (dict): The template dict to create data.json with.
    """

    logger.info("Creating new data.json")

    global cache

    cache = _template

    with open(config.DATAFILE, 'w') as file:
        json.dump(cache, file, indent=2)


def _validate(_template: dict) -> bool:
    """Validates a data.json dictionary

    Check if  the dictionary `_template` is in the right format for a data.json file using a hard-coded method, that will be changed to use the template defined in modis.tools.config in the future.

    Args:
        _template (dict): The data dictionary to validate.

    Returns:
        Bool of whether or not the database is valid
    """

    # TODO make this not hard-coded
    if "keys" not in _template:
        return False
    if "discord_token" not in _template["keys"]:
        return False
    return True


def _sort(_dict: dict) -> OrderedDict:
    """Sorts a dictionary.

    Recursively sorts all elements in a dictionary to produce an OrderedDict.

    Args:
        _dict (dict): The dictionary to sort.

    Returns:
        An OrderedDict with its items sorted.
    """

    newdict = {}

    for i in _dict.items():
        if type(i[1]) is dict:
            newdict[i[0]] = _sort(i[1])
        else:
            newdict[i[0]] = i[1]

    # TODO check if it should be _compare_type(type(item[1]), type(item[0]))
    return OrderedDict(sorted(newdict.items(), key=lambda item: (_compare(type(item[1])), item[0])))


def _compare(_type: type) -> int:
    """Defines a type order for a dictionary.

    Args:
        _type (type): The type to compare.

    Returns:
        An integer where 1 = dict/OrderedDict, and 0 = other
    """

    if _type in [dict, OrderedDict]:
        return 1

    return 0
