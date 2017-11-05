from modis import datatools
from . import _data, api_rocketleaguestats, ui_embed
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
        if content.startswith(data["discord"]["servers"][server.id]["prefix"]):
            alias_steam = ["steam", "pc"]
            alias_ps = ["ps", "psn", "playstation", "ps4", "playstation 4"]
            alias_xbox = ["xbox", "xb", "xb1", "xbone", "xbox one", "xbox one"]

            # Parse message
            package = content.split(" ")
            command = package[0][1:]
            args = package[1:]

            platform = "steam"
            if len(args) > 0:
                player_name = args[0]
            if len(args) > 1:
                platform = ' '.join(args[1:]).lower()

            if platform in alias_steam:
                platform = "steam"
            elif platform in alias_ps:
                platform = "ps"
            elif platform in alias_xbox:
                platform = "xbox"

            # Commands
            if command == 'rlstats':
                await client.send_typing(channel)

                # Get Rocket League stats from stats API
                success, rldata = api_rocketleaguestats.check_rank(player_name, platform)
                # Create embed UI
                if success:
                    embed = ui_embed.success(channel, rldata[0], rldata[1], rldata[2], rldata[3])
                else:
                    embed = ui_embed.fail_api(channel)

                await embed.send()
