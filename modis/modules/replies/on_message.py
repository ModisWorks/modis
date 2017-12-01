from modis import main
from modis.tools import data


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

    # TODO port to new activation
    # if not data["discord"]["servers"][server.id][_data.modulename]["activated"]:
    #     return

    # Only reply to server messages and don't reply to myself
    if server is not None and author != channel.server.me:
        # Retrieve replies from server data
        normal_replies = data.cache["servers"][server.id]["modules"]["replies"]["normal"]
        tts_replies = data.cache["servers"][server.id]["modules"]["replies"]["tts"]

        # Check normal replies
        for r in normal_replies.keys():
            if r in content.lower().replace(' ', ''):
                await main.client.send_typing(channel)
                await main.client.send_message(channel, normal_replies[r])

        # Check tts replies
        for r in tts_replies.keys():
            if r in content.lower().replace(' ', ''):
                await main.client.send_typing(channel)
                await main.client.send_message(channel, tts_replies[r])
