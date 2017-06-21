discord_thread = None


def thread_init(statusbar, moduletabs, botconsole):
    print("Loading Modis ...")
    statusbar["text"] = "LOADING"
    statusbar["background"] = "#FFFFBB"
    botconsole.button_stop.state(['!disabled'])
    botconsole.button_start.state(['disabled'])

    import threading
    global discord_thread
    discord_thread = threading.Thread(target=lambda: init(statusbar, moduletabs, botconsole), args=[])
    discord_thread.start()


def stop(statusbar, moduletabs, botconsole):
    print("Stopping...")
    from . import share
    share.runcoro(share.client.logout())

    print("Stopped.")
    for i in range(len(moduletabs.tabs())):
        moduletabs.forget(0)
    import tkinter.ttk as ttk
    moduletabs.add(ttk.Frame(moduletabs), text="No modules loaded")

    statusbar["text"] = "OFFLINE"
    statusbar["background"] = "#FFBBBB"
    botconsole.button_stop.state(['disabled'])
    botconsole.button_start.state(['disabled'])


def init(statusbar=None, moduletabs=None, botconsole=None):
    """Runs the Modis Discord bot"""

    from . import share
    # import asyncio
    # import discord
    # loop = asyncio.new_event_loop()
    # asyncio.set_event_loop(loop)
    # share.client = discord.Client(loop=loop)

    # Import module tabs
    print("    Importing console tabs...")
    if moduletabs:
        moduletabs.forget(0)
        from .console_elements import loading
        moduletabs.add(loading.UI(moduletabs), text="Importing modules")

    if moduletabs:
        console_tabs = get_console_tabs()
        for eh in console_tabs:
            try:
                moduletabs.add(eh.Page(moduletabs), text=eh.pagename)
            except AttributeError:
                # No pipe
                pass
        moduletabs.forget(0)

    # Import event handlers
    print("    Importing event handlers...")

    event_handlers = get_event_handlers()

    print("    Loaded.")

    # Define event handlers
    @share.client.event
    async def on_ready():
        """Runs some initialisation and runs on_ready() event handlers"""

        if statusbar:
            statusbar["text"] = "ONLINE"
            statusbar["background"] = "#BBFFBB"

        for eh in event_handlers["on_ready"]:
            await eh.on_ready()

    @share.client.event
    async def on_message(message):
        """Runs on_message() event handlers

        Args:
            message (discord.Message): The message received by the bot
        """

        # Run the on_message() event handler for all modules that have it
        for eh in event_handlers["on_message"]:
            await eh.on_message(message)

    @share.client.event
    async def on_reaction_add(reaction, user):
        """Runs on_reaction_add() event handlers

        Args:
            reaction (discord.Reaction): The reaction that was added
            user (discord.User): The user that sent the reaction
        """

        # Run the on_reaction_add() event handler for all modules that have it
        for eh in event_handlers["on_reaction_add"]:
            await eh.on_reaction_add(reaction, user)

    @share.client.event
    async def on_error(event_method, *args, **kwargs):
        """Prints the error that happened and runs on_error() event handlers

        Args:
            event_method:
            *args:
            **kwargs:
        """

        # Run the on_error() event handler for all modules that have it
        for eh in event_handlers["on_error"]:
            await eh.on_error(event_method, *args, **kwargs)

    # Start the discord client
    if statusbar:
        statusbar["text"] = "CONNECTING"
        statusbar["background"] = "#BBFFFF"
    print("Connecting to Discord...")
    share.client.run(share.apikeys["discord"])


def get_event_handlers():
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
    module_database_dir = "{}\\module_database".format(os.path.dirname(os.path.realpath(__file__)))

    for module_name in os.listdir(module_database_dir):
        module_dir = "{}\\{}".format(module_database_dir, module_name)

        # Iterate through files in module
        if os.path.isdir(module_dir) and not module_name.startswith("_"):
            print("        Importing {} event handler...".format(module_name))

            # Add all defined event handlers in module files
            module_event_handlers = os.listdir(module_dir)

            if "on_ready.py" in module_event_handlers:
                event_handlers["on_ready"].append(importlib.import_module(".module_database.{}.on_ready".format(module_name), "modis"))

            if "on_message.py" in module_event_handlers:
                event_handlers["on_message"].append(importlib.import_module(".module_database.{}.on_message".format(module_name), "modis"))

            if "on_reaction_add.py" in module_event_handlers:
                event_handlers["on_reaction_add"].append(importlib.import_module(".module_database.{}.on_reaction_add".format(module_name), "modis"))

            if "on_error.py" in module_event_handlers:
                event_handlers["on_error"].append(importlib.import_module(".module_database.{}.on_error".format(module_name), "modis"))

            print("            Import successfull.".format(module_name))

    return event_handlers


def get_console_tabs():
    """Gets dictionary of event handlers and the modules that define them

    Returns:
        window_tabs (list):
    """

    import os
    import importlib

    console_tabs = []

    # Iterate through module folders
    module_database_dir = "{}\\module_database".format(os.path.dirname(os.path.realpath(__file__)))

    for module_name in os.listdir(module_database_dir):
        module_dir = "{}\\{}".format(module_database_dir, module_name)

        # Iterate through files in module
        if os.path.isdir(module_dir) and not module_name.startswith("_"):
            print("        Importing {} console tab...".format(module_name))

            # Add all defined event handlers in module files
            module_event_handlers = os.listdir(module_dir)

            if "ui_window.py" in module_event_handlers:
                console_tabs.append(importlib.import_module(".module_database.{}.ui_window".format(module_name), "modis"))

            print("            Import successfull.".format(module_name))

    return console_tabs


def get_required_perms():
    """Returns Discord API Permissions object with all the permissions the modules require

    Returns:
        perms (discord.Permissions): The permissions this bot requires
    """

    import discord

    perms = discord.Permissions()

    perms.add_reactions = True
    perms.read_messages = True
    perms.send_messages = True
    perms.send_tts_messages = True
    perms.manage_messages = True
    perms.connect = True
    perms.speak = True

    return perms
