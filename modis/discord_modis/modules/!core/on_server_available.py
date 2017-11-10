from . import api_core


async def on_server_available(server):
    await api_core.update_server_data(server)
