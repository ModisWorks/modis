---
title: Events
permalink: /documentation/events/
---

# Discord Events
Modis looks for files in a module with these names. They are called when a Discord event occurs.

These files are the same as the [Discord.py Events](https://discordpy.readthedocs.io/en/v0.16.7/api.html#event-reference), with .py added to the end (for example to listen for messages, `on_message` becomes `on_message.py`). Modis then calls the function with the same name in that file.
