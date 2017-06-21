import requests as _requests
import json as _json


def check_rank(player):
    """Gets the Rocket League stats and name and dp of a SteamID

    Args:
        player (str): The SteamID of the player we want to rank check

    Returns:
        success (bool): Whether the rank check was successful
        package (tuple): If successful, the retrieved stats, in order (stats, name, dp)
    """

    # Get player ID and name Rocket League Tracker Network
    webpage = _requests.get(
        "https://rocketleague.tracker.network/profile/steam/{}".format(player)
    ).text

    try:
        # Get player SteamID
        steamid_index = webpage.index("/profile/mmr/steam/") + len("/profile/mmr/steam/")
        steamid_end_index = webpage.index("""">""", steamid_index)
        steamid = webpage[steamid_index:steamid_end_index]

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
    livedata = _json.loads(
        _requests.post(
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

    # Get player dp from steam (CURRENTLY DISABLED; EXCESSIVE LOAD)
    # try:
    #     int(player)
    # except ValueError:
    #     response = _requests.get('http://steamcommunity.com/id/{}'.format(player))
    # else:
    #     response = _requests.get('http://steamcommunity.com/profile/{}'.format(player))
    # parsed = _html.parse(_io.StringIO(response.text)).getroot()
    # try:
    #     dp = parsed[0][29].attrib['href']
    # except (IndexError, KeyError):
    #     dp = 'https://rocketleague.media.zestyio.com/' \
    #          'rocket-league-logos-vr-white.f1cb27a519bdb5b6ed34049a5b86e317.png'
    dp = 'https://rocketleague.media.zestyio.com/' \
         'rocket-league-logos-vr-white.f1cb27a519bdb5b6ed34049a5b86e317.png'

    return True, (stats, name, dp)
