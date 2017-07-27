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
        self.statustimer = None
        self.mready = False

    # Commands
    async def setup(self, author, text_channel):
        """Creates the UIs

        Args:
            author (discord.Member): The user that the voice ui will seek
            text_channel (discord.Channel): The channel for the embed ui to run in
        """

        # Create gui
        self.mchannel = text_channel
        self.new_embed_ui()
        self.embed.usend()
        self.statuslog.info("Loading buttons")
        for e in ("⏯", "⏹", "⏩", "🔀", "🔉", "🔊"):
            try:
                await client.add_reaction(self.embed.sent_embed, e)
            except discord.DiscordException:
                self.statuslog.error("I couldn't add the buttons. Check my permissions.")

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
        self.ready = True

    async def play(self, author, text_channel, query):
        """The play command

        Args:
            author (discord.Member): The member that called the command
            text_channel (discord.Channel): The channel where the command was called
            query (str): The argument that was passed with the command
        """

        # Init music player if not done
        if not self.ready:
            await self.setup(author, text_channel)

        if self.ready:
            # Add the query to queue
            self.enqueue(query)

            # Start playing if not yet playing
            if self.streamer is None:
                self.vplay()

    async def pause(self):
        """The pause command"""

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

        try:
            self.streamer.stop()
        except AttributeError:
            pass
        try:
            await self.vclient.disconnect()
        except discord.DiscordException:
            pass

        self.vclient = None
        self.streamer = None

        self.vready = False

        self.statuslog.info("Stopped")

    async def destroy(self, reason=None):
        """The destroy command

        Args:
            reason (str): The reason for destroying the player; will be sent as a separate message after destruction
        """

        logger.debug("Destroy command received")

        # Voice destroy
        self.queue = []
        self.stop()
        self.vready = False

        # Gui destroy
        await self.embed.delete()
        if reason:
            await client.send_typing(self.mchannel)
            await client.send_message(self.mchannel, reason)
        self.new_embed_ui()
        self.mready = False

        # Ready reset
        self.ready = False

    async def skip(self, query=1):
        """The skip command

        Args:
            query (int): The number of items to skip
        """

        if not self.ready:
            return

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

        if not self.ready:
            return

        await self.embed.delete()
        self.embed.channel = channel
        await self.embed.usend()

    # Methods
    def new_embed_ui(self):
        """Create the embed UI object and save it to self"""

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
        embed = ui_embed.UI(
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
        nowplayingformatter = logging.Formatter("Now playing {message}", style="{")
        volumeformatter = logging.Formatter("{message}%", style="{")

        nowplayinghandler = EmbedLogHandler(embed, 0)
        nowplayinghandler.setFormatter(nowplayingformatter)
        queuehandler = EmbedLogHandler(embed, 1)
        queuehandler.setFormatter(codeformatter)
        queuelenhandler = EmbedLogHandler(embed, 2)
        queuelenhandler.setFormatter(noformatter)
        volumehandler = EmbedLogHandler(embed, 3)
        volumehandler.setFormatter(volumeformatter)
        statushandler = EmbedLogHandler(embed, 4)
        statushandler.setFormatter(codeformatter)

        self.nowplayinglog.addHandler(nowplayinghandler)
        self.queuelog.addHandler(queuehandler)
        self.queuelenlog.addHandler(queuelenhandler)
        self.volumelog.addHandler(volumehandler)
        self.statuslog.addHandler(statushandler)

        return embed

    def enqueue(self, query):
        """Queues songs based on either a YouTube search or a link

        Args:
            query (str): Either a search term or a link
        """

        self.statuslog.info("Queueing {}".format(query))

        if "/" in query and "youtube" not in query:
            self.queue.append([query, query])
        else:
            self.queue = self.queue + api_youtube.get_ytvideos(query, self.statuslog)

        self.update_queue()

    def update_queue(self):
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
        # Queue has items
        if self.queue:
            self.statuslog.info("Loading next song")

            song = self.queue[0][0]
            songname = self.queue[0][1]

            try:
                self.streamer = await self.vclient.create_ytdl_player(song, after=lambda: runcoro(self.vafter()))

                self.streamer.volume = self.volume / 100
                self.streamer.start()
            except:
                self.statuslog.error("Had a problem playing {}".format(songname))

            self.queue.pop(0)

            self.update_queue()
            self.statuslog.info("Playing")
            self.nowplayinglog.info(songname)

        # Queue exhausted
        else:
            self.statuslog.info("Finished queue")
            await self.stop()

    async def vafter(self):
        """Function that is called after a song finishes playing"""

        if self.streamer.error is None:
            await self.vplay()
        else:
            await self.destroy()
            self.statuslog.critical("Encountered an error while playing :/")


class EmbedLogHandler(logging.Handler):
    def __init__(self, embed, line):
        logging.Handler.__init__(self)

        self.embed = embed
        self.line = line

    def flush(self):
        try:
            runcoro(self.embed.usend())
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

    future = asyncio.run_coroutine_threadsafe(async_function, client.loop)
    result = future.result()
    return result
