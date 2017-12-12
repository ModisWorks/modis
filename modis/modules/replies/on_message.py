from modis import main
from modis.tools import data


async def on_message(message):
    """The on_message event handler for this module

    Args:
        message (discord.Message): Input message
    """

    # Only reply to server messages and don't reply to myself
    if message.server is None or message.author == message.channel.server.me:
        return

    # Retrieve replies from server data
    normal_replies = data.cache["servers"][message.server.id]["modules"]["replies"]["normal"]
    tts_replies = data.cache["servers"][message.server.id]["modules"]["replies"]["tts"]

    # Check normal replies
    for r in normal_replies.keys():
        if r in message.content.lower().replace(' ', ''):
            await main.client.send_typing(message.channel)
            await main.client.send_message(message.channel, normal_replies[r])

    # Check tts replies
    for r in tts_replies.keys():
        if r in message.content.lower().replace(' ', ''):
            await main.client.send_typing(message.channel)
            await main.client.send_message(message.channel, tts_replies[r], tts=True)
