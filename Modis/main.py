def thread_init():
    import threading
    console_thread = threading.Thread(target=init, args=[])
    console_thread.start()


def init():
    """Runs the Modis Discord bot"""

    import discord
    import share

    # Import modules
    share.tkstatus.set("Modis is starting")
    print("Importing modules")
    share.moduletabs.forget(0)
    import console_elements.loading
    share.moduletabs.add(console_elements.loading.UI(share.moduletabs), text="Importing modules")

    import module_database

    for eh in module_database.event_handlers["ui_window"]:
        share.moduletabs.add(eh.Page(share.moduletabs), text=eh.pagename)
    share.moduletabs.forget(0)

    # Define event handlers
    @share.client.event
    async def on_ready():
        """Runs some initialisation and runs on_ready() event handlers"""

        share.tkstatus.set("Modis is online")
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
    share.tkstatus.set("Modis is connecting")
    print("Connecting to Discord...")
    share.client.run(share.apikeys["discord"])
