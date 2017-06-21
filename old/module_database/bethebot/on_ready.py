from ... import share


async def on_ready():
    # Set the game Modis is playing
    if share.game:
        await share.client.change_presence(
            game=share.discord.Game(
                name=share.game,
                url="https://infraxion.github.io/modis/",
                type=0),
            status=share.discord.Status.online,
            afk=False)
