import logging
import os
import importlib

from modis.tools import datatools
from . import _data
from modis.common import client

logger = logging.getLogger(__name__)


def server_update(server_id):
    """Updates the server info in data.json for the given server.

    Args:
        server_id (str): The Discord server to update info for.
    """

    logger.debug("Updating server {}".format(server_id))

    data = datatools.get()

    # Add the server to server data if it doesn't yet exist
    if server_id not in data["servers"]:
        logger.debug("Adding new server to data.json")
        data["servers"][server_id] = datatools.SERVER_TEMPLATE
        datatools.write(data)


def server_remove(server_id):
    """Remove a server from data.json.

    Args:
        server_id (str): The server to remove.
    """

    logger.debug("Removing server from data.json")
    data = datatools.get()
    try:
        data["servers"].pop(server_id)
    except KeyError:
        logger.warning("Server to be removed does not exist")
    else:
        logger.debug("Removed server {}".format(server_id))
        datatools.write(data)


def server_clean():
    """Checks all servers, removing any that Modis isn't part of any more"""

    logger.debug("Cleaning servers")

    data = datatools.get()
    for server_id in data["servers"]:
        exists = False
        for server_obj in client.servers:
            if server_obj.id == server_id:
                exists = True
        if not exists:
            server_remove(server_id)


def cmd_db_update():
    """Updates the command database"""

    logger.debug("Updating command database")

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
