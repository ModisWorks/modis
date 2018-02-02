"""
This is the hub from which Modis runs all its modules.

start() is called by __init__.py if Modis is running in command line, or by the
start button in the GUI if Modis is running in GUI.

_eh_create() combines multiple event handlers of the same type into one single
function, so that they can be registered into the discord.py client.
"""

import logging

logger = logging.getLogger(__name__)
statuslog = logging.getLogger("globalstatus")

client = None


def start(loop):
    """Start the Discord client and log Modis into Discord."""

    logger.info("Loading Modis...")

    import discord
    import asyncio

    from modis.tools import config, data, moduledb, version

    # Update data.json cache
    data.get()

    # Check the current version
    # logger.info(version.infostr())

    # Create client
    logger.debug("Creating Discord client")
    asyncio.set_event_loop(loop)
    global client
    client = discord.Client()

    # Import event handlers
    logger.debug("Importing event handlers")
    eh_lib = moduledb.get_by_eh(config.EH_TYPES)

    # Register event handlers
    logger.debug("Registering event handlers")
    for eh in eh_lib.keys():
        client.event(_eh_create(eh, eh_lib))

    # Start the bot
    logger.info("Logging in to Discord...")
    try:
        # Login to Discord
        token = data.cache["keys"]["discord_token"]
        client.loop.run_until_complete(client.login(token))
    except Exception as e:
        # Login failed
        logger.info("Could not login to Discord")
        logger.exception(e)
        statuslog.info("3")
    else:
        # Login successful
        logger.debug("Login successful")
        try:
            # Try to reconnect
            logger.debug("Connecting to Discord...")
            client.loop.run_until_complete(client.connect())
        except KeyboardInterrupt:
            # Reconnect cancelled
            logger.warning("Connection cancelled")
            client.loop.run_until_complete(client.logout())

            # Cancel all pending tasks
            pending = asyncio.Task.all_tasks(loop=client.loop)
            gathered = asyncio.gather(*pending, loop=client.loop)
            try:
                gathered.cancel()
                client.loop.run_until_complete(gathered)
                gathered.exception()
            except Exception as e:
                logger.exception(e)
        except Exception as e:
            # Reconnect failed
            logger.error("Connection failed")
            logger.exception(e)
            pending = asyncio.Task.all_tasks(loop=client.loop)
            gathered = asyncio.gather(*pending, loop=client.loop)
            gathered.exception()
    finally:
        # Bot shutdown
        logger.info("Logging out of Discord")
        try:
            client.loop.run_until_complete(client.logout())
        except Exception as e:
            logger.exception(e)

        logger.critical("Bot stopped")
        statuslog.info("0")
        client.loop.close()


def _eh_create(eh_type, eh_lib):
    """Create a function that combines all the event handlers of a specific type
    into one.

    Args:
        eh_type (str): The event handler type to be bundled.
        eh_lib (dict): The library of event handlers to pull from.

    Returns:
        func (function): A combined event handler function consisting of all the
        event handlers in its category.
    """

    async def func(*args, **kwargs):
        for eh_module in eh_lib[eh_type]:
            try:
                module_event_handler_func = getattr(eh_module, eh_type)
                await module_event_handler_func(*args, **kwargs)
            except Exception as e:
                logger.warning("An uncaught error occured in " + eh_module.__name__)
                logger.exception(e)
    func.__name__ = eh_type
    return func
