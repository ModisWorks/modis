from modis.tools import embed
from ._data import *


def modify_module(channel, module_name, module_state):
    """
    Creates an embed UI containing the module modified message

    Args:
        channel (discord.Channel): The Discord channel to bind the embed to
        module_name (str): The name of the module that was updated
        module_state (bool): The current state of the module

    Returns:
        embed: The created embed
    """

    # Create embed UI object
    gui = embed.UI(
        channel,
        "{} updated".format(module_name),
        "{} is now {}".format(module_name, "activated" if module_state else "deactivated"),
        modulename=modulename,
        creator=creator
    )

    return gui


def modify_prefix(channel, new_prefix):
    """
    Creates an embed UI containing the prefix modified message

    Args:
        channel (discord.Channel): The Discord channel to bind the embed to
        new_prefix (str): The value of the new prefix

    Returns:
        embed: The created embed
    """

    # Create embed UI object
    gui = embed.UI(
        channel,
        "Prefix updated",
        "Modis prefix is now '{}'".format(new_prefix),
        modulename=modulename,
        creator=creator
    )

    return gui


def error(channel, title, description):
    """
    Creates an embed UI containing an error message

    Args:
        channel (discord.Channel): The Discord channel to bind the embed to
        title (str): The title of the embed
        description (str): The description for the error

    Returns:
        ui (embed.UI): The embed UI object
    """

    # Create embed UI object
    gui = embed.UI(
        channel,
        title,
        description,
        modulename=modulename,
        creator=creator
    )

    return gui
