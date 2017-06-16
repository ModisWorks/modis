discord_thread = None


def thread_init(statusbar, moduletabs, botconsole):
    print("Starting...")
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

    import asyncio
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    share.client = share.discord.Client()

    print("Stopped.")
    for i in range(len(moduletabs.tabs())):
        moduletabs.forget(0)
    import tkinter.ttk as ttk
    moduletabs.add(ttk.Frame(moduletabs), text="No modules loaded")

    statusbar["text"] = "OFFLINE"
    statusbar["background"] = "#FFBBBB"
    botconsole.button_stop.state(['disabled'])
    botconsole.button_start.state(['!disabled'])


def init(statusbar=None, moduletabs=None, botconsole=None):
    """Runs the Modis Discord bot"""

    import discord
    from . import share

    # Import modules
    print("Importing modules...")
    if moduletabs:
        moduletabs.forget(0)
        from .console_elements import loading
        moduletabs.add(loading.UI(moduletabs), text="Importing modules")

    from . import module_database

    # Initialise module tabs
    if moduletabs:
        for eh in module_database.event_handlers["ui_window"]:
            try:
                moduletabs.add(eh.Page(moduletabs), text=eh.pagename)
            except AttributeError:
                # No pipe
                pass
        moduletabs.forget(0)

    # Define event handlers
    @share.client.event
    async def on_ready():
        """Runs some initialisation and runs on_ready() event handlers"""

        if statusbar:
            statusbar["text"] = "ONLINE"
            statusbar["background"] = "#BBFFBB"
        print("Ready.\n"
              + "---\n"
              + "To add this bot to a server, use this link:\n"
              + "{}\n".format(discord.utils.oauth_url(share.client_id))
              + "---")

        # Set the game Modis is playing
        if share.game:
            await share.client.change_presence(
                game=discord.Game(
                    name=share.game,
                    url="https://infraxion.github.io/modis/",
                    type=0),
                status=discord.Status.online,
                afk=False)

        for eh in module_database.event_handlers["on_ready"]:
            await eh.on_ready()

    @share.client.event
    async def on_message(message):
        """Runs on_message() event handlers

        Args:
            message (discord.Message): The message received by the bot
        """

        # Add the server to serverdata if it doesn't yet exist
        _sd = share.get_serverdata()
        if message.server.id not in _sd:
            _sd[message.server.id] = {
                "prefix": share.prefix
            }
            share.write_serverdata(_sd)

        # Run the on_message() event handler for all modules that have it
        for eh in module_database.event_handlers["on_message"]:
            await eh.on_message(message)

    @share.client.event
    async def on_reaction_add(reaction, user):
        """Runs on_reaction_add() event handlers

        Args:
            reaction (discord.Reaction): The reaction that was added
            user (discord.User): The user that sent the reaction
        """

        # Add the server to serverdata if it doesn't yet exist
        _sd = share.get_serverdata()
        if reaction.message.server.id not in _sd:
            _sd[reaction.message.server.id] = {
                "prefix": share.prefix
            }
            share.write_serverdata(_sd)

        # Run the on_reaction_add() event handler for all modules that have it
        for eh in module_database.event_handlers["on_reaction_add"]:
            await eh.on_reaction_add(reaction, user)

    import datetime
    import sys
    import traceback

    @share.client.event
    async def on_error(event_method, *args, **kwargs):
        """Prints the error that happened and runs on_error() event handlers

        Args:
            event_method:
            *args:
            **kwargs:
        """

        # Print error prettily
        print("\n"
              + "################################\n"
              + "ERROR\n"
              + str(datetime.datetime.now()).split('.')[0] + "\n"
              + ''.join(traceback.format_exception(sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2]))
              + "################################\n\n")

        # Run the on_error() event handler for all modules that have it
        for eh in module_database.event_handlers["on_error"]:
            await eh.on_error(event_method, *args, **kwargs)

    # Start the discord client
    if statusbar:
        statusbar["text"] = "CONNECTING"
        statusbar["background"] = "#BBFFFF"
    print("Connecting to Discord...")
    share.client.run(share.apikeys["discord"])
