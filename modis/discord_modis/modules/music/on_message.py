import logging

from ..._client import client
from .... import datatools

from . import _data

from . import _musicplayer

import discord

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

    # Make sure this module is in serverdata for this server
    data = datatools.get_data()
    if _data.modulename not in data["discord"]["servers"][server.id]:
        data["discord"]["servers"][server.id][_data.modulename] = _data.sd_structure
        datatools.write_data(data)

    # Only reply to server messages and don't reply to myself
    if server is not None and author != channel.server.me:
        # Commands section
        if content.startswith(datatools.get_data()["discord"]["servers"][server.id]["prefix"]):
            # Parse message
            package = content.split(" ")
            command = package[0][1:]
            args = package[1:]
            arg = ' '.join(args)

            # Lock on to server if not yet locked
            if server.id not in _data.cache:
                _data.cache[server.id] = _musicplayer.MusicPlayer(server.id)

            # Remove message
            if command in ['play', 'pause', 'skip', 'shuffle', 'stop', 'volume', 'front', 'movehere']:
                try:
                    await client.delete_message(message)
                except discord.errors.NotFound:
                    logger.warning("Could not delete music player command message - NotFound")
                except discord.errors.Forbidden:
                    logger.warning("Could not delete music player command message - Forbidden")

            # Commands
            if command == 'init':
                await _data.cache[server.id].setup(author, channel)

            if command == 'play':
                await _data.cache[server.id].play(author, channel, arg)

            elif command == 'pause':
                await _data.cache[server.id].pause()

            elif command == 'skip':
                await _data.cache[server.id].skip(query=arg)

            elif command == 'shuffle':
                await _data.cache[server.id].shuffle()

            elif command == 'destroy':
                await _data.cache[server.id].destroy(reason="Music Player was destroyed")

            elif command == 'stop':
                await _data.cache[server.id].stop()

            elif command == 'volume':
                await _data.cache[server.id].volume(arg)

            elif command == 'front' or command == 'movehere':
                await _data.cache[server.id].movehere(channel)
