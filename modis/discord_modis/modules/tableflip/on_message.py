from modis import datatools
from . import _data, api_flipcheck
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

    data = datatools.get_data()

    if not data["discord"]["servers"][server.id][_data.modulename]["activated"]:
        return

    # Only reply to server messages and don't reply to myself
    if server is not None and author != channel.server.me:
        # Do a flip check
        flipchecked = api_flipcheck.flipcheck(content)
        if flipchecked:
            await client.send_typing(channel)
            await client.send_message(channel, flipchecked)
