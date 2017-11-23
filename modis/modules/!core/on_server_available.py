from . import api_core


async def on_server_available(server):
    api_core.server_update(server.id)
