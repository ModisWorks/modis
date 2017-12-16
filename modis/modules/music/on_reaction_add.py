from modis import main

from . import _data

import discord


async def on_reaction_add(reaction, user):
    """The on_message event handler for this module

    Args:
        reaction (discord.Reaction): Input reaction
        user (discord.User): The user that added the reaction
    """

    # Simplify reaction info
    server = reaction.message.server
    emoji = reaction.emoji

    # TODO port to new activation
    # if not data.cache["servers"][server.id][_data.modulename]["activated"]:
    #     return

    # Commands section
    if user != reaction.message.channel.server.me:
        if server.id not in _data.cache or _data.cache[server.id].state == 'destroyed':
            return

        try:
            valid_reaction = reaction.message.id == _data.cache[server.id].embed.sent_embed.id
        except AttributeError:
            pass
        else:
            if valid_reaction:
                # Remove reaction
                try:
                    await main.client.remove_reaction(reaction.message, emoji, user)
                except discord.errors.NotFound:
                    pass
                except discord.errors.Forbidden:
                    pass

                # Commands
                if emoji == "⏯":
                    await _data.cache[server.id].toggle()
                if emoji == "⏹":
                    await _data.cache[server.id].stop()
                if emoji == "⏭":
                    await _data.cache[server.id].skip("1")
                if emoji == "⏮":
                    await _data.cache[server.id].rewind("1")
                if emoji == "🔀":
                    await _data.cache[server.id].shuffle()
                if emoji == "🔉":
                    await _data.cache[server.id].setvolume('-')
                if emoji == "🔊":
                    await _data.cache[server.id].setvolume('+')
