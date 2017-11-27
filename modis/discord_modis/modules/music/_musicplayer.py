"""The music player for the music module"""

import asyncio
import json
import logging
import os
import random
import shutil
import threading

import discord
import youtube_dl

from modis import datatools
from . import _data, _timebar, api_music, ui_embed
from .._tools import ui_embed as ui_embed_tools
from ..._client import client

logger = logging.getLogger(__name__)

_dir = os.getcwd()
_root_songcache_dir = "{}/.songcache".format(_dir)


def clear_cache_root():
    """Clears everything in the song cache"""
    logger.debug("Clearing root cache")
    if os.path.isdir(_root_songcache_dir):
        for filename in os.listdir(_root_songcache_dir):
            file_path = os.path.join(_root_songcache_dir, filename)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except PermissionError:
                pass
            except Exception as e:
                logger.exception(e)
    logger.debug("Root cache cleared")


def _match_func(info_dict):
    if "is_live" not in info_dict or not info_dict["is_live"]:
        if "duration" in info_dict and info_dict["duration"] and info_dict["duration"] > 0:
            return None
    raise DownloadStreamException("Cannot download stream")


file_format = "%(title)s"

ytdl_formats = [
    "worstaudio",
    "worst",
]

ydl_opts = {
    "format": '/'.join(ytdl_formats),
    "audio_format": "mp3",
    "extract_audio": True,
    "restrict_filenames": True,
    "writeinfojson": True,
    "nooverwrites": True,
    "noplaylist": True,
    "socket_timeout": 30,
    "max_downloads": 1,
    "match_filter": _match_func
}


