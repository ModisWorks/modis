import importlib
import os

import discord

from modis import datatools, logger
from . import _data
from ..._client import client


async def update_server_data(server):
    """
    Updates the server info for the given server

    Args:
        server: The Discord server to update info for
    """

    data = datatools.get_data()
    # Add the server to server data if it doesn't yet exist
    send_welcome_message = False
    if server.id not in data["discord"]["servers"]:
        logger.debug("Adding new server to serverdata")
        data["discord"]["servers"][server.id] = {"prefix": "!"}
        if "mute_intro" not in data or not data["mute_intro"]:
            send_welcome_message = True

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
                datatools.write_data(data)
        except Exception as e:
            logger.error("Could not initialise module {}".format(module_name))
            logger.exception(e)

    datatools.write_data(data)

    # Send a welcome message now
    if send_welcome_message:
        default_channel = server.default_channel
        if not default_channel:
            for channel in server.channels:
                if channel.name == "general":
                    default_channel = channel
                    break
        if not default_channel:
            for channel in server.channels:
                if "general" in channel.name:
                    default_channel = channel
                    break
        if not default_channel:
            for channel in server.channels:
                if channel.type == discord.ChannelType.text:
                    default_channel = channel
                    break

        # Display a welcome message
        if default_channel:
            hello_message = "Hello! I'm Modis.\n\n" + \
                            "The prefix is currently `!`, and can be changed at any time using `!prefix`\n\n" + \
                            "You can use `!help` to get help commands for all modules, " + \
                            "or {} me to get the server prefix and help commands.".format(server.me.mention)
            await client.send_message(default_channel, hello_message)


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


def update_cmd_db():
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
