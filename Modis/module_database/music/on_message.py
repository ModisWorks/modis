from ...share import *
from ._constants import *

from . import musicplayer


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
    _sd = get_serverdata()
    if modulename not in _sd[server.id]:
        _sd[server.id][modulename] = sd_structure
        write_serverdata(_sd)

    # Only reply to server messages and don't reply to myself
    if server is not None and author != channel.server.me:
        # Commands section
        if content.startswith(get_serverdata()[server.id]["prefix"]):
            # Parse message
            package = content.split(" ")
            command = package[0][1:]
            args = package[1:]
            arg = ' '.join(args)

            # Lock on to server if not yet locked
            if server.id not in cache:
                cache[server.id] = musicplayer.MusicPlayer(server.id)

            # Remove message
            if command in ['play', 'pause', 'skip', 'shuffle', 'stop', 'volume']:
                try:
                    await client.delete_message(message)
                except discord.errors.NotFound:
                    pass
                except discord.errors.Forbidden:
                    pass

            # Commands
            if command == 'init':
                await cache[server.id].init(author, channel)

            if command == 'play':
                await cache[server.id].play(author, channel, arg)

            elif command == 'pause':
                await cache[server.id].pause()

            elif command == 'skip':
                await cache[server.id].skip(num=arg)

            elif command == 'shuffle':
                await cache[server.id].shuffle()

            elif command == 'destroy':
                await cache[server.id].destroy(reason="Music Player was destroyed")

            elif command == 'stop':
                await cache[server.id].stop()

            elif command == 'volume':
                await cache[server.id].volume(arg)
