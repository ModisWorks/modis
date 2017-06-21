from ... import datatools


async def on_message(message):
    # Add the server to serverdata if it doesn't yet exist
    data = datatools.get_data()
    if message.server.id not in data["servers"]:
        data["servers"][message.server.id] = {
            "prefix": "!"
        }
        datatools.write_data(data)
