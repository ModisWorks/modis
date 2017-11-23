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
        creator=creator
    )

    return gui


def nowplaying_none(channel):
    """
    Creates an embed UI for no song playing

    Args:
        channel (discord.Channel): The Discord channel to bind the embed to

    Returns:
        embed: The created embed
    """
    # Create embed UI object
    gui = ui_embed.UI(
        channel,
        "Music",
        "Nothing is playing right now",
        modulename=modulename,
        creator=creator
    )

    return gui


def nowplaying_info(channel, title, duration, source, source_date, views=0, likes=0, description=""):
    """
    Creates an embed UI for no song playing

    Args:
        channel (discord.Channel): The Discord channel to bind the embed to
        title (str): The title of the current song
        duration (str): The duration string for the current song
        source (str): The uploader for this song
        source_date (datetime.date): The date that this song was uploaded
        views (int): The number of views for this video
        likes (int): The number of likes for this video
        description (str): The description for the current video

    Returns:
        embed: The created embed
    """

    format_date = source_date.strftime("%d %b, %Y")
    datapacks = [("Now Playing", title, False)]

    if description is not None and description != "":
        datapacks.append(("Description", description, False))

    datapacks.append(("Duration", duration, True))
    datapacks.append(("Author", source, True))
    datapacks.append(("Date", format_date, True))

    if views is not None and views > 0:
        datapacks.append(("Views", number_format(views), True))
    if likes is not None and likes > 0:
        datapacks.append(("Likes", number_format(likes), True))

    # Create embed UI object
    gui = ui_embed.UI(
        channel,
        "",
        "",
        datapacks=datapacks,
        modulename=modulename,
        creator=creator
    )

    return gui


def number_format(n):
    number_names = ['', ' Thousand', ' Million', ' Billion', ' Trillion']

    n = float(n)
    millidx = max(0, min(len(number_names) - 1, int(math.floor(0 if n == 0 else math.log10(abs(n)) / 3))))

    return '{:.0f}{}'.format(n / 10 ** (3 * millidx), number_names[millidx])
