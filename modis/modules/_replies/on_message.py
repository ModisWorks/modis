from modis import datatools
from . import _data
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
        # Retrieve replies from server data
        normal_replies = data["discord"]["servers"][server.id][_data.modulename]["normal"]
        tts_replies = data["discord"]["servers"][server.id][_data.modulename]["tts"]

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
