import logging

logger = logging.getLogger(__name__)


def start(token, client_id, loop, module_found_handler=None, on_ready_handler=None):
    """Start the Discord client and log Modis into Discord."""
    import discord
    import asyncio

    # Create client
    logger.debug("Creating Discord client")
    asyncio.set_event_loop(loop)
    client = discord.Client()
    from . import _client
    _client.client = client

    from .. import datatools
    if datatools.has_data():
        data = datatools.get_data()
    else:
        # Create a blank data file
        data = {"discord": {}}

    # Save default server info to data
    if "servers" not in data["discord"]:
        data["discord"]["servers"] = {}

    # Save default key info to data
    if "keys" not in data["discord"]:
        data["discord"]["keys"] = {}

    # Save logger info to data
    if "log_level" not in data:
        data["log_level"] = "INFO"

    data["discord"]["token"] = token
    data["discord"]["client_id"] = client_id
    datatools.write_data(data)

    # Import event handlers
    logger.debug("Importing event handlers")
    event_handlers = _get_event_handlers(module_found_handler)

    # Create event handler combiner
    logger.debug("Compiling event handlers")

    def create_event_handler(event_handler_type):
        async def func(*args, **kwargs):
            for module_event_handler in event_handlers[event_handler_type]:
                # Check for errors in the module event
                try:
                    module_event_handler_func = getattr(module_event_handler,
                                                        event_handler_type)
                    await module_event_handler_func(*args, **kwargs)
                except Exception as e:
                    logger.error("An error occured in '{}'".format(module_event_handler))
                    logger.exception(e)

            if on_ready_handler is not None and event_handler_type == "on_ready":
                await on_ready_handler()

        func.__name__ = event_handler_type
        return func

    # Register event handlers
    logger.debug("Registering event handlers into client")
    for event_handler in event_handlers.keys():
        client.event(create_event_handler(event_handler))

    # Run the client loop
    logger.info("Connecting to Discord")
    try:
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
            except:
                pass
        finally:
            logger.critical("Bot stopped\n")
            client.loop.close()


def _get_event_handlers(module_found_handler):
    """
    Gets dictionary of event handlers and the modules that define them

    Returns:
        event_handlers (dict): Contains "all", "on_ready", "on_message", "on_reaction_add", "on_error"
    """

    import os
    import importlib

    event_handlers = {
        "on_ready": [],
        "on_resume": [],
        "on_error": [],
        "on_message": [],
        "on_socket_raw_receive": [],
        "on_socket_raw_send": [],
        "on_message_delete": [],
        "on_message_edit": [],
        "on_reaction_add": [],
        "on_reaction_remove": [],
        "on_reaction_clear": [],
        "on_channel_delete": [],
        "on_channel_create": [],
        "on_channel_update": [],
        "on_member_join": [],
        "on_member_remove": [],
        "on_member_update": [],
        "on_server_join": [],
        "on_server_remove": [],
        "on_server_update": [],
        "on_server_role_create": [],
        "on_server_role_delete": [],
        "on_server_role_update": [],
        "on_server_emojis_update": [],
        "on_server_available": [],
        "on_server_unavailable": [],
        "on_voice_state_update": [],
        "on_member_ban": [],
        "on_member_unban": [],
        "on_typing": [],
        "on_group_join": [],
        "on_group_remove": []
    }

    # Iterate through module folders
    database_dir = "{}/modules".format(
        os.path.dirname(os.path.realpath(__file__)))
    for module_name in os.listdir(database_dir):
        module_dir = "{}/{}".format(database_dir, module_name)

        # Iterate through files in module
        if os.path.isdir(module_dir) and not module_name.startswith("_"):
            # Add all defined event handlers in module files
            module_event_handlers = os.listdir(module_dir)

            if module_found_handler:
                if "_ui.py" in module_event_handlers:
                    import_name = ".discord_modis.modules.{}.{}".format(
                        module_name, "_ui")
                    logger.debug(
                        "Found module UI file {}".format(import_name[23:]))

                    module_found_handler(module_name, importlib.import_module(import_name, "modis"))
                else:
                    module_found_handler(module_name, None)

            for event_handler in event_handlers.keys():
                if "{}.py".format(event_handler) in module_event_handlers:
                    import_name = ".discord_modis.modules.{}.{}".format(
                        module_name, event_handler)
                    logger.debug("Found event handler {}".format(import_name[23:]))

                    event_handlers[event_handler].append(
                        importlib.import_module(import_name, "modis"))

    return event_handlers


def add_api_key(key, value):
    """
    Adds a key to the bot's data

    Args:
        key: The name of the key to add
        value: The value for the key
    """

    if key is None or key == "":
        logger.error("Key cannot be empty")

    if value is None or value == "":
        logger.error("Value cannot be empty")

    from .. import datatools
    data = datatools.get_data()

    if "keys" not in data["discord"]:
        data["discord"]["keys"] = {}

    is_key_new = False
    if key not in data["discord"]["keys"]:
        is_key_new = True
    elif data["discord"]["keys"][key] == value:
        logger.info("API key '{}' already has value '{}'".format(key, value))
        return

    data["discord"]["keys"][key] = value
    datatools.write_data(data)

    key_text = "added" if is_key_new else "updated"
    logger.info("API key '{}' {} with value '{}'".format(key, key_text, value))
