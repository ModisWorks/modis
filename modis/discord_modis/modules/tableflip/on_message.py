from ..._client import client
from .... import datatools

from . import _data

from . import api_flipcheck


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
        # Do a flipcheck
        flipchecked = api_flipcheck.flipcheck(content)
        if flipchecked:
            await client.send_typing(channel)
            await client.send_message(channel, flipchecked)
