"""Handles the timebar, edit this for custom time bars"""
from modis.discord_modis.modules.music import api_music

TIMEBAR_LENGTH = 21
TIMEBAR_PCHAR = "◆"
TIMEBAR_ECHAR = "◇"


def make_timebar(progress=0, duration=0):
    """
    Makes a new time bar string

    Args:
        progress: How far through the current song we are (in seconds)
        duration: The duration of the current song (in seconds)

    Returns:
        timebar (str): The time bar string
    """

    duration_string = api_music.duration_to_string(duration)
    if duration <= 0:
        return "---"

    time_counts = int(round((progress / duration) * TIMEBAR_LENGTH))
    if time_counts > TIMEBAR_LENGTH:
        time_counts = TIMEBAR_LENGTH

    if duration > 0:
        bar = "│" + (TIMEBAR_PCHAR * time_counts) + (TIMEBAR_ECHAR * (TIMEBAR_LENGTH - time_counts)) + "│"
        time_bar = "{} {}".format(bar, duration_string)
    else:
        time_bar = duration_string

    return time_bar
