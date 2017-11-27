import discord

from .._tools import ui_embed
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
        modulename=modulename
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
        "Modis prefix is now `{}`".format(new_prefix),
        modulename=modulename
    )

    return gui


def user_warning(channel, user, warnings, max_warnings):
    """
    Creates an embed UI containing an user warning message

    Args:
        channel (discord.Channel): The Discord channel to bind the embed to
        user (discord.User): The user to warn
        warnings (str): The warnings for the user
        max_warnings (str): The maximum warnings for the user

    Returns:
        ui (ui_embed.UI): The embed UI object
    """

    username = user.name
    if isinstance(user, discord.Member):
        if user.nick is not None:
            username = user.nick

    warning_count_text = "warnings" if warnings != 1 else "warning"
    warning_text = "{} {}".format(warnings, warning_count_text)
    result_text = "at {} you will be banned".format(max_warnings)
    if warnings >= max_warnings:
        result_text = "you are being banned because you have more than the maximum warnings"

    # Create embed UI object
    gui = ui_embed.UI(
        channel,
        "Warning {}".format(username),
        "You now have {} {}, {}".format(warning_text, username, result_text),
        modulename=modulename
    )

    return gui


def user_ban(channel, user):
    """
    Creates an embed UI containing an user warning message

    Args:
        channel (discord.Channel): The Discord channel to bind the embed to
        user (discord.User): The user to ban

    Returns:
        ui (ui_embed.UI): The embed UI object
    """

    username = user.name
    if isinstance(user, discord.Member):
        if user.nick is not None:
            username = user.nick

    # Create embed UI object
    gui = ui_embed.UI(
        channel,
        "Banned {}".format(username),
        "{} has been banned from this server".format(username),
        modulename=modulename
    )

    return gui


def warning_max_changed(channel, max_warnings):
    """
    Creates an embed UI containing an error message

    Args:
        channel (discord.Channel): The Discord channel to bind the embed to
        max_warnings (int): The new maximum warnings

    Returns:
        ui (ui_embed.UI): The embed UI object
    """

    # Create embed UI object
    gui = ui_embed.UI(
        channel,
        "Maximum Warnings Changed",
        "Users must now have {} warnings to be banned "
        "(this won't ban existing users with warnings)".format(max_warnings),
        modulename=modulename
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
        modulename=modulename
    )

    return gui
