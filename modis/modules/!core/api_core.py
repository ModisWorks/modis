import logging

from modis import main
from modis.tools import data, config, moduledb
from . import _data

logger = logging.getLogger(__name__)


def server_update(server_id):
    """Updates the server info in data.json for the given server.

    Args:
        server_id (str): The Discord server to update info for.
    """

    logger.debug("Updating server {}".format(server_id))

    # Add the server to server data if it doesn't yet exist
    if server_id not in data.cache["servers"]:
        logger.debug("Adding new server to data.json")
        data.cache["servers"][server_id] = config.SERVER_TEMPLATE

        # Register slots for per-server module specific data
        module_names = moduledb.get_names()
        for module_name in module_names:
            info = moduledb.get_import_specific("__info", module_name)
            try:
                if info.DATA_SERVER:
                    data.cache["servers"][server_id]["modules"][module_name] = info.DATA_SERVER
            except AttributeError:
                logger.debug("Server data slot not requested for " + module_name)

        print(data)

        data.write()


def server_remove(server_id):
    """Remove a server from data.json.

    Args:
        server_id (str): The server to remove.
    """

    logger.debug("Removing server from data.json")

    try:
        data.cache["servers"].pop(server_id)
    except KeyError:
        logger.warning("Server to be removed does not exist")
    else:
        logger.debug("Removed server {}".format(server_id))
        data.write()


def server_clean():
    """Checks all servers, removing any that Modis isn't part of any more"""

    logger.debug("Cleaning servers")

    serverlist = list(data.cache["servers"].keys())

    for server_id in serverlist:
        exists = False
        for server_obj in main.client.servers:
            if server_obj.id == server_id:
                exists = True
        if not exists:
            server_remove(server_id)


def cmd_db_update():
    """Updates the command database"""

    logger.debug("Updating command database")

    cmd_db = moduledb.get_imports(["__info", "on_command"])
    for module_name in cmd_db.keys():
        _data.cmd_db[module_name] = {}
        if "on_command" in cmd_db[module_name].keys():
            _data.cmd_db[module_name]["eh"] = cmd_db[module_name]["on_command"].on_command
        if "__info" in cmd_db[module_name].keys():
            _data.cmd_db[module_name]["cmd"] = cmd_db[module_name]["__info"].COMMANDS
            # TODO also add to static database, implement checks to see if its already in there
