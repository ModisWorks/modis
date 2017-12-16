NAME = "rocketleague"
CONTRIBUTORS = {
    "@Infraxion": "Original module",
    "@YtnomSnrub": "PS4 & XBox support"
}
BLURB = "Looks up your Rocket League rank and stats; currently supported for Steam, XBox, and PS4 players."

COMMANDS = {
    "rlstats": {
        "level": 0,
        "params": {
            "steam": -1,
            "ps4": -1,
            "xbox": -1
        }
    }
}
DATA_SERVER = {}
DATA_GLOBAL = {}

HELP_DATAPACKS = {
    "Commands": [{
        "name": "rlstats",
        "params": ["userid"],
        "description": "Displays the stats for the given Steam user"
    }, {
        "name": "rlstats",
        "params": ["userid", "platform"],
        "description": "Displays the stats for the given user on the specified platform"
    }]
}
HELP_MARKDOWN = """"""
