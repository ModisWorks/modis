from modis import main
from modis.tools import data

from . import api_hexconvert, ui_embed


async def on_message(message):
    """The on_message event handler for this module

    Args:
        message (discord.Message): Input message
    """

    # TODO make an option to limit hex to only the !hex command instead of reading all messages

    if message.content.startswith(data.cache["servers"][message.server.id]["prefix"]):
        return

    hex_strs = api_hexconvert.convert_hex_value(message.content)
    if len(hex_strs) > 0:
        for hex_str in hex_strs:
            await main.client.send_typing(message.channel)
            image_url = "https://dummyimage.com/350x200.png/{0}/{0}".format(hex_str)
            embed = ui_embed.success(message.channel, image_url, hex_str)
            await embed.send()
