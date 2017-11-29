NAME = "music"
CONTRIBUTORS = {
    "@Infraxion": "Original module",
    "@YtnomSnrub": "Extended playback controls, GUI enhancements, SoundCloud support, stability",
    "@Disputes": "Spotify support"
}
BLURB = """
Modis' flagship module - a music player featuring a live-updating GUI with a 
progress bar, queue display, and more. The GUI also has working media buttons 
for easy control without needing to know any commands. The player supports 
songs and playlists for YouTube, Spotify, and SoundCloud, and can play most 
online audio sources.
"""

COMMANDS = {
    "play": {
        "level": 0,
        "params": {
            "now": -1,
            "next": -1,
            "shuffle": -1,
            "yt": -1,
            "sc": -1,
            "sp": -1
        }
    },
    "insert": {
        "level": 0,
        "params": {
            "#INT": -1
        }
    },
    "pause": {
        "level": 0
    },
    "resume": {
        "level": 0
    },
    "shuffle": {
        "level": 0
    },
    "skip": {
        "level": 0
    },
    "rewind": {
        "level": 0
    },
    "remove": {
        "level": 0
    },
    "volume": {
        "level": 0
    },
    "stop": {
        "level": 0
    },
    "destroy": {
        "level": 0
    },
    "loop": {
        "level": 0,
        "params": {
            "on": -1,
            "off": -1,
            "shuffle": -1
        }
    },
    "topic": {
        "level": 0,
        "params": {
            "on": -1,
            "off": -1
        }
    },
    "front": {
        "level": 0
    }
}

HELP_DATAPACKS = {}

HELP_MARKDOWN = """"""
