import discord
import threading
import sys
import traceback
import datetime
import os

import bot_modules
import bot_console.main_console as console

token = os.environ['token']
client_id = os.environ['client_id']
game = None
prefix = "!"
name = "Modis"

client = discord.Client()


def init():
    print("Starting console...")
    console_thread = threading.Thread(target=console.main, args=[])
    console_thread.start()
    console.init(client, name + " Console")

    print("Loading modules...")
    bot_modules.music.init(client, prefix)
    bot_modules.replies.init(client)
    bot_modules.tableflip.init(client)
    bot_modules.chatbot.init(client)
    bot_modules.rocketleague.init(client, prefix)

    print("Connecting to Discord...")
    client.run(token)


def required_perms():
    perms = discord.Permissions()
    perms.add_reactions = True
    perms.read_messages = True
    perms.send_messages = True
    perms.send_tts_messages = True
    perms.manage_messages = True
    perms.connect = True
    perms.speak = True
    return perms


@client.event
async def on_ready():
    print("Ready.\n"
          + "---\n"
          + "To add this bot to a server, use this link:\n"
          + "{}\n"
          + "---".format(discord.utils.oauth_url(client_id)))
    if game:
        await client.change_presence(
            game=discord.Game(
                name=game,
                url="https://infraxion.github.io/modis/",
                type=0),
            status=discord.Status.online,
            afk=False)


@client.event
async def on_message(message):
    for _module in bot_modules.reactors['on_message']:
        _module.on_message(message)


@client.event
async def on_reaction_add(reaction, user):
    for _module in bot_modules.reactors['on_reaction_add']:
        _module.on_reaction_add(reaction, user)


@client.event
async def on_error(event_method, *args, **kwargs):
    print("\n"
          + "################################\n"
          + "ERROR\n"
          + str(datetime.datetime.now()).split('.')[0] + "\n"
          + ''.join(traceback.format_exception(sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2]))
          + "################################\n\n")

init()
