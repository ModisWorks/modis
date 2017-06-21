from .... import datatools


async def on_server_available(server):
    # Add the server to serverdata if it doesn't yet exist
    data = datatools.get_data()
    if server.id not in data["discord"]["servers"]:
        data["discord"]["servers"][server.id] = {
            "prefix": "!"
        }
        datatools.write_data(data)
