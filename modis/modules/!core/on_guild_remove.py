from . import api_core


async def on_guild_remove(guild):
    api_core.guild_remove(guild.id)
