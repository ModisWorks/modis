def start(token, loop):
    import discord
    import asyncio

    asyncio.set_event_loop(loop)
    client = discord.Client(loop=loop)

    event_handlers = _get_event_handlers()

    # Define event handlers
    @client.event
    async def on_ready():
        for eh in event_handlers["on_ready"]:
            await eh.on_ready()

    @client.event
    async def on_message(message):
        for eh in event_handlers["on_message"]:
            await eh.on_message(message)

    @client.event
    async def on_reaction_add(reaction, user):
        for eh in event_handlers["on_reaction_add"]:
            await eh.on_reaction_add(reaction, user)

    @client.event
    async def on_error(event_method, *args, **kwargs):
        for eh in event_handlers["on_error"]:
            await eh.on_error(event_method, *args, **kwargs)

    # Register the client in cache
    from . import _client
    _client.client = client

    # Start the discord client
    client.run(token)


def _get_event_handlers():
    """Gets dictionary of event handlers and the modules that define them

    Returns:
        event_handlers (dict): Contains "all", "on_ready", "on_message", "on_reaction_add", "on_error"
    """

    import os
    import importlib

    event_handlers = {
        "on_ready": [],
        "on_message": [],
        "on_reaction_add": [],
        "on_error": [],
        "ui_window": []
    }

    # Iterate through module folders
    module_database_dir = "{}\\modules".format(os.path.dirname(os.path.realpath(__file__)))
    for module_name in os.listdir(module_database_dir):
        module_dir = "{}\\{}".format(module_database_dir, module_name)

        # Iterate through files in module
        if os.path.isdir(module_dir) and not module_name.startswith("_"):

            # Add all defined event handlers in module files
            module_event_handlers = os.listdir(module_dir)

            if "on_ready.py" in module_event_handlers:
                event_handlers["on_ready"].append(importlib.import_module(".discord_modis.modules.{}.on_ready".format(module_name), "modis"))

            if "on_message.py" in module_event_handlers:
                event_handlers["on_message"].append(importlib.import_module(".discord_modis.modules.{}.on_message".format(module_name), "modis"))

            if "on_reaction_add.py" in module_event_handlers:
                event_handlers["on_reaction_add"].append(importlib.import_module(".discord_modis.modules.{}.on_reaction_add".format(module_name), "modis"))

            if "on_error.py" in module_event_handlers:
                event_handlers["on_error"].append(importlib.import_module(".discord_modis.modules.{}.on_error".format(module_name), "modis"))

    return event_handlers
