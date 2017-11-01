import logging

from ..._client import client
from .._tools import ui_embed

from . import api_youtube
from . import _data

import discord
import asyncio
import random

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

        # Voice variables
        self.vchannel = None
        self.vclient = None
        self.streamer = None
        self.queue = []
        self.volume = 20

        # Status variables
        self.mready = False
        self.vready = False
        self.state = 'off'

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

    async def setup(self, author, text_channel):
        """
        The setup command

        Args:
            author (discord.Member): The member that called the command
            text_channel (discord.Channel): The channel where the command was called
        """
        if self.state == 'off':
            self.state = 'starting'
            # Init the music player
            await self.msetup(text_channel)
            # Connect to voice
            await self.vsetup(author)

            # Mark as 'ready' if everything is ok
            self.state = 'ready' if self.mready and self.vready else 'error'

            if self.state != 'ready':
                try:
                    await self.stop()
                except:
                    pass

    async def play(self, author, text_channel, query):
        """
        The play command

        Args:
            author (discord.Member): The member that called the command
            text_channel (discord.Channel): The channel where the command was called
            query (str): The argument that was passed with the command
        """
        await self.setup(author, text_channel)

        if self.state == 'ready':
            # Queue the song
            self.enqueue(query)

            # Start playing if not yet playing
            if self.streamer is None:
                await self.vplay()

    async def stop(self):
        """The stop command"""

        self.logger.debug("stop command")
        self.state = 'stopping'

        self.nowplayinglog.info("---")
        self.statuslog.info("Stopping")

        if self.embed:
            await self.embed.usend()

        self.mready = False
        self.vready = False

        try:
            self.streamer.stop()
        except:
            pass

        try:
            await self.vclient.disconnect()
        except Exception as e:
            logger.error(e)
            pass

        self.vclient = None
        self.streamer = None

        self.nowplayinglog.info("---")
        self.statuslog.info("Stopped")
        self.state = 'off'

    async def destroy(self):
        """Destroy the whole gui and music player"""

        self.logger.debug("destroy command")
        self.state = 'destroying'

        self.nowplayinglog.info("---")
        self.statuslog.info("Destroying")

        self.mready = False
        self.vready = False

        try:
            await self.vclient.disconnect()
        except Exception as e:
            logger.error(e)
            pass

        self.vclient = None
        self.vchannel = None
        self.streamer = None

        if self.embed:
            await self.embed.destroy()
            self.embed = None

        self.state = 'destroyed'

    async def toggle(self):
        """Toggles between paused and not paused command"""

        self.logger.debug("toggle command")

        if not self.state == 'ready':
            return

        try:
            if self.streamer.is_playing():
                self.statuslog.info("Paused")
                self.streamer.pause()
            else:
                self.statuslog.info("Playing")
                self.streamer.resume()
        except Exception as e:
            logger.error(e)
            pass

    async def pause(self):
        """Pauses playback if playing"""

        self.logger.debug("pause command")

        if not self.state == 'ready':
            return

        try:
            if self.streamer.is_playing():
                self.statuslog.info("Paused")
                self.streamer.pause()
        except Exception as e:
            logger.error(e)
            pass

    async def resume(self):
        """Resumes playback if paused"""

        self.logger.debug("toggle command")

        if not self.state == 'ready':
            return

        try:
            if not self.streamer.is_playing():
                self.statuslog.info("Playing")
                self.streamer.resume()
        except Exception as e:
            logger.error(e)
            pass

    async def skip(self, query="1"):
        """The skip command

        Args:
            query (int): The number of items to skip
        """

        if not self.state == 'ready':
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

        if not self.state == 'ready':
            return

        self.statuslog.debug("Shuffling")

        random.shuffle(self.queue)

        self.update_queue()
        self.statuslog.debug("Shuffled")

    async def setvolume(self, value):
        """The volume command

        Args:
            value (str): The value to set the volume to
        """

        self.logger.debug("volume command")

        if self.state != 'ready':
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

        if self.state != 'ready':
            return

        await self.embed.delete()
        self.embed.channel = channel
        await self.embed.usend()
        await self.add_reactions()

    # Methods
    async def vsetup(self, author):
        """Creates the voice client

        Args:
            author (discord.Member): The user that the voice ui will seek
        """

        if self.vready:
            logger.error("Attempt to init voice when already initialised")
            return

        if self.state != 'starting':
            logger.error("Attempt to init from wrong state ('{}'), must be 'starting'.".format(self.state))
            return

        self.logger.debug("Setting up voice")

        # Create voice client
        self.vchannel = author.voice.voice_channel
        if self.vchannel:
            self.statuslog.info("Connecting to voice")
            try:
                self.vclient = await client.join_voice_channel(self.vchannel)
            except discord.ClientException:
                self.statuslog.error("I'm already connected to a voice channel.")
                return
            except discord.DiscordException:
                self.statuslog.error("I couldn't connect to the voice channel. Check my permissions.")
                return
            except Exception as e:
                self.statuslog.error("Internal error connecting to voice, disconnecting")
                logger.error("Error connecting to voice {}".format(e))
                return
        else:
            self.statuslog.error("You're not connected to a voice channel.")
            return

        self.vready = True

    async def msetup(self, text_channel):
        """Creates the gui

        Args:
            text_channel (discord.Channel): The channel for the embed ui to run in
        """

        if self.mready:
            logger.error("Attempt to init music when already initialised")
            return

        if self.state != 'starting':
            logger.error("Attempt to init from wrong state ('{}'), must be 'starting'.".format(self.state))
            return

        self.logger.debug("Setting up gui")

        # Create gui
        self.mchannel = text_channel
        self.new_embed_ui()
        await self.embed.usend()
        await self.add_reactions()

        self.mready = True

    def new_embed_ui(self):
        """Create the embed UI object and save it to self"""

        if self.state != 'starting':
            logger.error("Attempt to create UI from wrong state ('{}'), must be 'starting'.".format(self.state))
            return

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
            ("Volume", "{}%".format(self.volume), True),
            ("Status", "```---```", False)
        ]

        # Create embed UI object
        if not self.embed:
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

        nowplayinghandler = EmbedLogHandler(self, self.embed, 0)
        nowplayinghandler.setFormatter(noformatter)
        queuehandler = EmbedLogHandler(self, self.embed, 1)
        queuehandler.setFormatter(codeformatter)
        queuelenhandler = EmbedLogHandler(self, self.embed, 2)
        queuelenhandler.setFormatter(noformatter)
        volumehandler = EmbedLogHandler(self, self.embed, 3)
        volumehandler.setFormatter(volumeformatter)
        statushandler = EmbedLogHandler(self, self.embed, 4)
        statushandler.setFormatter(codeformatter)

        self.nowplayinglog.addHandler(nowplayinghandler)
        self.queuelog.addHandler(queuehandler)
        self.queuelenlog.addHandler(queuelenhandler)
        self.volumelog.addHandler(volumehandler)
        self.statuslog.addHandler(statushandler)

    async def add_reactions(self):
        """Adds the reactions buttons to the current message"""
        self.statuslog.info("Loading buttons")
        for e in ("⏯", "⏹", "⏭", "🔀", "🔉", "🔊"):
            try:
                await client.add_reaction(self.embed.sent_embed, e)
            except discord.DiscordException:
                self.statuslog.error("I couldn't add the buttons. Check my permissions.")
            except Exception as e:
                logger.exception(e)

    def enqueue(self, query):
        """Queues songs based on either a YouTube search or a link

        Args:
            query (str): Either a search term or a link
        """

        if self.state != 'ready':
            logger.error("Attempt to queue song from wrong state ('{}'), must be 'ready'.".format(self.state))
            return

        self.logger.debug("Enqueueing from query")

        self.statuslog.info("Queueing {}".format(query))

        if "/" in query and "youtube" not in query:
            self.queue.append([query, query])
        else:
            self.queue = self.queue + api_youtube.get_ytvideos(query, self.statuslog)

        self.update_queue()

        self.statuslog.info("Queued {}".format(query))

    def update_queue(self):
        """ Updates the queue in the music player """

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
        if self.state != 'ready':
            logger.error("Attempt to play song from wrong state ('{}'), must be 'ready'.".format(self.state))
            return

        if self.streamer is not None:
            logger.error("Streamer already exists")
            return

        self.state = "starting streamer"

        self.logger.debug("Playing next in queue")

        # Queue has items
        if self.queue:
            self.statuslog.info("Loading next song")

            song = self.queue[0][0]
            songname = self.queue[0][1]

            self.queue.pop(0)

            try:
                self.streamer = await self.vclient.create_ytdl_player(song, after=lambda: runcoro(self.vafter()))
                self.state = "ready"

                self.streamer.volume = self.volume / 100
                self.streamer.start()

                self.statuslog.info("Playing")
                self.nowplayinglog.info(songname)
            except Exception as e:
                self.nowplayinglog.info("Error playing {}".format(songname))
                self.statuslog.error("Had a problem playing {}".format(songname))
                logger.exception(e)

                try:
                    self.streamer.stop()
                except:
                    pass

                self.streamer = None
                self.state = "ready"
                await self.vplay()

            self.update_queue()

        # Queue exhausted
        else:
            self.statuslog.info("Finished queue")
            self.state = "ready"
            await self.stop()

    async def vafter(self):
        """Function that is called after a song finishes playing"""

        if self.state != 'ready':
            return

        self.logger.debug("Finished playing a song")

        if self.streamer.error is None:
            self.streamer = None
            await self.vplay()
        else:
            await self.destroy()
            self.statuslog.critical("Encountered an error while playing :/")


class EmbedLogHandler(logging.Handler):
    def __init__(self, music_player, embed, line):
        """

        Args:
            embed (ui_embed.UI):
            line (int):
        """
        logging.Handler.__init__(self)

        self.music_player = music_player
        self.embed = embed
        self.line = line

    def flush(self):
        try:
            asyncio.run_coroutine_threadsafe(self.usend_when_ready(), client.loop)
        except discord.DiscordException:
            return

    async def usend_when_ready(self):
        if not self.music_player.state != 'destroying' and self.embed is not None:
            await self.embed.usend()

    def emit(self, record):
        msg = self.format(record)
        try:
            self.embed.update_data(self.line, msg)
        except AttributeError:
            return
        self.flush()


def runcoro(async_function):
    """
    Runs an asynchronous function without needing to use await - useful for lambda

    Args:
        async_function (Coroutine): The asynchronous function to run
    """

    print(async_function)

    future = asyncio.run_coroutine_threadsafe(async_function, client.loop)
    result = future.result()
    return result
