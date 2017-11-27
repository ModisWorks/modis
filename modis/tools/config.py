"""
This file can be thought of as a save file. The file itself isn't edited but
contains references to variables in RAM, making it easy for other modules to
access global variables.
"""

import os as _os

# Directory
ROOT_DIR = _os.path.dirname(_os.path.dirname(_os.path.realpath(__file__)))
MODULES_DIR = ROOT_DIR + "/modules"
WORK_DIR = _os.getcwd()
LOGS_DIR = WORK_DIR + "/logs"

# Discord
EH_TYPES = [
    "on_ready",
    "on_resume",
    "on_error",
    "on_message",
    "on_socket_raw_receive",
    "on_socket_raw_send",
    "on_message_delete",
    "on_message_edit",
    "on_reaction_add",
    "on_reaction_remove",
    "on_reaction_clear",
    "on_channel_delete",
    "on_channel_create",
    "on_channel_update",
    "on_member_join",
    "on_member_remove",
    "on_member_update",
    "on_server_join",
    "on_server_remove",
    "on_server_update",
    "on_server_role_create",
    "on_server_role_delete",
    "on_server_role_update",
    "on_server_emojis_update",
    "on_server_available",
    "on_server_unavailable",
    "on_voice_state_update",
    "on_member_ban",
    "on_member_unban",
    "on_typing",
    "on_group_join",
    "on_group_remove"
]

# data.json
DATAFILE = "{}/data.json".format(WORK_DIR)
ROOT_TEMPLATE = {
    "log_level": "INFO",
    "keys": {
        "discord_token": ""
    },
    "servers": {}
}
SERVER_TEMPLATE = {
    "prefix": "!",
    "activation": {},
    "commands": {}
}

# Logging
LOG_FORMAT = "{asctime} {levelname:8} {name} - {message}"
