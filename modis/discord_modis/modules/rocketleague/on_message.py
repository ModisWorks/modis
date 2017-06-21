from ..._client import client
from .... import datatools

from . import _data

from . import api_rocketleaguestats
from . import ui_embed

import requests


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

    # Make sure this module is in serverdata for this server
    data = datatools.get_data()
    if _data.modulename not in data["discord"]["servers"][server.id]:
        data["discord"]["servers"][server.id][_data.modulename] = _data.sd_structure
        datatools.write_data(data)

    # Only reply to server messages and don't reply to myself
    if server is not None and author != channel.server.me:
        # Commands section
        if content.startswith(datatools.get_data()["discord"]["servers"][server.id]["prefix"]):
            # Parse message
            package = content.split(" ")
            command = package[0][1:]
            args = package[1:]
            arg = ' '.join(args)

            # Commands
            if command == 'rlstats':
                await client.send_typing(channel)

                # Get Rocket League stats from stats API
                success, rldata = api_rocketleaguestats.check_rank(arg)
                # Create embed UI
                if success:
                    embed = ui_embed.success(channel, rldata[0], rldata[1], rldata[2])
                else:
                    embed = ui_embed.fail_api(channel)

                await embed.send()
