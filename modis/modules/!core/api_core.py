import logging

from modis import main
from modis.tools import data, config, moduledb
from . import _data

logger = logging.getLogger(__name__)


def guild_update(guild_id):
    """Updates a guild's info in the database.

    Args:
        guild_id (int): The guild to update.
    """

    logger.debug("Updating guild {}".format(guild_id))

    # Add the guild to database if it doesn't yet exist
    if str(guild_id) not in data.cache["guilds"]:
        logger.debug("Adding guild {} to database".format(guild_id))
        data.cache["guilds"][str(guild_id)] = config.GUILD_TEMPLATE

        # Register slots for per-guild module specific data
        module_names = moduledb.get_names()
        for module_name in module_names:
            info = moduledb.get_import_specific("__info", module_name)
            try:
                if info.DATA_GUILD:
                    data.cache["guilds"][str(guild_id)]["modules"][module_name] = info.DATA_GUILD
            except AttributeError:
                logger.debug("Guild data slot not requested for " + module_name)

        print(data)

        data.push()


def guild_remove(guild_id):
    """Removes a guild from the database.

    Args:
        guild_id (int): The guild to remove.
    """

    logger.debug("Removing guild {} from database".format(guild_id))

    try:
        data.cache["guilds"].pop(str(guild_id))
    except KeyError:
        logger.warning("Guild {} is nonexistent in database".format(guild_id))
    else:
        data.push()


def guild_clean():
    """Removes from the database guilds that Modis is no longer part of."""

    logger.debug("Cleaning guilds...")

    guilds_old = list(data.cache["guilds"].keys())
    guilds_new = [guild.id for guild in main.client.guilds]

    for guild_id in guilds_old:
        if guild_id not in guilds_new:
            guild_remove(guild_id)

    for guild_id in guilds_new:
        if guild_id not in guilds_old:
            guild_update(guild_id)


def cmd_db_update():
    """Updates the command database"""

    logger.debug("Updating command database")

    # Retrive module "header" files and functions
    cmd_db = moduledb.get_imports(["__info", "on_command"])

    for module_name in cmd_db.keys():
        _data.cmd_db[module_name] = {}

        if "on_command" in cmd_db[module_name].keys():
            # Enter module functions into database
            _data.cmd_db[module_name]["eh"] = cmd_db[module_name]["on_command"].on_command

        if "__info" in cmd_db[module_name].keys():
            # Enter module "header" file into database
            _data.cmd_db[module_name]["cmd"] = cmd_db[module_name]["__info"].COMMANDS
            # TODO also add to static database, implement checks to see if its already in there
