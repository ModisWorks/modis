from ... import share


async def on_message(message):
    # Add the server to serverdata if it doesn't yet exist
    _sd = share.get_serverdata()
    if message.server.id not in _sd:
        _sd[message.server.id] = {
            "prefix": share.prefix
        }
        share.write_serverdata(_sd)
