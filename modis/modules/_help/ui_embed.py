from modis.tools import embed
from ._data import *


def success(channel, title, datapacks):
    """
    Creates an embed UI containing the help message

    Args:
        channel (discord.Channel): The Discord channel to bind the embed to
        title (str): The title of the embed
        datapacks (list): The hex value

    Returns:
        ui (embed.UI): The embed UI object
    """

    # Create embed UI object
    gui = embed.UI(
        channel,
        title,
        "",
        modulename=modulename,
        creator=creator,
        datapacks=datapacks
    )

    return gui


def http_exception(channel, title):
    """
    Creates an embed UI containing the 'too long' error message

    Args:
        channel (discord.Channel): The Discord channel to bind the embed to
        title (str): The title of the embed

    Returns:
        ui (embed.UI): The embed UI object
    """

    # Create embed UI object
    gui = embed.UI(
        channel,
        "Too much help",
        "{} is too helpful! Try trimming some of the help messages.".format(title),
        modulename=modulename,
        creator=creator
    )

    return gui
