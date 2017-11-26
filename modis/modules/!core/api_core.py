import logging

from modis import common
from modis.tools import datatools
from modis.tools import moduletools
from . import _data

logger = logging.getLogger(__name__)


def server_update(server_id):
    """Updates the server info in data.json for the given server.

    Args:
        server_id (str): The Discord server to update info for.
    """

    logger.debug("Updating server {}".format(server_id))

    # Add the server to server data if it doesn't yet exist
    if server_id not in datatools.data["servers"]:
        logger.debug("Adding new server to data.json")
        datatools.data["servers"][server_id] = datatools.SERVER_TEMPLATE
        datatools.write()


def server_remove(server_id):
    """Remove a server from data.json.

    Args:
        server_id (str): The server to remove.
    """

    logger.debug("Removing server from data.json")

    try:
        datatools.data["servers"].pop(server_id)
    except KeyError:
        logger.warning("Server to be removed does not exist")
    else:
        logger.debug("Removed server {}".format(server_id))
        datatools.write()


def server_clean():
    """Checks all servers, removing any that Modis isn't part of any more"""

    logger.debug("Cleaning servers")

    for server_id in datatools.data["servers"]:
        exists = False
        for server_obj in common.client.servers:
            if server_obj.id == server_id:
                exists = True
        if not exists:
            server_remove(server_id)


def cmd_db_update():
    """Updates the command database"""

    logger.debug("Updating command database")

    cmd_event_handlers = moduletools.get_files(["commands"])["commands"]

    _data.cmd_db = cmd_event_handlers