class DownloadStreamException(BaseException):
    """Called when trying to download a stream"""


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
        # File variables
        self.songcache_dir = "{}/{}".format(_root_songcache_dir, self.server_id)
        self.songcache_next_dir = "{}/{}/next".format(_root_songcache_dir, self.server_id)
        self.output_format = "{}/{}".format(self.songcache_dir, file_format)
        self.output_format_next = "{}/{}".format(self.songcache_next_dir, file_format)

        # Voice variables
        self.vchannel = None
        self.vclient = None
        self.streamer = None
        self.current_duration = 0
        self.current_download_elapsed = 0
        self.is_live = False
        self.queue = []
        self.prev_queue = []
        self.prev_queue_max = 500
        self.volume = 20
        # Timebar
        self.vclient_starttime = None
        self.vclient_task = None
        self.pause_time = None
        self.prev_time = ""
        # Loop
        self.loop_type = 'off'

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
        self.nowplayingauthorlog = logging.getLogger("{}.{}.nowplayingauthor".format(__name__, self.server_id))
        self.nowplayingauthorlog.setLevel("DEBUG")
        self.nowplayingsourcelog = logging.getLogger("{}.{}.nowplayingsource".format(__name__, self.server_id))
        self.nowplayingsourcelog.setLevel("DEBUG")
        self.timelog = logging.getLogger("{}.{}.time".format(__name__, self.server_id))
        self.timelog.setLevel("DEBUG")
        self.timelog.propagate = False
        self.queuelog = logging.getLogger("{}.{}.queue".format(__name__, self.server_id))
        self.queuelog.setLevel("DEBUG")
        self.queuelog.propagate = False
        self.queuelenlog = logging.getLogger("{}.{}.queuelen".format(__name__, self.server_id))
        self.queuelenlog.setLevel("DEBUG")
        self.queuelenlog.propagate = False
        self.volumelog = logging.getLogger("{}.{}.volume".format(__name__, self.server_id))
        self.volumelog.setLevel("DEBUG")
        self.statuslog = logging.getLogger("{}.{}.status".format(__name__, self.server_id))
        self.statuslog.setLevel("DEBUG")
        self.statustimer = None

        # Clear the cache
        self.clear_cache()

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

    async def play(self, author, text_channel, query, index=None, stop_current=False, shuffle=False):
        """
        The play command

        Args:
            author (discord.Member): The member that called the command
            text_channel (discord.Channel): The channel where the command was called
            query (str): The argument that was passed with the command
            index (str): Whether to play next or at the end of the queue
            stop_current (bool): Whether to stop the currently playing song
            shuffle (bool): Whether to shuffle the queue after starting
        """

        if self.state == 'off':
            self.state = 'starting'
            self.prev_queue = []
            await self.set_topic("")
            # Init the music player
            await self.msetup(text_channel)
            # Queue the song
            await self.enqueue(query, index, stop_current, shuffle)
            # Connect to voice
            await self.vsetup(author)

            # Mark as 'ready' if everything is ok
            self.state = 'ready' if self.mready and self.vready else 'off'
        else:
            # Queue the song
            await self.enqueue(query, index, stop_current, shuffle)

        if self.state == 'ready':
            if self.streamer is None:
                await self.vplay()

    async def stop(self, log_stop=False):
        """The stop command"""

        self.logger.debug("stop command")
        self.state = 'stopping'

        await self.set_topic("")
        self.nowplayinglog.debug("---")
        self.nowplayingauthorlog.debug("---")
        self.nowplayingsourcelog.debug("---")
        self.timelog.debug(_timebar.make_timebar())
        self.prev_time = "---"

        if log_stop:
            self.statuslog.debug("Stopping")

        self.vready = False
        self.pause_time = None
        self.loop_type = 'off'

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
        self.current_duration = 0
        self.current_download_elapsed = 0
        self.is_live = False
        self.queue = []
        self.prev_queue = []

        self.update_queue()

        self.nowplayinglog.debug("---")
        self.nowplayingauthorlog.debug("---")
        self.nowplayingsourcelog.debug("---")
        self.timelog.debug(_timebar.make_timebar())
        self.prev_time = "---"

        self.clear_cache()

        if log_stop:
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
        self.nowplayingauthorlog.debug("---")
        self.nowplayingsourcelog.debug("---")
        self.timelog.debug(_timebar.make_timebar())
        self.prev_time = "---"
        self.statuslog.debug("Destroying")

        self.mready = False
        self.vready = False
        self.pause_time = None
        self.loop_type = 'off'

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
        self.current_duration = 0
        self.current_download_elapsed = 0
        self.is_live = False
        self.queue = []
        self.prev_queue = []

        if self.embed:
            await self.embed.delete()
            self.embed = None

        self.clear_cache()

    async def toggle(self):
        """Toggles between pause and resume command"""

        self.logger.debug("toggle command")

        if not self.state == 'ready':
            return

        if self.streamer is None:
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

        if self.streamer is None:
            return

        try:
            if self.streamer.is_playing():
                self.streamer.pause()
                self.pause_time = self.vclient.loop.time()
                self.statuslog.info("Paused")
        except Exception as e:
            logger.error(e)
            pass

    async def resume(self):
        """Resumes playback if paused"""

        self.logger.debug("resume command")

        if not self.state == 'ready':
            return

        if self.streamer is None:
            return

        try:
            if not self.streamer.is_playing():
                play_state = "Streaming" if self.is_live else "Playing"
                self.statuslog.info(play_state)
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
                    self.prev_queue.append(self.queue.pop(0))

            try:
                self.streamer.stop()
            except Exception as e:
                logger.exception(e)

    async def remove(self, index=""):
        """
        The remove command

        Args:
            index (str): The index to remove, can be either a number, or a range in the for '##-##'
        """

        if not self.state == 'ready':
            logger.debug("Trying to remove from wrong state '{}'".format(self.state))
            return

        if index == "":
            self.statuslog.error("Must provide index to remove")
            return
        elif index == "all":
            self.queue = []
            self.update_queue()
            self.statuslog.info("Removed all songs")
            return

        indexes = index.split("-")
        self.logger.debug("Removing {}".format(indexes))

        try:
            if len(indexes) == 0:
                self.statuslog.error("Remove must specify an index or range")
                return
            elif len(indexes) == 1:
                num_lower = int(indexes[0]) - 1
                num_upper = num_lower + 1
            elif len(indexes) == 2:
                num_lower = int(indexes[0]) - 1
                num_upper = int(indexes[1])
            else:
                self.statuslog.error("Cannot have more than 2 indexes for remove range")
                return
        except TypeError:
            self.statuslog.error("Remove index must be a number")
            return
        except ValueError:
            self.statuslog.error("Remove index must be a number")
            return

        if num_lower < 0 or num_lower >= len(self.queue) or num_upper > len(self.queue):
            if len(self.queue) == 0:
                self.statuslog.warning("No songs in queue")
            elif len(self.queue) == 1:
                self.statuslog.error("Remove index must be 1 (only 1 song in queue)")
            else:
                self.statuslog.error("Remove index must be between 1 and {}".format(len(self.queue)))
            return

        if num_upper <= num_lower:
            self.statuslog.error("Second index in range must be greater than first")
            return

        lower_songname = self.queue[num_lower][1]
        for num in range(0, num_upper - num_lower):
            self.logger.debug("Removed {}".format(self.queue[num_lower][1]))
            self.queue.pop(num_lower)

        if len(indexes) == 1:
            self.statuslog.info("Removed {}".format(lower_songname))
        else:
            self.statuslog.info("Removed songs {}-{}".format(num_lower + 1, num_upper))

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

            if num < 0:
                self.statuslog.error("Rewind must be postitive or 0")
                return
            elif num > len(self.prev_queue):
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

    async def set_loop(self, loop_value):
        """Updates the loop value, can be 'off', 'on', or 'shuffle'"""
        if loop_value not in ['on', 'off', 'shuffle']:
            self.statuslog.error("Loop value must be `off`, `on`, or `shuffle`")
            return

        self.loop_type = loop_value
        if self.loop_type == 'on':
            self.statuslog.info("Looping on")
        elif self.loop_type == 'off':
            self.statuslog.info("Looping off")
        elif self.loop_type == 'shuffle':
            self.statuslog.info("Looping on and shuffling")

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
        """Writes the current volume to the data.json"""
        # Update the volume
        data = datatools.get_data()
        data["discord"]["servers"][self.server_id][_data.modulename]["volume"] = self.volume
        datatools.write_data(data)

    async def movehere(self, channel):
        """
        Moves the embed message to a new channel; can also be used to move the musicplayer to the front

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

        await client.send_typing(channel)
        embed = ui_embed.topic_update(channel, self.topicchannel)
        await embed.send()

    async def clear_topic_channel(self, channel):
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

        await client.send_typing(channel)
        embed = ui_embed.topic_update(channel, self.topicchannel)
        await embed.send()

    # Methods
    async def vsetup(self, author):
        """Creates the voice client

        Args:
            author (discord.Member): The user that the voice ui will seek
        """

        if self.vready:
            logger.warning("Attempt to init voice when already initialised")
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
                logger.error("Could not load Opus. This is an error with your FFmpeg setup.")
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
            logger.warning("Attempt to init music when already initialised")
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
            ("Author", "---", True),
            ("Source", "---", True),
            ("Time", "```http\n" + _timebar.make_timebar() + "\n```", False),
            ("Queue", "```md\n{}\n```".format(''.join(queue_display)), False),
            ("Songs left in queue", "---", True),
            ("Volume", "{}%".format(self.volume), True),
            ("Status", "```---```", False)
        ]

        # Create embed UI object
        self.embed = ui_embed_tools.UI(
            self.mchannel,
            "",
            "",
            modulename=_data.modulename,
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
        nowplayingauthorhandler = EmbedLogHandler(self, self.embed, 1)
        nowplayingauthorhandler.setFormatter(noformatter)
        nowplayingsourcehandler = EmbedLogHandler(self, self.embed, 2)
        nowplayingsourcehandler.setFormatter(noformatter)
        timehandler = EmbedLogHandler(self, self.embed, 3)
        timehandler.setFormatter(timeformatter)
        queuehandler = EmbedLogHandler(self, self.embed, 4)
        queuehandler.setFormatter(mdformatter)
        queuelenhandler = EmbedLogHandler(self, self.embed, 5)
        queuelenhandler.setFormatter(noformatter)
        volumehandler = EmbedLogHandler(self, self.embed, 6)
        volumehandler.setFormatter(volumeformatter)
        statushandler = EmbedLogHandler(self, self.embed, 7)
        statushandler.setFormatter(statusformatter)

        self.nowplayinglog.addHandler(nowplayinghandler)
        self.nowplayingauthorlog.addHandler(nowplayingauthorhandler)
        self.nowplayingsourcelog.addHandler(nowplayingsourcehandler)
        self.timelog.addHandler(timehandler)
        self.queuelog.addHandler(queuehandler)
        self.queuelenlog.addHandler(queuelenhandler)
        self.volumelog.addHandler(volumehandler)
        self.statuslog.addHandler(statushandler)

    async def add_reactions(self):
        """Adds the reactions buttons to the current message"""
        self.statuslog.info("Loading buttons")
        for e in ("⏯", "⏮", "⏹", "⏭", "🔀", "🔉", "🔊"):
            try:
                if self.embed is not None:
                    await client.add_reaction(self.embed.sent_embed, e)
            except discord.DiscordException as e:
                logger.exception(e)
                self.statuslog.error("I couldn't add the buttons. Check my permissions.")
            except Exception as e:
                logger.exception(e)

    async def enqueue(self, query, queue_index=None, stop_current=False, shuffle=False):
        """
        Queues songs based on either a YouTube search or a link

        Args:
            query (str): Either a search term or a link
            queue_index (str): The queue index to enqueue at (None for end)
            stop_current (bool): Whether to stop the current song after the songs are queued
            shuffle (bool): Whether to shuffle the added songs
        """

        if query is None or query == "":
            return

        self.statuslog.info("Parsing {}".format(query))
        self.logger.debug("Enqueueing from query")

        indexnum = None
        if queue_index is not None:
            try:
                indexnum = int(queue_index) - 1
            except TypeError:
                self.statuslog.error("Play index argument must be a number")
                return
            except ValueError:
                self.statuslog.error("Play index argument must be a number")
                return

        if not self.vready:
            self.parse_query(query, indexnum, stop_current, shuffle)
        else:
            parse_thread = threading.Thread(
                target=self.parse_query,
                args=[query, indexnum, stop_current, shuffle])
            # Run threads
            parse_thread.start()

    def parse_query(self, query, index, stop_current, shuffle):
        """
        Parses a query and adds it to the queue

        Args:
            query (str): Either a search term or a link
            index (int): The index to enqueue at (None for end)
            stop_current (bool): Whether to stop the current song after the songs are queued
            shuffle (bool): Whether to shuffle the added songs
        """

        if index is not None and len(self.queue) > 0:
            if index < 0 or index >= len(self.queue):
                if len(self.queue) == 1:
                    self.statuslog.error("Play index must be 1 (1 song in queue)")
                    return
                else:
                    self.statuslog.error("Play index must be between 1 and {}".format(len(self.queue)))
                    return

        try:
            yt_videos = api_music.parse_query(query, self.statuslog)
            if shuffle:
                random.shuffle(yt_videos)

            if len(yt_videos) == 0:
                self.statuslog.error("No results for: {}".format(query))
                return

            if index is None:
                self.queue = self.queue + yt_videos
            else:
                if len(self.queue) > 0:
                    self.queue = self.queue[:index] + yt_videos + self.queue[index:]
                else:
                    self.queue = yt_videos

            self.update_queue()

            if stop_current:
                if self.streamer:
                    self.streamer.stop()
        except Exception as e:
            logger.exception(e)

    def update_queue(self):
        """Updates the queue in the music player """

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
                if self.vclient is not None and self.vclient_starttime is not None and self.streamer is not None:
                    diff = self.vclient.loop.time() - self.vclient_starttime

                    if self.is_live:
                        time_bar = "Livestream"
                    elif self.current_duration <= 0:
                        time_bar = "Unknown"
                    else:
                        time_bar = _timebar.make_timebar(diff, self.current_duration)

                    if time_bar != self.prev_time:
                        self.timelog.debug(time_bar)
                        self.prev_time = time_bar
                        yield from asyncio.sleep(5)
                    else:
                        yield from asyncio.sleep(1)
                else:
                    yield from asyncio.sleep(1)
            else:
                yield from asyncio.sleep(2)

    def clear_cache(self):
        """Removes all files from the songcache dir"""
        self.logger.debug("Clearing cache")
        if os.path.isdir(self.songcache_dir):
            for filename in os.listdir(self.songcache_dir):
                file_path = os.path.join(self.songcache_dir, filename)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                except PermissionError:
                    pass
                except Exception as e:
                    logger.exception(e)
        self.logger.debug("Cache cleared")

    def move_next_cache(self):
        """Moves files in the 'next' cache dir to the root"""
        if not os.path.isdir(self.songcache_next_dir):
            return

        logger.debug("Moving next cache")
        files = os.listdir(self.songcache_next_dir)
        for f in files:
            try:
                os.rename("{}/{}".format(self.songcache_next_dir, f), "{}/{}".format(self.songcache_dir, f))
            except PermissionError:
                pass
            except Exception as e:
                logger.exception(e)
        logger.debug("Next cache moved")

    def ytdl_progress_hook(self, d):
        """Called when youtube-dl updates progress"""
        if d['status'] == 'downloading':
            self.play_empty()

            if "elapsed" in d:
                if d["elapsed"] > self.current_download_elapsed + 4:
                    self.current_download_elapsed = d["elapsed"]

                    current_download = 0
                    current_download_total = 0
                    current_download_eta = 0
                    if "total_bytes" in d and d["total_bytes"] > 0:
                        current_download_total = d["total_bytes"]
                    elif "total_bytes_estimate" in d and d["total_bytes_estimate"] > 0:
                        current_download_total = d["total_bytes_estimate"]
                    if "downloaded_bytes" in d and d["downloaded_bytes"] > 0:
                        current_download = d["downloaded_bytes"]
                    if "eta" in d and d["eta"] > 0:
                        current_download_eta = d["eta"]

                    if current_download_total > 0:
                        percent = round(100 * (current_download / current_download_total))
                        if percent > 100:
                            percent = 100
                        elif percent < 0:
                            percent = 0

                        seconds = str(round(current_download_eta)) if current_download_eta > 0 else ""
                        eta = " ({} {} remaining)".format(seconds, "seconds" if seconds != 1 else "second")

                        downloading = "Downloading song: {}%{}".format(percent, eta)
                        if self.prev_time != downloading:
                            self.timelog.debug(downloading)
                            self.prev_time = downloading
        if d['status'] == 'error':
            self.statuslog.error("Error downloading song")
        elif d['status'] == 'finished':
            self.statuslog.info("Downloaded song")
            downloading = "Downloading song: {}%".format(100)
            if self.prev_time != downloading:
                self.timelog.debug(downloading)
                self.prev_time = downloading

            if "elapsed" in d:
                download_time = "{} {}".format(d["elapsed"] if d["elapsed"] > 0 else "<1",
                                               "seconds" if d["elapsed"] != 1 else "second")
                self.logger.debug("Downloaded song in {}".format(download_time))

            # Create an FFmpeg player
            future = asyncio.run_coroutine_threadsafe(self.create_ffmpeg_player(d['filename']), client.loop)
            try:
                future.result()
            except Exception as e:
                logger.exception(e)
                return

    def play_empty(self):
        """Play blank audio to let Discord know we're still here"""
        if self.vclient:
            if self.streamer:
                self.streamer.volume = 0
            self.vclient.play_audio("\n".encode(), encode=False)

    def download_next_song(self, song):
        """Downloads the next song and starts playing it"""

        dl_ydl_opts = dict(ydl_opts)
        dl_ydl_opts["progress_hooks"] = [self.ytdl_progress_hook]
        dl_ydl_opts["outtmpl"] = self.output_format

        # Move the songs from the next cache to the current cache
        self.move_next_cache()

        self.state = 'ready'
        self.play_empty()
        # Download the file and create the stream
        with youtube_dl.YoutubeDL(dl_ydl_opts) as ydl:
            try:
                ydl.download([song])
            except DownloadStreamException:
                # This is a livestream, use the appropriate player
                future = asyncio.run_coroutine_threadsafe(self.create_stream_player(song, dl_ydl_opts), client.loop)
                try:
                    future.result()
                except Exception as e:
                    logger.exception(e)
                    self.vafter_ts()
                    return
            except PermissionError:
                # File is still in use, it'll get cleared next time
                pass
            except youtube_dl.utils.DownloadError as e:
                self.logger.exception(e)
                self.statuslog.error(e)
                self.vafter_ts()
                return
            except Exception as e:
                self.logger.exception(e)
                self.vafter_ts()
                return

    def download_next_song_cache(self):
        """Downloads the next song in the queue to the cache"""
        if len(self.queue) == 0:
            return

        cache_ydl_opts = dict(ydl_opts)
        cache_ydl_opts["outtmpl"] = self.output_format_next

        with youtube_dl.YoutubeDL(cache_ydl_opts) as ydl:
            try:
                url = self.queue[0][0]
                ydl.download([url])
            except:
                pass

    async def create_ffmpeg_player(self, filepath):
        """Creates a streamer that plays from a file"""
        self.current_download_elapsed = 0

        self.streamer = self.vclient.create_ffmpeg_player(filepath, after=self.vafter_ts)
        self.state = "ready"
        await self.setup_streamer()

        try:
            # Read from the info json
            info_filename = "{}.info.json".format(filepath)
            with open(info_filename, 'r') as file:
                info = json.load(file)

                self.nowplayinglog.debug(info["title"])
                self.is_live = False

                if "duration" in info and info["duration"] is not None:
                    self.current_duration = info["duration"]
                else:
                    self.current_duration = 0

                if "uploader" in info:
                    self.nowplayingauthorlog.info(info["uploader"])
                else:
                    self.nowplayingauthorlog.info("Unknown")

                self.nowplayingsourcelog.info(api_music.parse_source(info))

                play_state = "Streaming" if self.is_live else "Playing"
                await self.set_topic("{} {}".format(play_state, info["title"]))
                self.statuslog.debug(play_state)
        except Exception as e:
            logger.exception(e)

    async def create_stream_player(self, url, opts=ydl_opts):
        """Creates a streamer that plays from a URL"""
        self.current_download_elapsed = 0

        self.streamer = await self.vclient.create_ytdl_player(url, ytdl_options=opts, after=self.vafter_ts)
        self.state = "ready"

        await self.setup_streamer()

        self.nowplayinglog.debug(self.streamer.title)
        self.nowplayingauthorlog.debug(self.streamer.uploader if self.streamer.uploader is not None else "Unknown")
        self.current_duration = 0
        self.is_live = True

        info = self.streamer.yt.extract_info(url, download=False)
        self.nowplayingsourcelog.info(api_music.parse_source(info))

        play_state = "Streaming" if self.is_live else "Playing"
        await self.set_topic("{} {}".format(play_state, self.streamer.title))
        self.statuslog.debug(play_state)

    async def setup_streamer(self):
        """Sets up basic defaults for the streamer"""
        self.streamer.volume = self.volume / 100
        self.streamer.start()

        self.pause_time = None
        self.vclient_starttime = self.vclient.loop.time()

        # Cache next song
        self.logger.debug("Caching next song")
        dl_thread = threading.Thread(target=self.download_next_song_cache)
        dl_thread.start()

    async def vplay(self):
        if self.state != 'ready':
            logger.error("Attempt to play song from wrong state ('{}'), must be 'ready'.".format(self.state))
            return

        self.state = "starting streamer"
        self.logger.debug("Playing next in queue")

        self.vclient_starttime = None
        self.pause_time = None
        self.clear_cache()

        # Queue has items
        if self.queue is not None and len(self.queue) > 0:
            song = self.queue[0][0]
            songname = self.queue[0][1]

            self.prev_queue.append(self.queue.pop(0))
            while len(self.prev_queue) > self.prev_queue_max:
                self.prev_queue.pop(0)

            try:
                self.nowplayinglog.debug("---")
                self.nowplayingauthorlog.debug("---")
                self.nowplayingsourcelog.debug("---")
                self.statuslog.debug("Downloading next song")
                self.timelog.debug("Loading song")
                self.prev_time = "---"

                dl_thread = threading.Thread(target=self.download_next_song, args=[song])
                dl_thread.start()

                await self.set_topic("Playing {}".format(songname))
            except Exception as e:
                await self.set_topic("")
                self.nowplayinglog.info("Error playing {}".format(songname))
                self.nowplayingauthorlog.info("---")
                self.nowplayingsourcelog.info("---")
                self.timelog.debug(_timebar.make_timebar())
                self.prev_time = "---"
                self.statuslog.error("Had a problem playing {}".format(songname))
                logger.exception(e)

                try:
                    self.streamer.stop()
                except Exception as e:
                    logger.exception(e)

                self.streamer = None
                self.current_duration = 0
                self.current_download_elapsed = 0
                self.is_live = False
                self.state = "ready"
                await self.vplay()

            self.update_queue()
            self.vclient_task = asyncio.Task(self.time_loop(), loop=client.loop)

        # Queue exhausted
        else:
            self.state = "ready"

            if self.loop_type == 'on':
                self.statuslog.info("Finished queue: looping")
                self.queue = self.prev_queue
            elif self.loop_type == 'shuffle':
                self.statuslog.info("Finished queue: looping and shuffling")
                self.queue = self.prev_queue
                random.shuffle(self.queue)
            else:
                self.statuslog.info("Finished queue")

            self.prev_queue = []
            self.update_queue()
            if self.queue:
                await self.vplay()
            else:
                await self.stop()

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

        self.pause_time = None

        if self.vclient_task:
            loop = asyncio.get_event_loop()
            loop.call_soon(self.vclient_task.cancel)
            self.vclient_task = None

        try:
            if self.streamer is None:
                await self.stop()
                return

            if self.streamer.error is None:
                await self.vplay()
            else:
                self.statuslog.error(self.streamer.error)
                await self.destroy()
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
