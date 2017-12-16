import logging

from modis import main

from . import api_flipcheck

logger = logging.getLogger(__name__)


async def on_message(msgobj):
    """The on_message event handler for this module

    Args:
        msgobj (discord.Message): Input message
    """

    # TODO work out how to make this conform to new activation
    # if not data["discord"]["servers"][server.id][_data.modulename]["activated"]:
    #     return

    # Only reply to server messages and don't reply to myself
    if msgobj.server is None or msgobj.author == msgobj.channel.server.me:
        return

    # Do a flip check
    flipchecked = api_flipcheck.flipcheck(msgobj.content)
    if flipchecked:
        await main.client.send_typing(msgobj.channel)
        await main.client.send_message(msgobj.channel, flipchecked)
