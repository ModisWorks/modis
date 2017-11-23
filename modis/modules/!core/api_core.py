import logging
import os
import importlib

from modis.tools import datatools
from . import _data
from modis.cache import client

logger = logging.getLogger(__name__)


async def server_update(server):
    """
    Updates the server info for the given server

    Args:
        server: The Discord server to update info for
    """

    data = data.get_data()

    # Add the server to server data if it doesn't yet exist
    if server.id not in data["servers"]:
        logger.debug("Adding new server to data.json")
        data["servers"][server.id] = {"prefix": "!"}

    # Make sure all modules are in the server
    _dir = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    _dir_modules = "{}/../".format(_dir)
    for module_name in os.listdir(_dir_modules):
        if module_name.startswith("_") or module_name.startswith("!"):
            continue

        if not os.path.isfile("{}/{}/_data.py".format(_dir_modules, module_name)):
            logger.warning("No _data.py file found for module {}".format(module_name))
            continue

        try:
            import_name = ".discord_modis.modules.{}.{}".format(module_name, "_data")
            _data = importlib.import_module(import_name, "modis")

            if _data.modulename not in data["discord"]["servers"][server.id]:
                data["discord"]["servers"][server.id][_data.modulename] = _data.sd_structure
                data.write_data(data)
        except Exception as e:
            logger.error("Could not initialise module {}".format(module_name))
            logger.exception(e)

    data.write_data(data)


def server_remove(server_id):
    """
    Remove a server from the server data

    Args:
        server_id (int): The server to remove from the server data
    """

    logger.debug("Removing server from serverdata")
    # Remove the server from data
    data = data.get_data()
    if server_id in data["discord"]["servers"]:
        data["discord"]["servers"].pop(server_id)
        data.write_data(data)


def server_check():
    """Checks all servers, removing any that Modis isn't part of any more"""
    data = data.get_data()
    for server_id in data["discord"]["servers"]:
        is_in_client = False
        for client_server in client.servers:
            if server_id == client_server.id:
                is_in_client = True
                break

        if not is_in_client:
            server_remove(server_id)


def cmd_db_update():
    """Updates the command database"""

    cmd_event_handlers = []

    database_dir = "{}/../".format(os.path.dirname(os.path.realpath(__file__)))
    for module_name in os.listdir(database_dir):
        if module_name.startswith("_"):
            return
        module_dir = "{}/{}".format(database_dir, module_name)

        module_event_handlers = os.listdir(module_dir)

        if "on_command.py" in module_event_handlers:
            import_name = ".discord_modis.modules.{}.on_command".format(module_name)
            cmd_event_handlers.append(importlib.import_module(import_name, "modis"))

    _data.cmd_db = cmd_event_handlers
    print(_data.cmd_db)
