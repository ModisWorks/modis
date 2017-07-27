from .._tools import ui_embed
from ._data import *


def success(channel, post):
    """Creates an embed UI containing the Reddit posts

    Args:
        channel (discord.Channel): The Discord channel to bind the embed to
        post (tuple): Tuples of (field, value, percentile)

    Returns:

    """

    # Create datapacks
    datapacks = [("Upvotes", post[2], True)]

    # Create embed UI object
    gui = ui_embed.UI(
        channel,
        post[0],
        post[1],
        modulename=modulename,
        creator=creator,
        colour=0xFF4444,
        thumbnail=post[3],
        datapacks=datapacks
    )

    return gui


def no_results(channel):
    """Creates an embed UI for when there were no results

    Args:
        channel (discord.Channel): The Discord channel to bind the embed to

    Returns:
        ui (ui_embed.UI): The embed UI object
    """

    gui = ui_embed.UI(
        channel,
        "No results",
        ":c",
        modulename=modulename,
        creator=creator,
        colour=0xFF4444
    )

    return gui
