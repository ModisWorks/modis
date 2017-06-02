import discord
import asyncio

import os
import googleapiclient.discovery

import random

import sys
import datetime

ytdevkey = "AIzaSyCQXS3nroiML-Vsf4-w6D34ImUzKrGkNtE"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "Menangorie-7f7c5e675b21.json"
youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=ytdevkey)

client = None
prefix = '/'

cache = {}

logging = True

modulename = "music"
creator = "Infraxion"
creatordp = "http://menangorie.ddns.net/modis/infraxion128.jpg"
modisdp = "http://menangorie.ddns.net/modis/logo128t.png"


class MessageUI:
    def __init__(self, channel):
        log("MessageUI.__init__", channel)
        self.gui_message = None
        self.gui = None
        self.channel = channel
        self.queue_length = 9

        self.init_gui()

        self.ready = False

    def init_gui(self):
        log("MessageUI.init_gui")
        self.gui = discord.Embed(
            title="Music Player",
            type='rich',
            description="Press the buttons!",
            colour=0x88FF00
        )
        self.gui.set_thumbnail(url=modisdp)
        self.gui.set_author(
            name="Modis",
            url="https://infraxion.github.io/modis/",
            icon_url=modisdp
        )
        self.gui.add_field(
            name="Now Playing",
            value="---",
            inline=False
        )
        display_queue = []
        for i in range(self.queue_length):
            display_queue.append("{}: ---\n".format(str(i + 1)))
        self.gui.add_field(
            name="Queue",
            value="```{}```".format(''.join(display_queue)),
            inline=False
        )
        self.gui.add_field(
            name="Songs left in queue",
            value="---"
        )
        self.gui.add_field(
            name="Volume",
            value="---"
        )
        self.gui.add_field(
            name="Status",
            value="```---```",
            inline=False
        )
        self.gui.set_footer(
            text="{} module by {}".format(modulename, creator),
            icon_url=creatordp
        )

    async def say(self, message):
        log("MessageUI.say", message)
        await client.send_typing(self.channel)
        await client.send_message(
            self.channel,
            message
        )

    async def tts(self, message):
        log("MessageUI.tts", message)
        await client.send_typing(self.channel)
        await client.send_message(
            self.channel,
            content=message,
            tts=True
        )

    async def create(self):
        log("MessageUI.create")
        if self.gui_message is None:
            await client.send_typing(self.channel)
            self.gui_message = await client.send_message(self.channel, embed=self.gui)

            await self.set_status("Loading buttons")
            await client.add_reaction(self.gui_message, "⏯")
            await client.add_reaction(self.gui_message, "⏹")
            await client.add_reaction(self.gui_message, "⏩")
            await client.add_reaction(self.gui_message, "🔀")
            await client.add_reaction(self.gui_message, "ℹ")
            await client.add_reaction(self.gui_message, "🔉")
            await client.add_reaction(self.gui_message, "🔊")

            self.ready = True

    async def update(self):
        log("MessageUI.update")
        if self.gui_message:
            try:
                await client.edit_message(self.gui_message, embed=self.gui)
            except discord.NotFound:
                pass

    async def destroy(self, reason=None):
        log("MessageUI.destroy", reason)
        if self.gui_message:
            try:
                await client.delete_message(self.gui_message)
            except discord.NotFound:
                pass
        if reason:
            await self.say(reason)
        self.gui_message = None
        self.init_gui()

        self.ready = False

    async def reset(self, reason=None):
        log("MessageUI.reset", reason)
        self.init_gui()
        await self.set_status(reason)

    async def set_nowplaying(self, message):
        log("MessageUI.set_nowplaying", message)
        self.gui.set_field_at(
            0,
            name="Now playing",
            value=message,
            inline=False
        )
        await self.update()

    async def set_queue(self, queue):
        log("MessageUI.set_queue", "list of length {}".format(str(len(queue))))
        display_queue = []

        for i in range(self.queue_length):
            try:
                if len(queue[i][1]) > 40:
                    songname = queue[i][1][:37] + "..."
                else:
                    songname = queue[i][1]
            except IndexError:
                songname = "---"
            display_queue.append("{}: {}\n".format(str(i + 1), songname))

        self.gui.set_field_at(
            1,
            name="Queue",
            value="```{}```".format(''.join(display_queue)),
            inline=False
        )

        self.gui.set_field_at(
            2,
            name="Songs left in queue",
            value=str(len(queue)),
            inline=True
        )

        await self.update()

    async def set_volume(self, volume):
        log("MessageUI.set_volume", volume)
        self.gui.set_field_at(
            3,
            name="Volume",
            value="{}%".format(str(volume)),
            inline=True
        )

        await self.update()

    async def set_status(self, message):
        log("MessageUI.set_status", message)
        if len(message) > 43:
            message = "{}...".format(message[:40])
        self.gui.set_field_at(
            4,
            name="Status",
            value="```{}```".format(message),
            inline=False
        )
        await self.update()

    async def set_tempstatus(self, message):
        log("MessageUI.set_status", message)
        if len(message) > 43:
            message = "{}...".format(message[:40])
        self.gui.set_field_at(
            4,
            name="Status",
            value="```{}```".format(message),
            inline=False
        )
        await self.update()


