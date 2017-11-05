import logging

from modis import datatools
from . import _data, api_mitsuku
from ..._client import client

logger = logging.getLogger(__name__)


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

    data = datatools.get_data()

    if not data["discord"]["servers"][server.id][_data.modulename]["activated"]:
        return

    # Only reply to server messages and don't reply to myself
    if server is not None and author != channel.server.me:
        # Only reply to mentions
        if channel.server.me in message.mentions:

            logger.info("Bot was mentioned, summoning Mitsuku")
            await client.send_typing(channel)

            # Get new botcust2 from Mitsuku if does not exist for channel in serverdata
            if channel.id not in data["discord"]["servers"][server.id][_data.modulename]["channels"]:
                new_serverdata = data
                new_serverdata["discord"]["servers"][server.id][_data.modulename]["channels"][channel.id] = \
                    api_mitsuku.get_botcust2()
                datatools.write_data(new_serverdata)

            # Get botcust2 from serverdata
            botcust2 = data["discord"]["servers"][server.id][_data.modulename]["channels"][channel.id]

            # Remove mention from message content so Mitsuku doesn't see it
            content = content.replace("<@{}>".format(str(channel.server.me.id)), ' ')
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
