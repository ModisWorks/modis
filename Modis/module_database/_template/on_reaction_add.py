from share import *
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

    # Your code here
