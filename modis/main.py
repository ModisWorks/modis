"""MAIN.PY - THE HUB

This is the hub from which Modis runs all its modules.

start() is called by __init__.py if Modis is running in command line, or by the start button in the GUI if Modis is running in GUI.

start() will then import all the event handlers of all the modules, and use _eh_create() to compile all event handlers of one type into one function. After that's done, it will add those compiled event handlers to the `client` object, and then log in to Discord.

Thats it! Whenever an event is triggered on the client object, it will now be sent to all modules that have an event handler for that specific event.
"""

import logging
import asyncio
import discord

logger = logging.getLogger(__name__)
statuslog = logging.getLogger("globalstatus")


# Create the client object
client: discord.AutoShardedClient = None
"""In Discord.py 1.0+, the client object is used for global Discord stuff, like listing guilds you're part of etc.
To use it, do `from modis import main`, and then use `main.client`.
"""


def start(loop: asyncio.AbstractEventLoop) -> None:
    """Starts the Discord client and logs Modis into Discord.

    Args:
        loop (asyncio.AbstractEventLoop): An asyncio event loop for the bot to run on.
    """

    logger.info("Loading Modis...")

    from modis.tools import config, data, moduledb, version

    # Update data.json cache
    data.pull()

    # Check the current version
    # TODO implement version check and display
    # logger.info(version.infostr())

    # Create client
    logger.debug("Creating Discord client")
    asyncio.set_event_loop(loop)
    global client
    client = discord.AutoShardedClient()

    # Import event handlers
    logger.info("Importing modules...")
    eh_lib = moduledb.get_imports(config.EH_TYPES)

    # Register event handlers
    logger.debug("Registering event handlers")
    for eh_type in config.EH_TYPES:
        eh_list = []
        for module_name in eh_lib.keys():
            if eh_type in eh_lib[module_name].keys():
                eh_list.append(eh_lib[module_name][eh_type])
        if eh_list:
            client.event(_eh_create(eh_type, eh_list))

    # CONNECTION STACK
    logger.info("Logging in...")
    try:
        # Attempt login
        token = data.cache["keys"]["discord_token"]
        client.loop.run_until_complete(client.login(token))
    except Exception as e:
        # Login failed
        logger.critical("Login failed")
        logger.exception(e)
        statuslog.info("3")
        client.loop.close()
    else:
        # Login successful
        logger.info("Connecting...")
        client.loop.run_until_complete(client.connect(reconnect=True))


def _eh_create(eh_type: str, eh_list: list) -> staticmethod:
    """Creates a compiled event handler

    Creates a function that combines all the event handlers of a specific type into one.

    Args:
        eh_type (str): The event handler type to be bundled.
        eh_list (list): The library of event handlers to pull from.

    Returns:
        func (staticmethod) A combined event handler function consisting of all the event handlers in its category.
    """

    # Create the combiner function
    async def func(*args, **kwargs) -> None:
        """A function that executes a specific event handler in all modules"""
        for eh in eh_list:
            try:
                module_event_handler_func = getattr(eh, eh_type)
                await module_event_handler_func(*args, **kwargs)
            except Exception as e:
                logger.warning("An uncaught error occured in " + eh.__name__)
                logger.exception(e)

    # Rename the combiner function to the name of the event handler
    func.__name__ = eh_type

    return func
