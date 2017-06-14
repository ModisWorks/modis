from globalvars import *
from ._constants import *

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
    _sd = get_serverdata()
    if modulename not in _sd[server.id]:
        _sd[server.id][modulename] = sd_structure
        write_serverdata(_sd)

    # Only reply to server messages and don't reply to myself
    if server is not None and author != channel.server.me:
        # Do a flipcheck
        flipchecked = api_flipcheck.flipcheck(content)
        if flipchecked:
            await client.send_typing(channel)
            await client.send_message(channel, flipchecked)
