NAME = "manager"
CONTRIBUTORS = {
    "@YtnomSnrub": "Original module"
}
BLURB = "Provides essential server management tools for server owners, such as activating and deactivating modules, changing the command prefix, and various moderation tools."

COMMANDS = {
    "activate": {
        "level": 0
    },
    "deactivate": {
        "level": 0
    },
    "warn": {
        "level": 0
    },
    "ban": {
        "level": 0
    },
    "warnmax": {
        "level": 0
    },
    "prefix": {
        "level": 0
    }
}

HELP_DATAPACKS = {
    "Commands": [{
        "name": "activate",
        "params": ["module"],
        "description": "Activates the given module for this server"
    }, {
        "name": "deactivate",
        "params": ["module"],
        "description": "Deactivates the given module for this server"
    }, {
        "name": "warn",
        "params": ["mention"],
        "description": "Gives a warning to the mentioned user"
    }, {
        "name": "ban",
        "params": ["mention"],
        "description": "Bans the mentioned user from the server"
    }, {
        "name": "warnmax",
        "params": ["n"],
        "description": "Sets the number of warnings a user must have before being banned to [n]"
    }, {
        "name": "prefix",
        "params": ["prefix"],
        "description": "Updates the prefix for the server"
    }]
}

HELP_MARKDOWN = """"""
