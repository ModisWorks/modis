import logging

from ..._client import client
from .._tools import ui_embed

from . import api_youtube
from . import _data

import discord
import asyncio
import random
import threading

logger = logging.getLogger(__name__)


class MusicPlayer:
    def __init__(self, server_id):
        """Locks onto a server for easy management of various UIs

        Args:
            server_id (str): The Discord ID of the server to lock on to
        """

        # Player variables
        self.server_id = server_id
        self.logger = logging.getLogger("{}.{}".format(__name__, self.server_id))
        self.ready = False

        # Voice variables
        self.vchannel = None
        self.vclient = None
        self.streamer = None
        self.queue = []
        self.volume = 10
        self.vready = False

        # Gui variables
        self.mchannel = None
        self.embed = None
        self.queue_display = 9
        self.nowplayinglog = logging.getLogger("{}.{}.nowplaying".format(__name__, self.server_id))
        self.queuelog = logging.getLogger("{}.{}.queue".format(__name__, self.server_id))
        self.queuelenlog = logging.getLogger("{}.{}.queuelen".format(__name__, self.server_id))
        self.volumelog = logging.getLogger("{}.{}.volume".format(__name__, self.server_id))
        self.statuslog = logging.getLogger("{}.{}.status".format(__name__, self.server_id))
        self.statuslog.setLevel("DEBUG")
        self.statustimer = None
        self.mready = False

    # Commands

    async def play(self, author, text_channel, query):
        """The play command

        Args:
            author (discord.Member): The member that called the command
            text_channel (discord.Channel): The channel where the command was called
            query (str): The argument that was passed with the command
        """

        self.logger.debug("play command")

        # Init music player if not done
        if not self.mready:
            await self.msetup(text_channel)

        if not self.vready:
            await self.vsetup(author)

        self.ready = self.mready and self.vready

        if self.ready:
            # Add the query to queue
            self.enqueue(query)

            # Start playing if not yet playing
            if self.streamer is None:
                await self.vplay()

    async def pause(self):
        """The pause command"""

        self.logger.debug("pause command")

        if not self.ready:
            return

        try:
            if self.streamer.is_playing():
                self.statuslog.info("Paused")
                self.streamer.pause()
            else:
                self.statuslog.info("Playing")
                self.streamer.resume()
        except AttributeError:
            pass

    async def stop(self):
        """The stop command"""

        self.logger.debug("stop command")

        # try:
        #     self.streamer.stop()
        # except AttributeError:
        #     pass
        try:
            await self.vclient.disconnect()
        except discord.DiscordException:
            pass

        self.vclient = None
        self.streamer = None

        self.ready = False
        self.mready = False
        self.vready = False

        self.nowplayinglog.info("---")
        self.statuslog.info("Stopped")

    async def destroy(self, reason=None):
        """The destroy command

        Args:
            reason (str): The reason for destroying the player; will be sent as a separate message after destruction
        """

        self.logger.debug("destroy command")

        # Voice destroy
        await self.stop()
        self.vready = False

        # Gui destroy
        await self.embed.delete()
        self.embed = None
        if reason:
            await client.send_typing(self.mchannel)
            await client.send_message(self.mchannel, reason)
        self.mready = False

        # Ready reset
        self.ready = False

    async def skip(self, query):
        """The skip command

        Args:
            query (int): The number of items to skip
        """

        if not self.ready:
            return

        if query == "":
            query = "1"

        try:
            num = int(query)
        except TypeError:
            self.statuslog.debug("Skip argument must be a number")
        except ValueError:
            self.statuslog.debug("Skip argument must be a number")
        else:
            self.statuslog.info("Skipping")

            for i in range(num - 1):
                try:
                    self.queue.pop(0)
                except IndexError:
                    pass

            try:
                self.streamer.stop()
            except AttributeError:
                pass

    async def shuffle(self):
        """The shuffle command"""

        self.logger.debug("shuffle command")

        if not self.ready:
            return

        self.statuslog.debug("Shuffling")

        random.shuffle(self.queue)

        self.update_queue()
        self.statuslog.debug("Shuffled")

    async def volume(self, value):
        """The volume command

        Args:
            value (str): The value to set the volume to
        """

        self.logger.debug("volume command")

        if not self.ready:
            return

        logger.debug("Volume command received")

        if value == '+':
            if self.volume < 100:
                self.statuslog.debug("Volume up")
                self.volume = (10 * (self.volume // 10)) + 10
                self.volumelog.info(str(self.volume))
                try:
                    self.streamer.volume = self.volume / 100
                except AttributeError:
                    pass
            else:
                self.statuslog.debug("Already at maximum volume")

        elif value == '-':
            if self.volume > 0:
                self.statuslog.debug("Volume down")
                self.volume = (10 * ((self.volume + 9) // 10)) - 10
                self.volumelog.info(str(self.volume))
                try:
                    self.streamer.volume = self.volume / 100
                except AttributeError:
                    pass
            else:
                self.statuslog.debug("Already at minimum volume")

        else:
            try:
                value = int(value)
            except ValueError:
                self.statuslog.debug("Volume argument must be +, -, or a %")
            else:
                if 0 <= value <= 200:
                    self.statuslog.debug("Setting volume")
                    self.volume = value
                    self.volumelog.info(str(self.volume))
                    try:
                        self.streamer.volume = self.volume / 100
                    except AttributeError:
                        pass
                else:
                    self.statuslog.debug("Volume must be between 0 and 200%")

    async def movehere(self, channel):
        """Moves the embed message to a new channel; can also be used to move the musicplayer to the front

        Args:
            channel (discord.Channel): The channel to move to
        """

        self.logger.debug("movehere command")

        if not self.ready:
            return

        await self.embed.delete()
        self.embed.channel = channel
        await self.embed.usend()

    # Methods
    async def vsetup(self, author):
        """Creates the voice client

        Args:
            author (discord.Member): The user that the voice ui will seek
        """

        self.logger.debug("Setting up voice")

        # Create voice client
        self.vchannel = author.voice.voice_channel
        if self.vchannel:
            self.statuslog.info("Connecting to voice")
            try:
                self.vclient = await client.join_voice_channel(self.vchannel)
            except discord.DiscordException:
                self.statuslog.error("I couldn't connect to the voice channel. Check my permissions.")
                return
            self.vready = True
        else:
            self.statuslog.error("You're not connected to a voice channel.")
            return

        # Mark ready
        self.vready = True

    async def msetup(self, text_channel):
        """Creates the gui

        Args:
            text_channel (discord.Channel): The channel for the embed ui to run in
        """

        self.logger.debug("Setting up gui")

        # Create gui
        self.mchannel = text_channel
        self.new_embed_ui()
        await self.embed.usend()
        self.statuslog.info("Loading buttons")
        for e in ("⏯", "⏹", "⏩", "🔀", "🔉", "🔊"):
            try:
                await client.add_reaction(self.embed.sent_embed, e)
            except discord.DiscordException:
                self.statuslog.error("I couldn't add the buttons. Check my permissions.")

        # Mark ready
        self.mready = True

    def new_embed_ui(self):
        """Create the embed UI object and save it to self"""

        self.logger.debug("Creating new embed ui object")

        # Initial queue display
        queue_display = []
        for i in range(self.queue_display):
            queue_display.append("{}: ---\n".format(str(i + 1)))

        # Initial datapacks
        datapacks = [
            ("Now playing", "---", False),
            ("Queue", "```{}```".format(''.join(queue_display)), False),
            ("Songs left in queue", "---", True),
            ("Volume", "10%", True),
            ("Status", "```---```", False)
        ]

        # Create embed UI object
        self.embed = ui_embed.UI(
            self.mchannel,
            "Music Player",
            "Press the buttons!",
            modulename=_data.modulename,
            creator=_data.creator,
            colour=0x88FF00,
            datapacks=datapacks
        )

        # Add handlers to update gui
        noformatter = logging.Formatter("{message}", style="{")
        codeformatter = logging.Formatter("```{message}```", style="{")
        volumeformatter = logging.Formatter("{message}%", style="{")

        nowplayinghandler = EmbedLogHandler(self.embed, 0)
        nowplayinghandler.setFormatter(noformatter)
        queuehandler = EmbedLogHandler(self.embed, 1)
        queuehandler.setFormatter(codeformatter)
        queuelenhandler = EmbedLogHandler(self.embed, 2)
        queuelenhandler.setFormatter(noformatter)
        volumehandler = EmbedLogHandler(self.embed, 3)
        volumehandler.setFormatter(volumeformatter)
        statushandler = EmbedLogHandler(self.embed, 4)
        statushandler.setFormatter(codeformatter)

        self.nowplayinglog.addHandler(nowplayinghandler)
        self.queuelog.addHandler(queuehandler)
        self.queuelenlog.addHandler(queuelenhandler)
        self.volumelog.addHandler(volumehandler)
        self.statuslog.addHandler(statushandler)

    def enqueue(self, query):
        """Queues songs based on either a YouTube search or a link

        Args:
            query (str): Either a search term or a link
        """

        self.logger.debug("Enqueueing from query")

        self.statuslog.info("Queueing {}".format(query))

        if "/" in query and "youtube" not in query:
            self.queue.append([query, query])
        else:
            self.queue = self.queue + api_youtube.get_ytvideos(query, self.statuslog)

        self.update_queue()

        self.statuslog.info("Queued {}".format(query))

    def update_queue(self):

        self.logger.debug("Updating queue display")

        queue_display = []
        for i in range(self.queue_display):
            try:
                if len(self.queue[i][1]) > 40:
                    songname = self.queue[i][1][:37] + "..."
                else:
                    songname = self.queue[i][1]
            except IndexError:
                songname = "---"
            queue_display.append("{}: {}\n".format(str(i + 1), songname))

        self.queuelog.info(''.join(queue_display))
        self.queuelenlog.info(str(len(self.queue)))

    async def vplay(self):

        self.logger.debug("Playing next in queue")

        # Queue has items
        if self.queue:
            self.statuslog.info("Loading next song")

            song = self.queue[0][0]
            songname = self.queue[0][1]

            self.queue.pop(0)

            try:
                result = await self.vclient.create_ytdl_player(song, after=lambda: runcoro(self.vafter()))
                self.streamer = result

                self.streamer.volume = self.volume / 100
                self.streamer.start()

                self.statuslog.info("Playing")
                self.nowplayinglog.info(songname)
            except:
                self.nowplayinglog.info("Error playing {}".format(songname))
                self.statuslog.error("Had a problem playing {}".format(songname))
                await self.vplay()

            self.update_queue()

        # Queue exhausted
        else:
            self.statuslog.info("Finished queue")
            await self.stop()

    async def vafter(self):
        """Function that is called after a song finishes playing"""

        self.logger.debug("Finished playing a song")

        if self.streamer.error is None:
            await self.vplay()
        else:
            await self.destroy()
            self.statuslog.critical("Encountered an error while playing :/")


class EmbedLogHandler(logging.Handler):
    def __init__(self, embed, line):
        """

        Args:
            embed (ui_embed.UI):
            line (int):
        """
        logging.Handler.__init__(self)

        self.embed = embed
        self.line = line

    def flush(self):
        try:
            asyncio.run_coroutine_threadsafe(self.embed.usend(), client.loop)
        except discord.DiscordException:
            return

    def emit(self, record):
        msg = self.format(record)
        try:
            self.embed.update_data(self.line, msg)
        except AttributeError:
            return
        self.flush()


def runcoro(async_function):
    """Runs an asynchronous function without needing to use await - useful for lambda

    Args:
        async_function (Coroutine): The asynchronous function to run
    """

    print(async_function)

    future = asyncio.run_coroutine_threadsafe(async_function, client.loop)
    result = future.result()
    return result
