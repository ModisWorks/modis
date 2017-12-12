import logging

from . import api_hexconvert, ui_embed

logger = logging.getLogger(__name__)


async def on_command(root, aux, query, msgobj):
    if root == "hex":
        hex_strs = api_hexconvert.convert_hex_value(query)

        if len(hex_strs) > 0:
            for hex_str in hex_strs:
                image_url = "https://dummyimage.com/350x200.png/{0}/{0}".format(hex_str)
                embed = ui_embed.success(msgobj.channel, image_url, hex_str)
                await embed.send()
        else:
            embed = ui_embed.fail_api(msgobj.channel)
            await embed.send()
