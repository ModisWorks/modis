import discord

from modis import data
from . import api_help, ui_embed
from ..._client import client


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
        # Commands section
        prefix = data["discord"]["servers"][server.id]["prefix"]
        if content.startswith(prefix):
            # Parse message
            package = content.split(" ")
            command = package[0][len(prefix):]
            args = package[1:]
            arg = ' '.join(args)

            # Commands
            if command == 'help':
                if args:
                    # Parse message
                    datapacks = api_help.get_help_datapacks(arg, prefix)
                    # Create embed UI
                    if datapacks:
                        await client.send_typing(channel)
                        embed = ui_embed.success(channel, arg, datapacks)
                        try:
                            await embed.send()
                        except discord.errors.HTTPException:
                            embed = ui_embed.http_exception(channel, arg)
                            await embed.send()
                else:
                    # Parse message
                    datapacks = api_help.get_help_commands(prefix)
                    # Create embed UI
                    if datapacks:
                        await client.send_typing(channel)
                        embed = ui_embed.success(channel, arg, datapacks)
                        try:
                            await embed.send()
                        except discord.errors.HTTPException:
                            embed = ui_embed.http_exception(channel, arg)
                            await embed.send()
