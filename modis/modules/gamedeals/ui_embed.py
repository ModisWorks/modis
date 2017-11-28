from modis.tools import embed

from . import _data


def success(channel, post):
    """Creates an embed UI containing the Reddit posts

    Args:
        channel (discord.Channel): The Discord channel to bind the embed to
        post (tuple): Tuples of (field, value, percentile)

    Returns:

    """

    # Create datapacks
    datapacks = [("Game", post[0], True), ("Upvotes", post[2], True)]

    # Create embed UI object
    gui = embed.UI(
        channel,
        "Link",
        post[1],
        modulename=_data.modulename,
        colour=0xFF8800,
        thumbnail=post[1],
        datapacks=datapacks
    )

    return gui


def no_results(channel):
    """Creates an embed UI for when there were no results

    Args:
        channel (discord.Channel): The Discord channel to bind the embed to

    Returns:
        ui (embed.UI): The embed UI object
    """

    gui = embed.UI(
        channel,
        "No results",
        ":c",
        modulename=_data.modulename,
        colour=0xFF8800
    )

    return gui