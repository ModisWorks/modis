# Error reporting
import datetime
import sys
import traceback

# Modis imports
from globalvars import *


# import modis_console.main_console as console
# import threading


def run(client_id=None, game=None, prefix="!"):
    """Runs Modis

    Args:
        client_id (str): The client id of the bot Modis will run on; used to make the invite link
        game (str): The game Modis will be playing; defaults to ""
        prefix (str): The prefix to use for Modis commands; defaults to '!'
    """

    import module_database

    # Start GUI console
    # print("Starting console...")
    # console_thread = threading.Thread(target=console.main, args=[])
    # console_thread.start()
    # console.init(client, "Modis Console")

    @client.event
    async def on_ready():
        """Runs some initialisation and runs on_ready() event handlers"""

        # Print ready message to console
        print("Ready.\n"
              + "---\n"
              + "To add this bot to a server, use this link:\n"
              + "{}\n".format(discord.utils.oauth_url(client_id))
              + "---")

        # Set the game Modis is playing
        if game:
            await client.change_presence(
                game=discord.Game(
                    name=game,
                    url="https://infraxion.github.io/modis/",
                    type=0),
                status=discord.Status.online,
                afk=False)

        for eh in module_database.event_handlers["on_ready"]:
            await eh.on_ready()

    @client.event
    async def on_message(message):
        """Runs on_message() event handlers

        Args:
            message (discord.Message): The message received by the bot
        """

        # Add the server to serverdata if it doesn't yet exist
        _sd = get_serverdata()
        if message.server.id not in _sd:
            _sd[message.server.id] = {
                "prefix": prefix
            }
            write_serverdata(_sd)

        # Run the on_message() event handler for all modules that have it
        for eh in module_database.event_handlers["on_message"]:
            await eh.on_message(message)

    @client.event
    async def on_reaction_add(reaction, user):
        """Runs on_reaction_add() event handlers

        Args:
            reaction (discord.Reaction): The reaction that was added
            user (discord.User): The user that sent the reaction
        """

        # Add the server to serverdata if it doesn't yet exist
        _sd = get_serverdata()
        if reaction.message.server.id not in _sd:
            _sd[reaction.message.server.id] = {
                "prefix": prefix
            }
            write_serverdata(_sd)

        # Run the on_reaction_add() event handler for all modules that have it
        for eh in module_database.event_handlers["on_reaction_add"]:
            await eh.on_reaction_add(reaction, user)

    @client.event
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
    print("Connecting to Discord...")
    client.run(apikeys["discord"])

    import atexit
    atexit.register(runcoro(client.logout))
