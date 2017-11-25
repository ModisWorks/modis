import requests
import json


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
            else:
                percentile = None
            stats.append((field, value, percentile))
    except (IndexError, KeyError):
        return False, ()

    dp = "https://rocketleague.media.zestyio.com/rocket-league-logos-vr-white.f1cb27a519bdb5b6ed34049a5b86e317.png"

    platform_display = platform
    if platform == "steam":
        platform_display = "Steam"
    elif platform == "ps":
        platform_display = "PlayStation"
    elif platform == "xbox":
        platform_display = "Xbox"

    return True, (stats, name, platform_display, dp)
