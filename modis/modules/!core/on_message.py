import logging

from modis.tools import datatools
from . import _data

logger = logging.getLogger(__name__)


async def on_message(message):
    """Parses commands into arrays

    Args:
        message: (discord.Message): Input message
    """

    # Don't reply to myself
    if message.author == message.channel.server.me:
        return

    # Check prefix
    prefix = datatools.data["servers"][message.server.id]["prefix"]
    if not message.content.startswith(prefix):
        return

    logger.debug("Cmd call s: {} c: {}".format(message.server, message.channel))

    # Parse message
    package = message.content.split(" ")
    root = package.pop(0)[len(prefix):]
    aux = []
    for arg in package[1:]:
        if arg.startswith("-"):
            aux.append(package.pop(0))
        else:
            break
    query = " ".join(package)
