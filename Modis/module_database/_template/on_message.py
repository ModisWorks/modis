from share import *
from ._constants import *


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
        # Commands section
        if content.startswith(get_serverdata()[server.id]["prefix"]):
            # Parse message
            package = content.split(" ")
            command = package[0][1:]
            args = package[1:]
            arg = ' '.join(args)
