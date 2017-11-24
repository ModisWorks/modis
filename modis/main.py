"""
This is the hub from which Modis runs all its modules.

start() is called by __init__.py if Modis is running in command line, or by the
start button in the GUI if Modis is running in GUI.

_eh_get() scans the modules folder and returns a dictionary of all the event
handlers in all the modules. _eh_create() then combines all event handlers of
the same type into one, so that they can be registered into the discord.py
client.
"""

import logging

logger = logging.getLogger(__name__)

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


def start(loop):
    """Start the Discord client and log Modis into Discord."""

    import discord
    import asyncio
    
    from modis import cache
    from modis.tools import moduletools

    # TODO data.json setup

    # Create client
    logger.debug("Creating Discord client")
    asyncio.set_event_loop(loop)
    client = discord.Client()
    cache.client = client

    # Import event handlers
    logger.debug("Importing event handlers")
    eh_lib = moduletools.get_files(EH_TYPES)

    # Register event handlers
    logger.debug("Registering event handlers")
    for eh in eh_lib.keys():
        client.event(_eh_create(eh, eh_lib))

    # Run the client loop
    logger.info("Connecting to Discord")
    # TODO clean up this massive exception stack
    try:
        from modis.tools import datatools
        data = datatools.get()
        token = data["keys"]["discord_token"]
        client.loop.run_until_complete(client.login(token))
    except Exception as e:
        logger.exception(e)
        logger.critical("Could not connect to Discord")
    else:
        logger.debug("Running the bot")
        try:
            client.loop.run_until_complete(client.connect())
        except KeyboardInterrupt:
            client.loop.run_until_complete(client.logout())
            pending = asyncio.Task.all_tasks(loop=client.loop)
            gathered = asyncio.gather(*pending, loop=client.loop)
            try:
                gathered.cancel()
                client.loop.run_until_complete(gathered)

                # we want to retrieve any exceptions to make sure that
                # they don't nag us about it being un-retrieved.
                gathered.exception()
            except Exception as e:
                logger.exception(e)
        except Exception as e:
            logger.exception(e)
            pending = asyncio.Task.all_tasks(loop=client.loop)
            gathered = asyncio.gather(*pending, loop=client.loop)
            gathered.exception()
        finally:
            try:
                client.loop.run_until_complete(client.logout())
            except Exception as e:
                logger.exception(e)

            logger.critical("Bot stopped\n")
            client.loop.close()


def _eh_create(eh_type, eh_lib):
    """Create a function that combines all the event handlers of a specific type
    into one.

    Args:
        eh_type (str):
        eh_lib (dict):

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
                logger.error("An error occured in '{}'".format(eh_module))
                logger.exception(e)
    func.__name__ = eh_type
    return func
