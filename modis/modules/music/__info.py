NAME = "music"
CONTRIBUTORS = {
    "@Infraxion": "Original module",
    "@YtnomSnrub": "Extended playback controls, GUI enhancements, SoundCloud support, stability",
    "@Disputes": "Spotify support"
}
BLURB = "Modis' flagship module - a music player featuring a live-updating GUI with a progress bar, queue display, and more. The GUI also has working media buttons for easy control without needing to know any commands. The player supports songs and playlists for YouTube, Spotify, and SoundCloud, and can play most online audio sources."

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
    },
}
DATA_SERVER = {
    "topic_id": "",
    "volume": 20
}
DATA_GLOBAL = {}

HELP_DATAPACKS = {
    "Play Commands": [{
        "name": "play",
        "params": ["query/link"],
        "description": "Starts playing the first result of the query or link, or adds it to the end of the queue if something is already playing"
    }, {
        "name": "playnow",
        "params": ["query/link"],
        "description": "Stops playing the current song and starts playing the first result of the query or link"
    }, {
        "name": "playnext",
        "params": ["query/link"],
        "description": "Starts playing the first result of the query or link after the current song has finished"
    }, {
        "name": "playshuffle",
        "params": ["query/link"],
        "description": "Plays the first result of the query or link in a random order"
    }, {
        "name": "insert",
        "params": ["index", "query/link"],
        "description": "Adds the first result of the query of link at the given index"
    }],
    "Music Player Commands": [{
        "name": "pause",
        "description": "Pauses the currently playing song"
    }, {
        "name": "resume",
        "description": "Resumes the currently playing song"
    }, {
        "name": "shuffle",
        "description": "Randomly shuffles the remaining songs in the queue"
    }, {
        "name": "skip",
        "params": ["n"],
        "description": "Skips [n] songs"
    }, {
        "name": "rewind",
        "params": ["n"],
        "description": "Rewinds the queue [n] songs"
    }, {
        "name": "remove",
        "params": ["index"],
        "description": "Removes the song from the queue at [index], you can remove a range of songs by giving the index in the form #-#"
    }, {
        "name": "volume",
        "params": ["v"],
        "description": "Sets the volume to [v]% (must be between 0% and 200%)"
    }, {
        "name": "stop",
        "description": "Stops the currently playing song, clears the queue, and disconnects from voice"
    }, {
        "name": "destroy",
        "description": "Stops and removes the music player"
    }],
    "SoundCloud Commands": [{
        "name": "play sc",
        "params": ["query"],
        "description": "Searches SoundCloud using the query and plays the first song"
    }, {
        "name": "play sc song",
        "params": ["query"],
        "description": "Searches SoundCloud using the query and plays the first song"
    }, {
        "name": "play sc songs",
        "params": ["query"],
        "description": "Searches SoundCloud using the query and plays the top songs that match the query"
    }, {
        "name": "play sc user",
        "params": ["query"],
        "description": "Searches SoundCloud for a user and plays their most recent songs"
    }, {
        "name": "play sc playlist",
        "params": ["query"],
        "description": "Searches SoundCloud for a playlist and queues songs from the first result"
    }, {
        "name": "play sc tagged",
        "params": ["query"],
        "description": "Searches SoundCloud for songs with a given tag and plays the top songs with that tag"
    }, {
        "name": "play sc genre",
        "params": ["query"],
        "description": "Searches SoundCloud for songs with a given genre and plays the top songs with that genre"
    }],
    "Utility Commands": [{
        "name": "loop",
        "params": ["off/on/shuffle"],
        "description": "Sets the loop state for this session: 'off' will stop looping, 'on' will loop everything played this session when the queue finishes, 'shuffle' will shuffle before looping"
    }, {
        "name": "settopic",
        "description": "Sets Modis to update this channel's topic with the currently playing song"
    }, {
        "name": "cleartopic",
        "description": "Stops Modis from updating this channel's topic with the currently playing song"
    }, {
        "name": "movehere",
        "description": "Moves the music player to the front of the channel the command was sent from"
    }]
}
HELP_MARKDOWN = """"""
