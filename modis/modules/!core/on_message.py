import logging

from modis import main
from modis.tools import data

from . import _data

logger = logging.getLogger(__name__)


async def on_message(msgobj):
    """Parses commands into arrays

    Args:
        msgobj: (discord.Message): Input message
    """

    # Don't reply to myself
    if msgobj.author == main.client.user:
        return

    # Check prefix
    prefix = data.cache["guilds"][str(msgobj.guild.id)]["prefix"]
    if not msgobj.content.startswith(prefix):
        return

    # Parse msgobj
    package = msgobj.content.split(" ")
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

        # Check for this command in list of commands for this module
        if root not in _data.cmd_db[module_name]["cmd"].keys():
            continue

        # Check for this command having permissions defined
        if "level" not in _data.cmd_db[module_name]["cmd"][root].keys():
            await _data.cmd_db[module_name]["eh"](root, aux, query, msgobj)
            continue

        # Check permissions
        level = _data.cmd_db[module_name]["cmd"][root]["level"]

        if isinstance(level, int):
            # Permission is specified as role ranking
            if msgobj.author.guild.owner == msgobj.author:
                role = 0
            else:
                role = len(msgobj.guild.roles) - msgobj.author.top_role.position
            # Highest role = 1, guild owner = 0, everyone = -1

            if level < 0 or role <= level:
                await _data.cmd_db[module_name]["eh"](root, aux, query, msgobj)
            else:
                # TODO permission notification gui
                continue

        elif isinstance(level, str):
            # Permission is specified as specific Discord permission
            if _data.perm_db[level] <= msgobj.channel.permissions_for(msgobj.author):
                await _data.cmd_db[module_name]["eh"](root, aux, query, msgobj)
            else:
                # TODO permission notification gui
                continue

        else:
            # TODO bad perm definition handling
            continue
