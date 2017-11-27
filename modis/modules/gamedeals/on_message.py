from modis import main
from modis.tools import data

from . import api_reddit, ui_embed


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

    # TODO port to new activation
    # if not data["discord"]["servers"][server.id][_data.modulename]["activated"]:
    #     return

    # Only reply to server messages and don't reply to myself
    if server is not None and author != channel.server.me:
        # Commands section
        prefix = data.cache["servers"][server.id]["prefix"]
        if content.startswith(prefix):
            # Parse message
            package = content.split(" ")
            command = package[0][len(prefix):]

            # Commands
            if command == 'gamedeals':
                await main.client.send_typing(channel)

                # Get posts from Reddit API
                posts = api_reddit.get_top10()

                if posts:
                    for post in posts:
                        # Create embed UI
                        embed = ui_embed.success(channel, post)
                        await embed.send()
                else:
                    embed = ui_embed.no_results(channel)
                    await embed.send()
