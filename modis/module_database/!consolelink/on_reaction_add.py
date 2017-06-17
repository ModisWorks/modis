from ... import share


async def on_reaction_add(reaction, user):
    # Add the server to serverdata if it doesn't yet exist
    _sd = share.get_serverdata()
    if reaction.message.server.id not in _sd:
        _sd[reaction.message.server.id] = {
            "prefix": share.prefix
        }
        share.write_serverdata(_sd)
