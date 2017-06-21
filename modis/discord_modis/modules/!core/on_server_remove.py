from .... import datatools


async def on_server_remove(server):
    # Remove the server from data
    data = datatools.get_data()
    if server.id in data["discord"]["servers"]:
        data["discord"]["servers"].pop(server.id)
        datatools.write_data(data)
