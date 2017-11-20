"""The music player for the music module"""

import asyncio
import logging
import math
import random

import discord

from modis import datatools
from . import _data, api_youtube
from .._tools import ui_embed
from ..._client import client

logger = logging.getLogger(__name__)


class MusicPlayer:
    """The music player for the music module"""

    def __init__(self, server_id):
        """Locks onto a server for easy management of various UIs

        Args:
            server_id (str): The Discord ID of the server to lock on to
        """

        data = datatools.get_data()
        # Player variables
        self.server_id = server_id
        self.logger = logging.getLogger("{}.{}".format(__name__, self.server_id))

        # Voice variables
        self.vchannel = None
        self.vclient = None
        self.streamer = None
        self.queue = []
        self.prev_queue = []
        self.prev_queue_max = 50
        self.volume = 20
        # Timebar
        self.current_duration = 0
        self.timebar_length = 33
        self.vclient_starttime = None
        self.vclient_task = None
        self.pause_time = None
        self.prev_time = ""

        # Status variables
        self.mready = False
        self.vready = False
        self.state = 'off'

        # Gui variables
        self.mchannel = None
        self.embed = None
        self.queue_display = 9
        self.nowplayinglog = logging.getLogger("{}.{}.nowplaying".format(__name__, self.server_id))
        self.nowplayinglog.setLevel("DEBUG")
        self.timelog = logging.getLogger("{}.{}.time".format(__name__, self.server_id))
        self.timelog.setLevel("DEBUG")
        self.queuelog = logging.getLogger("{}.{}.queue".format(__name__, self.server_id))
        self.queuelog.setLevel("DEBUG")
        self.queuelenlog = logging.getLogger("{}.{}.queuelen".format(__name__, self.server_id))
        self.queuelenlog.setLevel("DEBUG")
        self.volumelog = logging.getLogger("{}.{}.volume".format(__name__, self.server_id))
        self.volumelog.setLevel("DEBUG")
        self.statuslog = logging.getLogger("{}.{}.status".format(__name__, self.server_id))
        self.statuslog.setLevel("DEBUG")
        self.statustimer = None

        # Get channel topic
        self.topic = ""
        self.topicchannel = None
        # Set topic channel
        if "topic_id" in data["discord"]["servers"][self.server_id][_data.modulename]:
            topic_id = data["discord"]["servers"][self.server_id][_data.modulename]["topic_id"]
            if topic_id is not None and topic_id != "":
                logger.debug("Topic channel id: {}".format(topic_id))
                self.topicchannel = client.get_channel(topic_id)
        # Get volume
        if "volume" in data["discord"]["servers"][self.server_id][_data.modulename]:
            self.volume = data["discord"]["servers"][self.server_id][_data.modulename]["volume"]
        else:
            self.write_volume()

    async def setup(self, author, text_channel):
        """
        The setup command

        Args:
            author (discord.Member): The member that called the command
            text_channel (discord.Channel): The channel where the command was called
        """

        if self.state == 'off':
            self.state = 'starting'
            await self.set_topic("")
            # Init the music player
            await self.msetup(text_channel)
            # Connect to voice
            await self.vsetup(author)

            # Mark as 'ready' if everything is ok
            self.state = 'ready' if self.mready and self.vready else 'off'

    async def play(self, author, text_channel, query, now=False, stop_current=False, shuffle=False):
        """
        The play command

        Args:
            author (discord.Member): The member that called the command
            text_channel (discord.Channel): The channel where the command was called
            query (str): The argument that was passed with the command
            now (bool): Whether to play next or at the end of the queue
            stop_current (bool): Whether to stop the currently playing song
            shuffle (bool): Whether to shuffle the queue after starting
        """
        await self.setup(author, text_channel)

        if self.state == 'ready':
            # Queue the song
            self.enqueue(query, now, shuffle)

            if stop_current:
                if self.streamer:
                    self.streamer.stop()

            # Start playing if not yet playing
            if self.streamer is None:
                await self.vplay()

    async def stop(self):
        """The stop command"""

        self.logger.debug("stop command")
        self.state = 'stopping'

        await self.set_topic("")
        self.nowplayinglog.debug("---")
        self.timelog.debug(self.make_timebar())
        self.prev_time = "---"
        self.statuslog.debug("Stopping")

        self.vready = False
        self.pause_time = None

        if self.vclient:
            try:
                await self.vclient.disconnect()
            except Exception as e:
                logger.error(e)
                pass

        if self.streamer:
            try:
                self.streamer.stop()
            except:
                pass

        self.vclient = None
        self.vchannel = None
        self.streamer = None
        self.queue = []
        self.prev_queue = []

        self.update_queue()

        self.nowplayinglog.debug("---")
        self.timelog.debug(self.make_timebar())
        self.prev_time = "---"
        self.statuslog.info("Stopped")
        self.state = 'off'

        if self.embed:
            await self.embed.usend()

    async def destroy(self):
        """Destroy the whole gui and music player"""

        self.logger.debug("destroy command")
        self.state = 'destroyed'

        await self.set_topic("")
        self.nowplayinglog.debug("---")
        self.timelog.debug(self.make_timebar())
        self.prev_time = "---"
        self.statuslog.debug("Destroying")

        self.mready = False
        self.vready = False
        self.pause_time = None

        if self.vclient:
            try:
                await self.vclient.disconnect()
            except Exception as e:
                logger.error(e)
                pass

        if self.streamer:
            try:
                self.streamer.stop()
            except:
                pass

        self.vclient = None
        self.vchannel = None
        self.streamer = None
        self.queue = []
        self.prev_queue = []

        if self.embed:
            await self.embed.delete()
            self.embed = None

    async def toggle(self):
        """Toggles between paused and not paused command"""

        self.logger.debug("toggle command")

        if not self.state == 'ready':
            return

        try:
            if self.streamer.is_playing():
                await self.pause()
            else:
                await self.resume()
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

                self.pause_time = self.vclient.loop.time()
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

                if self.pause_time is not None:
                    self.vclient_starttime += (self.vclient.loop.time() - self.pause_time)
                self.pause_time = None
        except Exception as e:
            logger.error(e)
            pass

    async def skip(self, query="1"):
        """The skip command

        Args:
            query (str): The number of items to skip
        """

        if not self.state == 'ready':
            logger.debug("Trying to skip from wrong state '{}'".format(self.state))
            return

        if query == "":
            query = "1"
        elif query == "all":
            query = str(len(self.queue) + 1)

        try:
            num = int(query)
        except TypeError:
            self.statuslog.error("Skip argument must be a number")
        except ValueError:
            self.statuslog.error("Skip argument must be a number")
        else:
            self.statuslog.info("Skipping")

            for i in range(num - 1):
                if len(self.queue) > 0:
                    self.queue.pop(0)

            try:
                self.streamer.stop()
            except Exception as e:
                logger.exception(e)

    async def remove(self, index=""):
        """
        The remove command

        Args:
            index (str): The index to remove
        """

        if not self.state == 'ready':
            logger.debug("Trying to remove from wrong state '{}'".format(self.state))
            return

        if index == "":
            self.statuslog.error("Must provide index to remove")
            return
        elif index == "all":
            self.queue = []
            self.prev_queue = []
            self.update_queue()
            self.statuslog.info("Removed all songs")
            return

        try:
            num = int(index) - 1
        except TypeError:
            self.statuslog.error("Remove index must be a number")
        except ValueError:
            self.statuslog.error("Remove index must be a number")
        else:
            if num < 0 or num >= len(self.queue):
                if len(self.queue) == 0:
                    self.statuslog.warning("No songs in queue")
                elif len(self.queue) == 1:
                    self.statuslog.error("Index must be 1 (only 1 song in queue)")
                else:
                    self.statuslog.error("Index must be between 1 and {}".format(len(self.queue)))
                return

            self.statuslog.info("Removed {}".format(self.queue[num][1]))
            self.queue.pop(num)
            self.update_queue()

    async def rewind(self, query="1"):
        """
        The rewind command

        Args:
            query (str): The number of items to skip
        """

        if not self.state == 'ready':
            logger.debug("Trying to rewind from wrong state '{}'".format(self.state))
            return

        if query == "":
            query = "1"

        try:
            num = int(query)
        except TypeError:
            self.statuslog.error("Rewind argument must be a number")
        except ValueError:
            self.statuslog.error("Rewind argument must be a number")
        else:
            if len(self.prev_queue) == 0:
                self.statuslog.error("No songs to rewind")
                return

            if num > len(self.prev_queue):
                self.statuslog.warning("Rewinding to start")
            else:
                self.statuslog.info("Rewinding")

            for i in range(num + 1):
                if len(self.prev_queue) > 0:
                    self.queue.insert(0, self.prev_queue.pop())

            try:
                self.streamer.stop()
            except Exception as e:
                logger.exception(e)

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
                self.statuslog.warning("Already at maximum volume")

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
                self.statuslog.warning("Already at minimum volume")

        else:
            try:
                value = int(value)
            except ValueError:
                self.statuslog.error("Volume argument must be +, -, or a %")
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
                    self.statuslog.error("Volume must be between 0 and 200")

        self.write_volume()

    def write_volume(self):
        # Update the volume
        data = datatools.get_data()
        data["discord"]["servers"][self.server_id][_data.modulename]["volume"] = self.volume
        datatools.write_data(data)

    async def movehere(self, channel):
        """Moves the embed message to a new channel; can also be used to move the musicplayer to the front

        Args:
            channel (discord.Channel): The channel to move to
        """

        self.logger.debug("movehere command")

        # Delete the old message
        await self.embed.delete()
        # Set the channel to this channel
        self.embed.channel = channel
        # Send a new embed to the channel
        await self.embed.send()
        # Re-add the reactions
        await self.add_reactions()

        self.statuslog.info("Moved to front")

    async def set_topic_channel(self, channel):
        """Set the topic channel for this server"""
        data = datatools.get_data()
        data["discord"]["servers"][self.server_id][_data.modulename]["topic_id"] = channel.id
        datatools.write_data(data)

        self.topicchannel = channel
        await self.set_topic(self.topic)

    async def clear_topic_channel(self):
        """Set the topic channel for this server"""
        try:
            if self.topicchannel:
                await client.edit_channel(self.topicchannel, topic="")
        except Exception as e:
            logger.exception(e)

        self.topicchannel = None
        logger.debug("Clearing topic channel")

        data = datatools.get_data()
        data["discord"]["servers"][self.server_id][_data.modulename]["topic_id"] = ""
        datatools.write_data(data)

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
            except discord.ClientException as e:
                logger.exception(e)
                self.statuslog.warning("I'm already connected to a voice channel.")
                return
            except discord.opus.OpusNotLoaded as e:
                logger.exception(e)
                logger.error("This is an error with your FFmpeg setup.")
                self.statuslog.error("Could not load Opus.")
                return
            except discord.DiscordException as e:
                logger.exception(e)
                self.statuslog.error("I couldn't connect to the voice channel. Check my permissions.")
                return
            except Exception as e:
                self.statuslog.error("Internal error connecting to voice, disconnecting.")
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
        await self.embed.send()
        await self.embed.usend()
        await self.add_reactions()

        self.mready = True

    def new_embed_ui(self):
        """Create the embed UI object and save it to self"""

        self.logger.debug("Creating new embed ui object")

        # Initial queue display
        queue_display = []
        for i in range(self.queue_display):
            queue_display.append("{}. ---\n".format(str(i + 1)))

        # Initial datapacks
        datapacks = [
            ("Now playing", "---", False),
            ("Time", "```http\n" + self.make_timebar() + "\n```", True),
            ("Queue", "```md\n{}\n```".format(''.join(queue_display)), False),
            ("Songs left in queue", "---", True),
            ("Volume", "{}%".format(self.volume), True),
            ("Status", "```---```", False)
        ]

        # Create embed UI object
        self.embed = ui_embed.UI(
            self.mchannel,
            "Music Player",
            "Press the buttons!",
            modulename=_data.modulename,
            creator=_data.creator,
            colour=_data.modulecolor,
            datapacks=datapacks
        )

        # Add handlers to update gui
        noformatter = logging.Formatter("{message}", style="{")
        timeformatter = logging.Formatter("```http\n{message}\n```", style="{")
        mdformatter = logging.Formatter("```md\n{message}\n```", style="{")
        statusformatter = logging.Formatter("```__{levelname}__\n{message}\n```", style="{")
        volumeformatter = logging.Formatter("{message}%", style="{")

        nowplayinghandler = EmbedLogHandler(self, self.embed, 0)
        nowplayinghandler.setFormatter(noformatter)
        timehandler = EmbedLogHandler(self, self.embed, 1)
        timehandler.setFormatter(timeformatter)
        queuehandler = EmbedLogHandler(self, self.embed, 2)
        queuehandler.setFormatter(mdformatter)
        queuelenhandler = EmbedLogHandler(self, self.embed, 3)
        queuelenhandler.setFormatter(noformatter)
        volumehandler = EmbedLogHandler(self, self.embed, 4)
        volumehandler.setFormatter(volumeformatter)
        statushandler = EmbedLogHandler(self, self.embed, 5)
        statushandler.setFormatter(statusformatter)

        self.nowplayinglog.addHandler(nowplayinghandler)
        self.timelog.addHandler(timehandler)
        self.queuelog.addHandler(queuehandler)
        self.queuelenlog.addHandler(queuelenhandler)
        self.volumelog.addHandler(volumehandler)
        self.statuslog.addHandler(statushandler)

    async def add_reactions(self):
        """Adds the reactions buttons to the current message"""
        self.statuslog.info("Loading buttons")
        for e in ("⏯", "⏹", "⏭", "🔀", "🔉", "🔊"):
            try:
                if self.embed is not None:
                    await client.add_reaction(self.embed.sent_embed, e)
            except discord.DiscordException as e:
                logger.exception(e)
                self.statuslog.error("I couldn't add the buttons. Check my permissions.")
            except Exception as e:
                logger.exception(e)

    def enqueue(self, query, front=False, shuffle=False):
        """Queues songs based on either a YouTube search or a link

        Args:
            query (str): Either a search term or a link
            front (bool): Whether to enqueue at the front or the end
            shuffle (bool): Whether to shuffle the added songs
        """

        if self.state != 'ready':
            logger.error("Attempt to queue song from wrong state ('{}'), must be 'ready'.".format(self.state))
            return

        self.logger.debug("Enqueueing from query")

        self.statuslog.info("Queueing {}".format(query))

        yt_videos = api_youtube.parse_query(query, self.statuslog)
        if shuffle:
            random.shuffle(yt_videos)

        if front:
            self.queue = yt_videos + self.queue
        else:
            self.queue = self.queue + yt_videos

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
            queue_display.append("{}. {}\n".format(str(i + 1), songname))

        self.queuelog.debug(''.join(queue_display))
        self.queuelenlog.debug(str(len(self.queue)))

    async def set_topic(self, topic):
        """Sets the topic for the topic channel"""
        self.topic = topic
        try:
            if self.topicchannel:
                await client.edit_channel(self.topicchannel, topic=topic)
        except Exception as e:
            logger.exception(e)

    @asyncio.coroutine
    def time_loop(self):
        while True:
            if self.pause_time is None:
                diff = self.vclient.loop.time() - self.vclient_starttime

                if self.current_duration > 0:
                    time_counts = int(math.ceil((diff / self.current_duration) * self.timebar_length))
                    if time_counts > self.timebar_length:
                        time_counts = self.timebar_length

                    time_bar = self.make_timebar(time_counts, self.current_duration)
                else:
                    time_bar = self.make_timebar()

                if time_bar != self.prev_time:
                    self.timelog.debug(time_bar)
                    self.prev_time = time_bar

            yield from asyncio.sleep(5)

    async def vplay(self):
        if self.state != 'ready':
            logger.error("Attempt to play song from wrong state ('{}'), must be 'ready'.".format(self.state))
            return

        self.state = "starting streamer"
        self.logger.debug("Playing next in queue")

        self.pause_time = None

        # Queue has items
        if self.queue:
            self.statuslog.info("Loading next song")

            song = self.queue[0][0]
            songname = self.queue[0][1]

            self.prev_queue.append(self.queue.pop(0))
            while len(self.prev_queue) > self.prev_queue_max:
                self.prev_queue.pop(0)

            try:
                bopt_list = ["-reconnect 1", "-reconnect_streamed 1", "-reconnect_delay_max 15", "-reconnect_at_eof 1",
                             "-timeout 15", "-multiple_requests 1"]
                boptions = " {}".format(' '.join(bopt_list))
                logger.debug("FFmpeg options: {}".format(boptions))

                ytoptions = {
                    "format": "bestaudio/best",
                    "extractaudio": True,
                    "audioformat": "mp3",
                    "noplaylist": True,
                    "socket_timeout": 15,
                    "nocheckcertificate": True,
                    "logger": logger
                }

                self.streamer = await self.vclient.create_ytdl_player(song,
                                                                      ytdl_options=ytoptions,
                                                                      after=self.vafter_ts,
                                                                      before_options=boptions)
                self.state = "ready"

                self.current_duration = self.streamer.duration

                self.vclient_starttime = self.vclient.loop.time()
                self.vclient_task = asyncio.Task(self.time_loop())

                self.streamer.volume = self.volume / 100
                self.streamer.start()

                nowplaying = "Playing {}".format(self.streamer.title)
                self.statuslog.debug("Playing")
                await self.set_topic(nowplaying)
                self.nowplayinglog.debug(nowplaying)
            except Exception as e:
                await self.set_topic("")
                self.nowplayinglog.info("Error playing {}".format(songname))
                self.timelog.debug(self.make_timebar())
                self.prev_time = "---"
                self.statuslog.error("Had a problem playing {}".format(songname))
                logger.exception(e)

                try:
                    self.streamer.stop()
                except Exception as e:
                    logger.exception(e)

                self.streamer = None
                self.state = "ready"
                await self.vplay()

            self.update_queue()

        # Queue exhausted
        else:
            self.statuslog.info("Finished Queue")
            self.state = "ready"

            self.update_queue()

            await self.stop()

    def duration_to_string(self, duration):
        """
        Converts a duration to a string

        Args:
            duration (int): The duration in seconds to convert

        Returns s (str): The duration as a string
        """

        m, s = divmod(duration, 60)
        h, m = divmod(m, 60)
        return "%d:%02d:%02d" % (h, m, s)

    def make_timebar(self, progress=0, duration=0):
        """
        Makes a new time bar string

        Args:
            progress: The number of 'dots' in the time bar
            duration: The duration of the current song

        Returns:
            timebar (str): The time bar string
        """

        if progress > self.timebar_length:
            progress = self.timebar_length

        duration_string = self.duration_to_string(duration)
        if duration > 0:
            bar = "|" + ("-" * progress) + (" " * (self.timebar_length - progress)) + "|"
            time_bar = "{} {}".format(bar, duration_string)
        else:
            time_bar = duration_string

        return time_bar

    def vafter_ts(self):
        """Function that is called after a song finishes playing"""
        logger.debug("Song finishing")
        future = asyncio.run_coroutine_threadsafe(self.vafter(), client.loop)
        try:
            future.result()
        except Exception as e:
            logger.exception(e)

    async def vafter(self):
        """Function that is called after a song finishes playing"""

        self.logger.debug("Finished playing a song")
        if self.state != 'ready':
            self.logger.debug("Returning because player is in state {}".format(self.state))
            return

        self.current_duration = 0
        self.pause_time = None

        if self.vclient_task:
            loop = asyncio.get_event_loop()
            loop.call_soon(self.vclient_task.cancel)
            self.vclient_task = None

        try:
            if self.streamer.error is None:
                await self.vplay()
            else:
                await self.destroy()
                self.statuslog.error(self.streamer.error)
                self.statuslog.error("Encountered an error")
        except Exception as e:
            logger.exception(e)
            try:
                await self.destroy()
            except Exception as e:
                logger.exception(e)


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
        except Exception as e:
            logger.exception(e)
            return

    async def usend_when_ready(self):
        if self.embed is not None:
            await self.embed.usend()

    def emit(self, record):
        msg = self.format(record)
        msg = msg.replace("__DEBUG__", "").replace("__INFO__", "")
        msg = msg.replace("__WARNING__", "css").replace("__ERROR__", "http").replace("__CRITICAL__", "http")

        try:
            self.embed.update_data(self.line, msg)
        except AttributeError:
            return
        self.flush()
