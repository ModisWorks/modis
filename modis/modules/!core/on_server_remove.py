from . import api_core


async def on_server_remove(server):
    api_core.guild_remove(server.id)
