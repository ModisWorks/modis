import logging

import discord

from modis import datatools
from . import _data, _musicplayer
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
        # Commands section
        prefix = data["discord"]["servers"][server.id]["prefix"]
        if content.startswith(prefix):
            # Parse message
            package = content.split(" ")
            command = package[0][len(prefix):]
            args = package[1:]
            arg = ' '.join(args)

            # Lock on to server if not yet locked
            if server.id not in _data.cache or _data.cache[server.id].state == 'destroyed':
                _data.cache[server.id] = _musicplayer.MusicPlayer(server.id)

            # Remove message
            if command in ['play', 'playnext', 'playnow', 'playshuffle', 'pause', 'resume', 'skip', 'remove', 'rewind',
                           'shuffle', 'volume', 'stop', 'destroy', 'front', 'movehere', 'settopic', 'cleartopic',
                           'notopic']:
                try:
                    await client.delete_message(message)
                except discord.errors.NotFound:
                    logger.warning("Could not delete music player command message - NotFound")
                except discord.errors.Forbidden:
                    logger.warning("Could not delete music player command message - Forbidden")

            # Commands
            if command == 'play':
                await _data.cache[server.id].play(author, channel, arg)

            if command == 'playnext':
                await _data.cache[server.id].play(author, channel, arg, now=True)

            if command == 'playnow':
                await _data.cache[server.id].play(author, channel, arg, now=True, stop_current=True)

            if command == 'playshuffle':
                await _data.cache[server.id].play(author, channel, arg, shuffle=True)

            elif command == 'pause':
                await _data.cache[server.id].pause()

            elif command == 'resume':
                await _data.cache[server.id].resume()

            elif command == 'skip':
                await _data.cache[server.id].skip(query=arg)

            elif command == 'remove':
                await _data.cache[server.id].remove(index=arg)

            elif command == 'rewind':
                await _data.cache[server.id].rewind(query=arg)

            elif command == 'shuffle':
                await _data.cache[server.id].shuffle()

            elif command == 'stop':
                await _data.cache[server.id].stop()

            elif command == 'destroy':
                await _data.cache[server.id].destroy()

            elif command == 'volume':
                await _data.cache[server.id].setvolume(arg)

            elif command == 'front' or command == 'movehere':
                await _data.cache[server.id].movehere(channel)

            elif command == 'settopic':
                await _data.cache[server.id].set_topic_channel(channel)

            elif command == 'cleartopic' or command == 'notopic':
                await _data.cache[server.id].clear_topic_channel(channel)
