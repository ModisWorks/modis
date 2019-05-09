from . import api_core


async def on_server_available(server):
    api_core.guild_update(server.id)
