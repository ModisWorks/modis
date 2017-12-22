from modis.tools import embed


def success(channel, stats, name, platform, dp):
    """Creates an embed UI containing the Rocket League stats

    Args:
        channel (discord.Channel): The Discord channel to bind the embed to
        stats (tuple): Tuples of (field, value, percentile)
        name (str): The name of the player
        platform (str): The playfor to search on, can be 'steam', 'ps', or 'xbox'
        dp (str): URL to the player's dp

    Returns:
        (discord.Embed): The created embed
    """

    # Create datapacks
    datapacks = [("Platform", platform, False)]
    for stat in stats:
        # Add stats
        if stat[0] in ("Duel 1v1", "Doubles 2v2", "Solo Standard 3v3", "Standard 3v3"):
            stat_name = "__" + stat[0] + "__"
            stat_value = "**" + stat[1] + "**"
        else:
            stat_name = stat[0]
            stat_value = stat[1]

        # Add percentile if it exists
        if stat[2]:
            stat_value += " *({})*".format(stat[2])

        datapacks.append((stat_name, stat_value, True))

    # Create embed UI object
    gui = embed.UI(
        channel,
        "Rocket League Stats: {}".format(name),
        "*Stats obtained from [Rocket League Tracker Network]"
        "(https://rocketleague.tracker.network/)*",
        modulename="rocketleague",
        colour=0x0088FF,
        thumbnail=dp,
        datapacks=datapacks
    )

    return gui


def fail_steamid(channel):
    """Creates an embed UI for invalid SteamIDs

    Args:
        channel (discord.Channel): The Discord channel to bind the embed to

    Returns:
        ui (embed.UI): The embed UI object
    """

    gui = embed.UI(
        channel,
        "That SteamID doesn't exist.",
        "You can get your SteamID by going to your profile page and looking at "
        "the url, or you can set a custom ID by going to edit profile on your "
        "profile page.",
        modulename="rocketleague",
        colour=0x0088FF
    )

    return gui


def fail_api(channel):
    """Creates an embed UI for when the API call didn't work

    Args:
        channel (discord.Channel): The Discord channel to bind the embed to

    Returns:
        ui (embed.UI): The embed UI object
    """

    gui = embed.UI(
        channel,
        "Couldn't get stats off RLTrackerNetwork.",
        "Please tell a dev if you're getting this repeatedly.",
        modulename="rocketleague",
        colour=0x0088FF
    )

    return gui
