from . import api_core


async def on_server_join(server):
    await api_core.server_update(server)
