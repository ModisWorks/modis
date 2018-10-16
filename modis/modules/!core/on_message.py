import logging

from modis import main
from modis.tools import data

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
    prefix = data.cache["servers"][message.server.id]["prefix"]
    if not message.content.startswith(prefix):
        return

    # Parse message
    package = message.content.split(" ")
    root = package.pop(0)[len(prefix):]
    aux = []
    while len(package) > 0:
        if not package[0].startswith("-"):
            break
        aux.append(package.pop(0)[1:])
    query = " ".join(package)

    # Process command
    for module_name in _data.cmd_db.keys():
        # Check for commands existing for this module
        if "cmd" not in _data.cmd_db[module_name]:
            continue
        # Check for command in list of commands for this module
        if root not in _data.cmd_db[module_name]["cmd"].keys():
            continue

        # Permission checks
        if "level" not in _data.cmd_db[module_name]["cmd"][root].keys():
            # Send command to module
            await _data.cmd_db[module_name]["eh"](root, aux, query, message)
        else:
            level = _data.cmd_db[module_name]["cmd"][root]["level"]

            if isinstance(level, int):
                # Permission is specified as role ranking
                pass

            elif isinstance(level, str):
                # Permission is specified as specific Discord permission
                pass
        # TODO permission checks