class VoiceUI:
    def __init__(self, channel, linked_messageui=None):
        log("VoiceUI.__init__", channel, linked_messageui)

        self.channel = channel
        self.speaker = None
        self.player = None

        self.queue = []
        self.volume = 10

        self.messageui = linked_messageui

        self.ready = False

    async def create(self):
        log("VoiceUI.create")
        if self.channel:
            if self.messageui:
                await self.messageui.set_status("Connecting to voice")
            self.speaker = await client.join_voice_channel(self.channel)

            self.ready = True
        else:
            await self.destroy()
            await self.messageui.reset("You're not connected to a voice channel.")

    async def enqueue(self, query):
        log("VoiceUI.enqueue", query)
        # Non-YouTube
        if "/" in query and "youtube" not in query:
            self.queue.append([query, query])
            # INFORM QUEUE OF NON-YT LINK
        # YouTube
        else:
            # Search YouTube
            sys.stdout = open("ytdl.log", 'a')
            ytget = youtube.search().list(
                q=query,
                part="id,snippet",
                maxResults=1,
                type="video,playlist"
            ).execute()
            sys.stdout = sys.__stdout__

            title = ytget["items"][0]["snippet"]["title"]
            if self.messageui:
                await self.messageui.set_tempstatus("Queueing {}".format(title))

            # Videos
            if ytget["items"][0]["id"]["kind"] == "youtube#video":
                videoid = ytget["items"][0]["id"]["videoId"]
                self.queue.append(["https://www.youtube.com/watch?v={}".format(videoid), title])

            # Playlists
            elif ytget["items"][0]["id"]["kind"] == "youtube#playlist":
                playlistid = ytget["items"][0]["id"]["playlistId"]
                plget = youtube.playlistItems().list(
                    playlistId=playlistid,
                    part="snippet",
                    maxResults=50
                ).execute()

                for entry in plget["items"]:
                    videoid = entry["snippet"]["resourceId"]["videoId"]
                    songname = entry["snippet"]["title"]
                    self.queue.append(["https://www.youtube.com/watch?v={}".format(videoid), songname])

                # For playlists with more than 50 entries
                if "nextPageToken" in plget:
                    counter = 2
                    while "nextPageToken" in plget:
                        if self.messageui:
                            await self.messageui.set_tempstatus("Queueing {} (page {})".format(title, str(counter)))
                        counter += 1
                        plget = youtube.playlistItems().list(
                            playlistId=playlistid,
                            part="snippet",
                            maxResults=50,
                            pageToken=plget["nextPageToken"]
                        ).execute()

                        for entry in plget["items"]:
                            videoid = entry["snippet"]["resourceId"]["videoId"]
                            songname = entry["snippet"]["title"]
                            self.queue.append(["https://www.youtube.com/watch?v={}".format(videoid), songname])

        if self.messageui:
            await self.messageui.set_queue(self.queue)

    async def play(self):
        log("VoiceUI.play")
        if self.queue:
            if self.messageui:
                await self.messageui.set_status("Loading next song")

            song = self.queue[0][0]
            songname = self.queue[0][1]

            sys.stdout = open("ytdl.log", 'a')
            self.player = await self.speaker.create_ytdl_player(song, after=lambda: runcoro(self.after()))
            sys.stdout = sys.__stdout__

            self.player.volume = self.volume / 100
            self.player.start()

            self.queue.pop(0)

            if self.messageui:
                await self.messageui.set_queue(self.queue)
                await self.messageui.set_status("Playing")
                await self.messageui.set_nowplaying(songname)
        else:
            await self.destroy()
            await self.messageui.reset("Finished queue")

    async def after(self):
        log("VoiceUI.after")
        if self.player.error is None:
            await self.play()
        else:
            await self.destroy()
            if self.messageui:
                await self.messageui.reset("Encountered an error while playing :/")

    async def destroy(self):
        log("VoiceUI.destroy")
        self.queue = []
        try:
            await self.speaker.disconnect()
            self.player.stop()
        except AttributeError:
            pass
        except discord.NotFound:
            pass

        self.ready = False

    async def skip(self, number=1):
        log("VoiceUI.skip", number)
        for i in range(number - 1):
            try:
                self.queue.pop(0)
            except IndexError:
                pass

        if self.messageui:
            await self.messageui.set_status("Skipping")

        try:
            self.player.stop()
        except AttributeError:
            pass

    async def shuffle(self):
        log("VoiceUI.shuffle")
        if self.messageui:
            await self.messageui.set_tempstatus("Shuffling")

        random.shuffle(self.queue)

        if self.messageui:
            await self.messageui.set_queue(self.queue)

        if self.messageui:
            await self.messageui.set_tempstatus("Shuffled")

    async def pause(self):
        log("VoiceUI.pause")
        try:
            if self.player.is_playing():
                if self.messageui:
                    await self.messageui.set_status("Paused")

                self.player.pause()
            else:
                if self.messageui:
                    await self.messageui.set_status("Playing")

                self.player.resume()
        except AttributeError:
            pass

    async def vol_down(self):
        log("VoiceUI.vol_down")
        if self.volume > 0:
            if self.messageui:
                await self.messageui.set_tempstatus("Volume down")

            self.volume = (10 * ((self.volume + 9) // 10)) - 10

            if self.messageui:
                await self.messageui.set_volume(self.volume)

            try:
                self.player.volume = self.volume / 100
            except AttributeError:
                pass
        else:
            if self.messageui:
                await self.messageui.set_tempstatus("Already at minimum volume")

    async def vol_up(self):
        log("VoiceUI.vol_up")
        if self.volume < 100:
            if self.messageui:
                await self.messageui.set_tempstatus("Volume up")

            self.volume = (10 * (self.volume // 10)) + 10

            if self.messageui:
                await self.messageui.set_volume(self.volume)

            try:
                self.player.volume = self.volume / 100
            except AttributeError:
                pass
        else:
            if self.messageui:
                await self.messageui.set_tempstatus("Already at maximum volume")

    async def set_vol(self, volume):
        log("VoiceUI.set_vol", volume)
        if 0 <= volume <= 200:
            if self.messageui:
                await self.messageui.set_tempstatus("Setting volume")

            self.volume = volume

            if self.messageui:
                await self.messageui.set_volume(self.volume)

            try:
                self.player.volume = self.volume / 100
            except AttributeError:
                pass
        else:
            if self.messageui:
                await self.messageui.set_tempstatus("Volume must be between 0 and 200%")


class ServerLock:
    def __init__(self, server_id):
        log("ServerLock.__init__")
        self.messageui = None
        self.voiceui = None

        self.server_id = server_id

        self.ready = False

    async def create_ui(self, author, text_channel):
        log("ServerLock.create_ui")
        if self.voiceui is None or not self.voiceui.ready:
            if self.messageui is None:
                self.messageui = MessageUI(text_channel)
            await self.messageui.create()

            self.voiceui = VoiceUI(author.voice_channel, self.messageui)
            await self.voiceui.create()

            self.ready = all((self.messageui.ready, self.voiceui.ready))

        return self.ready

    async def play(self, author, text_channel, args):
        log("ServerLock.play")
        # Create uis
        if await self.create_ui(author, text_channel):
            # Add the query to queue
            await self.voiceui.enqueue(" ".join(args))
            # Start playing if not yet playing
            if self.voiceui.player is None:
                await self.voiceui.play()

    async def pause(self):
        log("ServerLock.pause")
        if self.voiceui and self.ready:
            await self.voiceui.pause()

    async def stop(self, reason):
        log("ServerLock.destroy")
        if self.voiceui:
            if self.voiceui.ready:
                await self.voiceui.destroy()

        if self.messageui:
            if self.messageui.ready:
                await self.messageui.reset(reason)

    async def destroy(self, reason=None):
        log("ServerLock.destroy", reason)
        if self.voiceui and self.voiceui.ready:
                await self.voiceui.destroy()
                self.voiceui = None

        if self.messageui and self.messageui.ready:
                await self.messageui.destroy(reason)
                self.voiceui = None

    async def skip(self, num=1):
        log("ServerLock.skip", num)
        if self.voiceui and self.ready:
            if num:
                try:
                    arg = int(num)
                except TypeError:
                    if self.messageui:
                        await self.messageui.set_tempstatus("Skip argument must be a number")
                else:
                    await self.voiceui.skip(arg)
            else:
                await self.voiceui.skip(1)

    async def shuffle(self):
        log("ServerLock.shuffle")
        if self.voiceui and self.ready:
            await self.voiceui.shuffle()

    async def help(self):
        log("ServerLock.help")
        if self.messageui and self.ready:
            await self.messageui.set_tempstatus("Feature unavailable")

    async def volume(self, value):
        log("ServerLock.volume", value)
        if self.voiceui and self.ready:
            if value == '+':
                await self.voiceui.vol_up()
            elif value == '-':
                await self.voiceui.vol_down()
            else:
                try:
                    value = int(value)
                except ValueError:
                    if self.messageui:
                        await self.messageui.set_tempstatus("Volume argument must be +, -, or a %")
                else:
                    await self.voiceui.set_vol(value)


def init(iclient, iprefix):
    log("################################")
    log("musibot.init")
    print("Loading {} by {}".format(modulename, creator))

    global client
    client = iclient
    global prefix
    prefix = iprefix


def runcoro(async_function):
    asyncio.run_coroutine_threadsafe(async_function, client.loop)


def log(name, *args):
    if logging:
        log_package = [str(datetime.datetime.now()).split('.')[0] + " " + name]
        for arg in args:
            log_package.append("                        " + str(arg))

        sys.stdout = open("musibot.log", 'a')
        print('\n'.join(log_package))
        sys.stdout = sys.__stdout__
        print('\n'.join(log_package))


async def on_message(message):
    # Get message info
    server = message.server
    author = message.author
    channel = message.channel
    content = message.content
    # Server commands
    if server is not None and author != channel.server.me and content.startswith(prefix):

        # Lock on to server if not yet locked
        if server.id not in cache:
            cache[server.id] = ServerLock(server.id)

        # Parse message
        package = content.split(" ")
        command = package[0][1:]
        args = package[1:]

        # Remove message
        if command in ['play', 'pause', 'skip', 'shuffle', 'destroy', 'stop', 'help', 'volume']:
            try:
                await client.delete_message(message)
            except discord.errors.NotFound:
                pass
            except discord.errors.Forbidden:
                pass

        # Commands
        if command == 'play':
            await cache[server.id].play(author, channel, args)

        elif command == 'pause':
            await cache[server.id].pause()

        elif command == 'skip':
            await cache[server.id].skip(''.join(args))

        elif command == 'shuffle':
            await cache[server.id].shuffle()

        elif command == 'destroy':
            await cache[server.id].destroy("Thanks for using Menangorie MusicBot v2.1!")

        elif command == 'stop':
            await cache[server.id].stop("Stopped")

        elif command == 'help':
            await cache[server.id].info()

        elif command == 'volume':
            await cache[server.id].volume(''.join(args))


async def on_reaction_add(reaction, user):
    # Get reaction info
    message = reaction.message
    server = reaction.message.server
    command = reaction.emoji

    # Check if command
    if server.id in cache:
        if cache[server.id].messageui:
            if cache[server.id].messageui.gui_message:
                if user != message.channel.server.me and message.id == cache[server.id].messageui.gui_message.id:
                    # Remove reaction
                    try:
                        await client.remove_reaction(message, command, user)
                    except discord.errors.NotFound:
                        pass
                    except discord.errors.Forbidden:
                        pass

                    # Commands
                    if command == "⏯":
                        await cache[server.id].pause()
                    if command == "⏹":
                        await cache[server.id].stop("Stopped")
                    if command == "⏩":
                        await cache[server.id].skip()
                    if command == "🔀":
                        await cache[server.id].shuffle()
                    if command == "ℹ":
                        await cache[server.id].help()
                    if command == "🔉":
                        await cache[server.id].volume('-')
                    if command == "🔊":
                        await cache[server.id].volume('+')
