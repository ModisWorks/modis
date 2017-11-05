import importlib
import os

from modis import datatools, logger
from ..._client import client


def update_server_data(server_id):
    """
    Updates the server info for the given server

    Args:
        server_id (int): The Discord server to update info for
    """

    data = datatools.get_data()
    # Add the server to server data if it doesn't yet exist
    if server_id not in data["discord"]["servers"]:
        logger.debug("Adding new server to serverdata")
        data["discord"]["servers"][server_id] = {"prefix": "!"}

    # Make sure all modules are in the server
    _dir = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    _dir_modules = "{}/../".format(_dir)
    for module_name in os.listdir(_dir_modules):
        if not os.path.isfile("{}/{}/_data.py".format(_dir_modules, module_name)):
            logger.warning("No _data.py file found for module {}".format(module_name))
            continue

        try:
            import_name = ".discord_modis.modules.{}.{}".format(module_name, "_data")
            _data = importlib.import_module(import_name, "modis")

            if _data.modulename not in data["discord"]["servers"][server_id]:
                data["discord"]["servers"][server_id][_data.modulename] = _data.sd_structure
                datatools.write_data(data)
        except Exception as e:
            logger.error("Could not initialise module {}".format(module_name))
            logger.exception(e)

    datatools.write_data(data)


def remove_server_data(server_id):
    """
    Remove a server from the server data

    Args:
        server_id (int): The server to remove from the server data
    """

    logger.debug("Removing server from serverdata")
    # Remove the server from data
    data = datatools.get_data()
    if server_id in data["discord"]["servers"]:
        data["discord"]["servers"].pop(server_id)
        datatools.write_data(data)


def check_all_servers():
    """Checks all servers, removing any that Modis isn't part of any more"""
    data = datatools.get_data()
    for server_id in data["discord"]["servers"]:
        is_in_client = False
        for client_server in client.servers:
            if server_id == client_server.id:
                is_in_client = True
                break

        if not is_in_client:
            remove_server_data(server_id)
