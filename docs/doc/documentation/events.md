---
title: Events
permalink: /documentation/events/
---
# Discord Events

Modis looks for files in a module with these names. They are called when a Discord event occurs.

These files and their actions are the same as the [Discord.py Events](https://discordpy.readthedocs.io/en/v0.16.7/api.html#event-reference), with .py added to the end (for example to listen for messages, `on_message` becomes `on_message.py`). Modis then calls the function with the same name in that file.

## Events List

The events supported by Modis are:

- `on_ready`
- `on_resume`
- `on_error`
- `on_message`
- `on_socket_raw_receive`
- `on_socket_raw_send`
- `on_message_delete`
- `on_message_edit`
- `on_reaction_add`
- `on_reaction_remove`
- `on_reaction_clear`
- `on_channel_delete`
- `on_channel_create`
- `on_channel_update`
- `on_member_join`
- `on_member_remove`
- `on_member_update`
- `on_server_join`
- `on_server_remove`
- `on_server_update`
- `on_server_role_create`
- `on_server_role_delete`
- `on_server_role_update`
- `on_server_emojis_update`
- `on_server_available`
- `on_server_unavailable`
- `on_voice_state_update`
- `on_member_ban`
- `on_member_unban`
- `on_typing`
- `on_group_join`
- `on_group_remove`
