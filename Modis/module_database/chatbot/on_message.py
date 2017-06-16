from ...share import *
from ._constants import *

from . import api_mitsuku


async def on_message(message):
    """The on_message event handler for this module

    Args:
        message (discord.Message): Input message
    """

    # Simplify message info
    server = message.server
    author = message.author
    channel = message.channel
    content = message.content

    # Only reply to server messages and don't reply to myself
    if server is not None and author != channel.server.me:
        # Only reply to mentions
        if channel.server.me in message.mentions:
            await client.send_typing(channel)

            # Make sure this module is in serverdata for this server
            _sd = get_serverdata()
            if modulename not in _sd[server.id]:
                _sd[server.id][modulename] = sd_structure
                write_serverdata(_sd)

            # Get new botcust2 from Mitsuku if does not exist for channel in serverdata
            if channel.id not in get_serverdata()[server.id][modulename]["channels"]:
                new_serverdata = get_serverdata()
                new_serverdata[server.id][modulename]["channels"][channel.id] = api_mitsuku.get_botcust2()
                write_serverdata(new_serverdata)

            # Get botcust2 from serverdata
            botcust2 = get_serverdata()[server.id][modulename]["channels"][channel.id]

            # Remove mention from message content so Mitsuku doesn't see it
            content = content.replace("<@!{}>".format(str(channel.server.me.id)), ' ')

            # Send Mitsuku's reply
            if botcust2:
                response = api_mitsuku.query(botcust2, content)
                if response:
                    await client.send_message(channel, response)
                else:
                    await client.send_message(channel, "```Couldn't get readable response from Mitsuku.```")
            else:
                await client.send_message(channel, "```Couldn't initialise with Mitsuku.```")
