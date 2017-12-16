import logging

from . import api_reddit, ui_embed

logger = logging.getLogger(__name__)


async def on_command(root, aux, query, msgobj):
    if root == "gamedeals":
        posts = api_reddit.get_top10()
        if posts:
            for post in posts:
                embed = ui_embed.success(msgobj.channel, post)
                await embed.send()
        else:
            embed = ui_embed.no_results(msgobj.channel)
            await embed.send()
