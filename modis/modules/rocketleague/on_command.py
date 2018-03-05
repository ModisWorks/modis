import logging

from modis import main
from . import api_rocketleaguestats, ui_embed

logger = logging.getLogger(__name__)

ALIAS_STEAM = ["steam", "pc"]
ALIAS_PS = ["ps", "psn", "playstation", "ps4", "playstation4"]
ALIAS_XBOX = ["xbox", "xb", "xb1", "xbone", "xboxone", "xbox1"]


async def on_command(root, aux, query, msgobj):
    if root == "rlstats":
        if not aux:
            platform = "steam"
        elif aux[0] in ALIAS_STEAM:
            platform = "steam"
        elif aux[0] in ALIAS_PS:
            platform = "ps"
        elif aux[0] in ALIAS_XBOX:
            platform = "xbox"
        else:
            platform = "steam"

        # Get Rocket League stats from stats API
        success, rldata = api_rocketleaguestats.check_rank(query, platform)

        # Create embed UI
        await main.client.send_typing(msgobj.channel)
        if success:
            embed = ui_embed.success(msgobj.channel, rldata[0], rldata[1], rldata[2], rldata[3])
        else:
            embed = ui_embed.fail_api(msgobj.channel)

        await embed.send()
