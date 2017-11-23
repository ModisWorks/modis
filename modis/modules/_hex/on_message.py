from modis import datatools
from . import api_hexconvert, ui_embed, _data
from ..._client import client


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
            command = package[0][len(prefix):]
            args = package[1:]
            arg = ' '.join(args)

            # Commands
            if command == 'hex':
                await client.send_typing(channel)

                # Parse message
                success, hex_str = api_hexconvert.convert_hex_value(arg)
                # Create embed UI
                if success:
                    image_url = convert_hex_to_url(hex_str)
                    embed = ui_embed.success(channel, image_url, hex_str)
                else:
                    embed = ui_embed.fail_api(channel)

                await embed.send()
        else:
            # Parse message
            success, hex_str = api_hexconvert.convert_hex_value(content)
            # Create embed UI
            if success:
                await client.send_typing(channel)
                image_url = convert_hex_to_url(hex_str)
                embed = ui_embed.success(channel, image_url, hex_str)
                await embed.send()


def convert_hex_to_url(hex_value):
    """
    Converts a hex value to a url for an image of that value

    Returns:
        url (str): A url referencing an image of the given hex value
    """
    return "https://dummyimage.com/250.png/{0}/{0}".format(hex_value)
