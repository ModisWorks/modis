from ..._client import client
from .... import datatools

from . import _data


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
        # Retrieve replies from serverdata
        normal_replies = datatools.get_data()["discord"]["servers"][server.id][_data.modulename]["normal"]
        tts_replies = datatools.get_data()["discord"]["servers"][server.id][_data.modulename]["tts"]

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
