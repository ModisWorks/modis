from .._tools import ui_embed
from ._data import *


def success(channel, title, datapacks):
    """Creates an embed UI containing the Rocket League stats

    Args:
        channel (discord.Channel): The Discord channel to bind the embed to
        title (str): The title of the embed
        datapacks (list): The hex value

    Returns:
        embed: The sent embed
    """

    # Create embed UI object
    gui = ui_embed.UI(
        channel,
        title,
        "",
        modulename=modulename,
        creator=creator,
        datapacks=datapacks
    )

    return gui
