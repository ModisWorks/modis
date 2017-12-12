import logging

from modis import main
from modis.tools import data

logger = logging.getLogger(__name__)


async def on_message(msgobj):
    """The on_message event handler for this module

    Args:
        msgobj (discord.Message): Input message
    """

    # Only reply to server messages and don't reply to myself
    if msgobj.server is None or msgobj.author == msgobj.channel.server.me:
        return

    # Retrieve replies from server data
    normal_replies = data.cache["servers"][msgobj.server.id]["modules"]["replies"]["normal"]
    tts_replies = data.cache["servers"][msgobj.server.id]["modules"]["replies"]["tts"]

    # Check normal replies
    for r in normal_replies.keys():
        if r in msgobj.content.lower().replace(' ', ''):
            await main.client.send_typing(msgobj.channel)
            await main.client.send_message(msgobj.channel, normal_replies[r])

    # Check tts replies
    for r in tts_replies.keys():
        if r in msgobj.content.lower().replace(' ', ''):
            await main.client.send_typing(msgobj.channel)
            await main.client.send_message(msgobj.channel, tts_replies[r], tts=True)
