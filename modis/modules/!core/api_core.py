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
        data.write()

    # TODO add module subdata


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

    for server_id in data.cache["servers"]:
        exists = False
        for server_obj in main.client.servers:
            if server_obj.id == server_id:
                exists = True
        if not exists:
            server_remove(server_id)


def cmd_db_update():
    """Updates the command database"""

    logger.debug("Updating command database")

    cmd_event_handlers = moduledb.get_py(["commands"])["commands"]

    _data.cmd_db = cmd_event_handlers
