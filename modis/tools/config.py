"""THE CONFIGURATION FILE

This file can be thought of as a read-only save file, as opposed to the read-and-write save file that is data.json. This file makes it easy to store global variables for all modules and framework to access.
"""

import os as _os

# About
VERSION = "0.4.0"
NICKNAME = "CHOPIN"

# Directory
ROOT_DIR = _os.path.dirname(_os.path.dirname(_os.path.realpath(__file__)))
WORK_DIR = _os.getcwd()
MODULES_DIR = ROOT_DIR + "/modules"
LOGS_DIR = WORK_DIR + "/logs"

# Discord
EH_TYPES = [
    "on_connect",
    "on_disconnect",
    "on_ready",
    "on_shard_ready",
    "on_resumed",
    "on_error",
    "on_socket_raw_receive",
    "on_socket_raw_send",
    "on_typing",
    "on_message",
    "on_message_delete",
    "on_bulk_message_delete",
    "on_raw_message_delete",
    "on_raw_bulk_message_delete",
    "on_message_edit",
    "on_raw_message_edit",
    "on_reaction_add",
    "on_raw_reaction_add",
    "on_reaction_remove",
    "on_raw_reaction_remove",
    "on_reaction_clear",
    "on_raw_reaction_clear",
    "on_private_channel_delete",
    "on_private_channel_create",
    "on_private_channel_update",
    "on_private_channel_pins_update",
    "on_guild_channel_delete",
    "on_guild_channel_create",
    "on_guild_channel_update",
    "on_guild_channel_pins_update",
    "on_webhooks_update",
    "on_member_join",
    "on_member_remove",
    "on_member_update",
    "on_guild_join",
    "on_guild_remove",
    "on_guild_update",
    "on_guild_role_create",
    "on_guild_role_delete",
    "on_guild_role_update",
    "on_guild_emojis_update",
    "on_guild_available",
    "on_guild_unavailable",
    "on_voice_state_update",
    "on_member_ban",
    "on_member_unban",
    "on_group_join",
    "on_group_remove",
    "on_relationship_add",
    "on_relationship_remove",
    "on_relationship_update"
]

# data.json
DATAFILE = "{}/data.json".format(WORK_DIR)
ROOT_TEMPLATE = {
    "log_level": "INFO",
    "keys": {
        "discord_token": ""
    },
    "guilds": {}
}
GUILD_TEMPLATE = {
    "prefix": "!",
    "activation": {},
    "commands": {},
    "modules": {}
}

# Logging
LOG_FORMAT = "{asctime} {levelname:8} {name} - {message}"
