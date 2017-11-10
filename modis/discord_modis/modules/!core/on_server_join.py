from . import api_core


async def on_server_join(server):
    await api_core.update_server_data(server)
