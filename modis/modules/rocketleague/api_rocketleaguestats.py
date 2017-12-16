import logging
import requests
import json

logger = logging.getLogger(__name__)

LOGO = "https://rocketleague.media.zestyio.com/rocket-league-logos-vr-white.f1cb27a519bdb5b6ed34049a5b86e317.png"


def check_rank(player, platform="steam"):
    """Gets the Rocket League stats and name and dp of a UserID

    Args:
        player (str): The UserID of the player we want to rank check
        platform (str): The platform to check for, can be 'steam', 'ps', or 'xbox'

    Returns:
        success (bool): Whether the rank check was successful
        package (tuple): If successful, the retrieved stats, in order (stats, name, dp)
    """

    # Get player ID and name Rocket League Tracker Network
    logger.debug("HTML GET")
    webpage = requests.get(
        "https://rocketleague.tracker.network/profile/{}/{}".format(platform, player)
    ).text

    try:
        # Get player ID
        playerid_index = webpage.index("/live?ids=") + len("/live?ids=")
        playerid_end_index = webpage.index("""">""", playerid_index)
        playerid = webpage[playerid_index:playerid_end_index]

        # Get player name
        name_index = webpage.index("Stats Profile : ") + len("Stats Profile : ")
        name_end_index = webpage.index("""\n""", name_index)
        name = webpage[name_index:name_end_index]
    except (ValueError, IndexError):
        return False, ()

    # Get player stats from Rocket League Tracker Network
    logger.debug("HTML POST")
    livedata = json.loads(
        requests.post(
            "https://rocketleague.tracker.network/live/data",
            json={"playerIds": [playerid]}
        ).text
    )

    stats = []
    try:
        for statpack in livedata['players'][0]['Stats']:
            field = statpack['Value']['Label']
            value = str(statpack['Value']['DisplayValue'])
            if statpack['Value']['Percentile']:
                percentile = str(statpack['Value']['Percentile'])
                stats.append((field, value, "Top {}%".format(percentile)))
            else:
                rank = str(statpack['Other']['subtitle'])
                division = str(statpack['Other']['subtitle2'])
                winstreak = statpack['Other']['winstreak']
                if winstreak >= 0:
                    winstreak = str(winstreak) + " game winning streak"
                else:
                    winstreak = str(-winstreak) + " game losing streak"
                stats.append((field, "{} - MMR {}".format(rank, value), "{}, {}".format(division, winstreak)))
    except (IndexError, KeyError):
        return False, ()

    dp = LOGO

    platform_display = platform
    if platform == "steam":
        platform_display = "Steam"
    elif platform == "ps":
        platform_display = "PlayStation"
    elif platform == "xbox":
        platform_display = "Xbox"

    return True, (stats, name, platform_display, dp)
