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
        # Retrieve replies from serverdata
        normal_replies = get_serverdata()[server.id][modulename]["normal"]
        tts_replies = get_serverdata()[server.id][modulename]["tts"]

        # Check normal replies
        for r in normal_replies.keys():
            if r in content.lower().replace(' ', ''):
                await client.send_typing(channel)
                await client.send_message(channel, normal_replies[r])

        # Check tts replies
        for r in tts_replies.keys():
            if r in content.lower().replace(' ', ''):
                await client.send_typing(channel)
                await client.send_message(channel, tts_replies[r])
