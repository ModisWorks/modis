import logging

import discord

from modis import main
from modis.modules.music import _data, _musicplayer, ui_embed

logger = logging.getLogger(__name__)


async def on_command(root, aux, query, msgobj):
    # Simplify message info
    server = msgobj.server
    author = msgobj.author
    channel = msgobj.channel
    content = msgobj.content

    # Lock on to server if not yet locked
    if server.id not in _data.cache or _data.cache[server.id].state == 'destroyed':
        _data.cache[server.id] = _musicplayer.MusicPlayer(server.id)

    # Remove message
    try:
        await main.client.delete_message(msgobj)
    except discord.errors.NotFound:
        logger.warning("Could not delete music player command message - NotFound")
    except discord.errors.Forbidden:
        logger.warning("Could not delete music player command message - Forbidden")

    logger.info("Root: {}, Aux: {}, Query: {}".format(root, aux, query))

    # Commands
    if root == 'play':
        now = "now" in aux
        next = "next" in aux
        shuffle = "shuffle" in aux

        if now or next:
            await _data.cache[server.id].play(author, channel, query, index=1, stop_current=now, shuffle=shuffle)
        else:
            await _data.cache[server.id].play(author, channel, query, shuffle=shuffle)
    if root == 'insert':
        await _data.cache[server.id].play(author, channel, query, index=query)
    elif root == 'pause':
        await _data.cache[server.id].pause()
    elif root == 'resume':
        await _data.cache[server.id].resume()
    elif root == 'skip':
        await _data.cache[server.id].skip(query=query)
    elif root == 'remove':
        await _data.cache[server.id].remove(index=query)
    elif root == 'rewind':
        await _data.cache[server.id].rewind(query=query)
    elif root == 'restart':
        await _data.cache[server.id].rewind(query="0")
    elif root == 'shuffle':
        await _data.cache[server.id].shuffle()
    elif root == 'loop':
        await _data.cache[server.id].set_loop(query)
    elif root == 'stop':
        await _data.cache[server.id].stop(log_stop=True)
    elif root == 'volume':
        await _data.cache[server.id].setvolume(query)
    elif root == 'topic':
        topic_on = "on" in aux
        topic_off = "off" in aux

        if topic_on and topic_off:
            await main.client.send_typing(msgobj.channel)
            embed = ui_embed.error_message(channel, "Invalid Topic",
                                           "The topic aux command cannot contain both 'on' and 'off'")
            await embed.send()
        elif topic_on:
            await main.client.send_typing(msgobj.channel)
            await _data.cache[server.id].set_topic_channel(channel)
        elif topic_off:
            await main.client.send_typing(msgobj.channel)
            await _data.cache[server.id].clear_topic_channel(channel)
        else:
            await main.client.send_typing(msgobj.channel)
            embed = ui_embed.error_message(channel, "Invalid Topic",
                                           "The topic aux command must be either 'on' or 'off'")
            await embed.send()
    elif root == 'nowplaying':
        await _data.cache[server.id].nowplaying_info(channel)
    elif root == 'destroy':
        await _data.cache[server.id].destroy()
    elif root == 'front' or root == 'movehere':
        await _data.cache[server.id].movehere(channel)
    elif root == 'reconnect' or root == 'movevoice':
        await _data.cache[server.id].movevoice(author)
