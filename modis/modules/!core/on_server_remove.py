from . import api_core


async def on_server_remove(server):
    api_core.server_remove(server.id)
