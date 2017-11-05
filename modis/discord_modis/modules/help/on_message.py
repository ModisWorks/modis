from . import api_help, ui_embed, _data
from ..._client import client
from modis import datatools


async def on_message(message):
    """The on_message event handler for this module

    Args:
        message (discord.Message): Input message
    """

    # Simplify message info
    server = message.server
    author = message.author
    channel = message.channel
    content = message.content

    data = datatools.get_data()

    if not data["discord"]["servers"][server.id][_data.modulename]["activated"]:
        return

    # Only reply to server messages and don't reply to myself
    if server is not None and author != channel.server.me:
        # Commands section
        prefix = data["discord"]["servers"][server.id]["prefix"]
        if content.startswith(prefix):
            # Parse message
            package = content.split(" ")
            command = package[0][1:]
            args = package[1:]
            arg = ' '.join(args)

            # Commands
            if command == 'help':
                if args:
                    # Parse message
                    datapacks = api_help.get_help_datapacks(arg, prefix)
                    # Create embed UI
                    if datapacks:
                        await client.send_typing(channel)
                        embed = ui_embed.success(channel, arg, datapacks)
                        await embed.send()
                else:
                    # Parse message
                    datapacks = api_help.get_help_commands(prefix)
                    # Create embed UI
                    if datapacks:
                        await client.send_typing(channel)
                        embed = ui_embed.success(channel, arg, datapacks)
                        await embed.send()


def convert_hex_to_url(hex_value):
    """
    Converts a hex value to a url for an image of that value

    Returns:
        url (str): A url referencing an image of the given hex value
    """
    return "https://dummyimage.com/250.png/{0}/{0}".format(hex_value)
