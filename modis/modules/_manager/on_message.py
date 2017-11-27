import logging

import discord

from modis import datatools
from . import _data, api_manager, ui_embed
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

    data = data.get_data()

    # Only reply to server messages and don't reply to myself
    if server is not None and author != channel.server.me:
        prefix = data["discord"]["servers"][server.id]["prefix"]
        # Check for mentions reply to mentions
        if channel.server.me in message.mentions:
            await client.send_typing(channel)
            response = "The current server prefix is `{0}`. Type `{0}help` for help.".format(prefix)
            await client.send_message(channel, response)

        # Commands section
        if content.startswith(prefix):
            # Parse message
            package = content.split(" ")
            command = package[0][len(prefix):]
            args = package[1:]
            arg = ' '.join(args)

            # Commands
            if command not in ["prefix", "activate", "deactivate", "warnmax", "warn", "ban"]:
                return

            is_admin = author == server.owner
            for role in message.author.roles:
                if role.permissions.administrator:
                    is_admin = True

            if not is_admin:
                await client.send_typing(channel)
                reason = "You must have a role that has the permission 'Administrator'"
                embed = ui_embed.error(channel, "Insufficient Permissions", reason)
                await embed.send()
                return

            if command == "prefix" and args:
                new_prefix = arg.replace(" ", "").strip()
                data["discord"]["servers"][server.id]["prefix"] = new_prefix
                # Write the data
                data.write_data(data)

                await client.send_typing(channel)
                embed = ui_embed.modify_prefix(channel, new_prefix)
                await embed.send()

            if command == "warnmax" and args:
                try:
                    warn_max = int(arg)
                    if warn_max > 0:
                        data["discord"]["servers"][server.id][_data.modulename]["warnings_max"] = warn_max
                        datatools.write_data(data)
                        await client.send_typing(channel)
                        embed = ui_embed.warning_max_changed(channel, warn_max)
                        await embed.send()
                    else:
                        reason = "Maximum warnings must be greater than 0"
                        embed = ui_embed.error(channel, "Error", reason)
                        await embed.send()
                except (ValueError, TypeError):
                    reason = "Warning maximum must be a number"
                    embed = ui_embed.error(channel, "Error", reason)
                    await embed.send()
                except Exception as e:
                    logger.exception(e)

            if command == "warn" and args:
                for user in message.mentions:
                    await api_manager.warn_user(channel, user)

            if command == "ban" and args:
                for user in message.mentions:
                    await api_manager.ban_user(channel, user)

            if command == "activate" and args:
                await api_manager.activate_module(channel, arg, True)
            elif command == "deactivate" and args:
                await api_manager.activate_module(channel, arg, False)
