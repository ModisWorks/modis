from . import api_core


async def on_guild_join(guild):
    api_core.guild_update(guild.id)
