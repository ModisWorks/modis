from ...share import *
from ._constants import *


async def on_reaction_add(reaction, user):
    """The on_message event handler for this module

    Args:
        reaction (discord.Reaction): Input reaction
        user (discord.User): The user that added the reaction
    """

    # Simplify reaction info
    server = reaction.message.server
    channel = reaction.message.channel
    emoji = reaction.emoji

    # Commands section
    if user != reaction.message.channel.server.me:
        try:
            valid_reaction = reaction.message.id == cache[server.id].ui_m.ui_m.sent_embed.id
        except AttributeError:
            pass
        else:
            if valid_reaction:
                # Remove reaction
                try:
                    await client.remove_reaction(reaction.message, emoji, user)
                except discord.errors.NotFound:
                    pass
                except discord.errors.Forbidden:
                    pass

                # Commands
                if emoji == "⏯":
                    await cache[server.id].pause()
                if emoji == "⏹":
                    await cache[server.id].stop()
                if emoji == "⏩":
                    await cache[server.id].skip()
                if emoji == "🔀":
                    await cache[server.id].shuffle()
                if emoji == "🔉":
                    await cache[server.id].volume('-')
                if emoji == "🔊":
                    await cache[server.id].volume('+')
