from ._data import *
from .._tools import ui_embed


def success(channel, image, hex_str):
    """
    Creates an embed UI containing a hex color message

    Args:
        channel (discord.Channel): The Discord channel to bind the embed to
        image (str): The url of the image to add
        hex_str (str): The hex value

    Returns:
        ui (ui_embed.UI): The embed UI object that was created
    """

    hex_number = int(hex_str, 16)

    # Create embed UI object
    gui = ui_embed.UI(
        channel,
        "",
        "#{}".format(hex_str),
        modulename=modulename,
        creator=creator,
        colour=hex_number,
        thumbnail=image,
    )

    return gui


def fail_api(channel):
    """
    Creates an embed UI for when the API call didn't work

    Args:
        channel (discord.Channel): The Discord channel to bind the embed to

    Returns:
        ui (ui_embed.UI): The embed UI object
    """

    gui = ui_embed.UI(
        channel,
        "Invalid value",
        "Hex values must be 3 or 6 characters long, " +
        "and must start with '#' or '0x'.",
        modulename=modulename,
        creator=creator,
        colour=0x555555,
    )

    return gui
