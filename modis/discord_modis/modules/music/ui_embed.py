"""UI Embed generator for music module"""

import logging
import math

from ._data import *
from .._tools import ui_embed

logger = logging.getLogger(__name__)


def topic_update(channel, topic_channel):
    """
    Creates an embed UI for the topic update

    Args:
        channel (discord.Channel): The Discord channel to bind the embed to
        topic_channel: The new topic channel

    Returns:
        embed: The created embed
    """

    if topic_channel is not None:
        try:
            channel_message = "Topic channel is now `{}`.".format(topic_channel.name)
        except Exception as e:
            logger.exception(e)
            channel_message = "Topic channel has been updated."
    else:
        channel_message = "Topic channel has been cleared."

    # Create embed UI object
    gui = ui_embed.UI(
        channel,
        "Topic channel updated",
        channel_message,
        modulename=modulename,
        colour=modulecolor_info,
        creator=creator
    )

    return gui


def error_message(channel, error_title, error_message):
    """
    Creates an embed UI for the topic update

    Args:
        channel (discord.Channel): The Discord channel to bind the embed to
        error_title: The title for the error
        error_message: The message for the error

    Returns:
        embed: The created embed
    """

    # Create embed UI object
    gui = ui_embed.UI(
        channel,
        error_title,
        error_message,
        modulename=modulename,
        colour=modulecolor_error,
        creator=creator
    )

    return gui
