import importlib
import logging
import os

import discord

from modis import datatools
from . import _data, ui_embed
from ..._client import client

logger = logging.getLogger(__name__)


async def on_message(message):
    """The on_message event handler for this module

    Args:
        message (discord.Message): Input message
    """

    # Simplify message info
    server = message.server
    author = message.author
    channel = message.channel
    content = message.content

    data = datatools.get_data()

    # Only reply to server messages and don't reply to myself
    if server is not None and author != channel.server.me:
        # Commands section
        prefix = data["discord"]["servers"][server.id]["prefix"]
        if content.startswith(prefix):
            # Parse message
            package = content.split(" ")
            command = package[0][len(prefix):]
            args = package[1:]
            arg = ' '.join(args)

            # Commands
            if command not in ["prefix", "activate", "deactivate"]:
                return

            is_admin = False
            for role in message.author.roles:
                if role.permissions.administrator or \
                        role.permissions.manage_server or \
                        role.permissions.manage_channels:
                    is_admin = True

            if not is_admin:
                await client.send_typing(channel)
                reason = "You must have a role that has the permission" + \
                         "'Administrator', 'Manage Server', or 'Manage Channels'"
                embed = ui_embed.error(channel, "Insufficient Permissions", reason)
                await embed.send()
                return

            if command == "prefix" and args:
                new_prefix = arg.lstrip()
                data["discord"]["servers"][server.id]["prefix"] = new_prefix
                # Write the data
                datatools.write_data(data)

                await client.send_typing(channel)
                embed = ui_embed.modify_prefix(channel, new_prefix)
                await embed.send()

            if command in ["activate", "deactivate"] and args:
                _dir = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
                _dir_modules = "{}/../".format(_dir)
                if not os.path.isfile("{}/{}/_data.py".format(_dir_modules, arg)):
                    await client.send_typing(channel)
                    embed = ui_embed.error(channel, "Error", "No module found named '{}'".format(arg))
                    await embed.send()
                    return

                try:
                    import_name = ".discord_modis.modules.{}.{}".format(arg, "_data")
                    module_data = importlib.import_module(import_name, "modis")

                    # Don't try and deactivate this module (not that it would do anything)
                    if module_data.modulename == _data.modulename:
                        await client.send_typing(channel)
                        embed = ui_embed.error(channel, "Error", "I'm sorry, Dave. I'm afraid I can't do that.")
                        await embed.send()
                        return

                    # This /should/ never happen if everything goes well
                    if module_data.modulename not in data["discord"]["servers"][server.id]:
                        await client.send_typing(channel)
                        embed = ui_embed.error(channel, "Error",
                                               "No data found for module '{}'".format(module_data.modulename))
                        await embed.send()
                        return

                    # Modify the module
                    if "activated" in data["discord"]["servers"][server.id][module_data.modulename]:
                        is_activate = command == "activate"
                        data["discord"]["servers"][server.id][module_data.modulename]["activated"] = is_activate
                        # Write the data
                        datatools.write_data(data)

                        await client.send_typing(channel)
                        embed = ui_embed.modify_module(channel, module_data.modulename, is_activate)
                        await embed.send()
                        return
                    else:
                        await client.send_typing(channel)
                        embed = ui_embed.error(channel, "Error",
                                               "Can't deactivate module '{}'".format(module_data.modulename))
                        await embed.send()
                        return
                except Exception as e:
                    logger.error("Could not modify module {}".format(arg))
                    logger.exception(e)
