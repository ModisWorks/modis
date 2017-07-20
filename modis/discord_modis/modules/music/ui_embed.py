import logging

from ..._client import client

from . import _data

from .._tools import ui_embed

import threading
import asyncio

logger = logging.getLogger(__name__)


class MusicPlayer:
    def __init__(self, channel, queue_length=9):
        """Runs the embed UI side of the music player

        Args:
            channel (discord.Channel): The text channel to run the embed UI on
            queue_length (int): The amount of songs to display in the queue, defaults to 9
        """

        logger.debug("Creating new gui")

        self.channel = channel
        self.queue_length = queue_length

        self.ui_m = None

        self.new_embed_ui()

        self.status = ""
        self.statustimer = None

        self.ready = False

    def new_embed_ui(self):
        """Create the embed UI object and save it to self"""

        logger.debug("Initiating new gui")

        # Initial queue display
        queue_display = []
        for i in range(self.queue_length):
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
        self.ui_m = ui_embed.UI(
            self.channel,
            "Music Player",
            "Press the buttons!",
            modulename=_data.modulename,
            creator=_data.creator,
            colour=0x88FF00,
            datapacks=datapacks
        )

        # Add handler to show logs in status bar of player
        class LogHandler(logging.Handler):
            def __init__(self, embed):
                logging.Handler.__init__(self)

                self.embed = embed

            def flush(self):
                runcoro(self.ui_m.usend())

            def emit(self, record):
                msg = self.format(record)
                self.ui_m.update_data(4, "```{}```".format(msg))
                self.flush()

        music_logger = logging.getLogger("modis.discord_modis.modules.music")
        formatter = logging.Formatter("{message}", style="{")
        handler = LogHandler(self.ui_m)
        handler.setFormatter(formatter)
        music_logger.addHandler(handler)

    def reset_embed_ui(self):
        """Resets the current embed UI object"""

        logger.debug("Resetting gui data")

        # Initial queue display
        queue_display = []
        for i in range(self.queue_length):
            queue_display.append("{}: ---\n".format(str(i + 1)))

        # Initial datapacks
        datapacks = [
            ("Now playing", "---", False),
            ("Queue", "```{}```".format(''.join(queue_display)), False),
            ("Songs left in queue", "---", True),
            ("Volume", "10%", True),
            ("Status", "```---```", False)
        ]

        for i in range(len(datapacks)):
            self.ui_m.update_data(i, datapacks[i][1])

    async def create(self):
        """Sends the embed ui created by get_embed_ui to the channel specified in self"""

        logger.debug("Sending embed gui")

        await self.ui_m.usend()

        await self.update_status("Loading buttons")
        for e in ("⏯", "⏹", "⏩", "🔀", "🔉", "🔊"):
            await client.add_reaction(self.ui_m.sent_embed, e)

        self.ready = True

    async def destroy(self, reason=None):
        """Deletes the embed message and sends a regular message with the reason for deletion

        Args:
            reason (str): The message to send after deleting the embed message
        """

        logger.debug("Destroying gui")

        await self.ui_m.delete()

        if reason:
            await client.send_typing(self.channel)
            await client.send_message(self.channel, reason)

        self.new_embed_ui()

        self.ready = False

    async def reset(self, reason=None):
        """Resets the embed UI

        Args:
            reason (str): The reason for the player reset
        """

        logger.debug("Resetting gui")

        self.reset_embed_ui()
        await self.update_status(reason)

    async def update_nowplaying(self, songname):
        """Updates the nowplaying field

        Args:
            songname (str): The currently playing song
        """

        logger.debug("Updating nowplaying")

        self.ui_m.update_data(0, songname)
        await self.ui_m.usend()

    async def update_queue(self, queue):
        """Updates the displayed queue

        Args:
            queue (list): The current queue
        """

        logger.debug("Updating queue")

        queue_display = []
        for i in range(self.queue_length):
            try:
                if len(queue[i][1]) > 40:
                    songname = queue[i][1][:37] + "..."
                else:
                    songname = queue[i][1]
            except IndexError:
                songname = "---"
            queue_display.append("{}: {}\n".format(str(i + 1), songname))

        self.ui_m.update_data(1, "```{}```".format(''.join(queue_display)))
        self.ui_m.update_data(2, str(len(queue)))
        await self.ui_m.usend()

    async def update_volume(self, volume):
        """Updates the currently displaying volume

        Args:
            volume (int): The current volume percentage
        """

        logger.debug("Updating volume")

        self.ui_m.update_data(3, "{}%".format(str(volume)))
        await self.ui_m.usend()

    async def update_status(self, message):
        """Updates the status field

        Args:
            message (str): The new status
        """

        self.status = message

        if len(message) > 43:
            message = "{}...".format(message[:40])

        self.ui_m.update_data(4, "```{}```".format(message))
        await self.ui_m.usend()

    async def temp_update_status(self, message):
        """Temporarily updates the status field

        Args:
            message (str): The temporary status
        """

        if len(message) > 43:
            message = "{}...".format(message[:40])

        self.ui_m.update_data(4, "```{}```".format(message))
        await self.ui_m.usend()

        if self.statustimer:
            self.statustimer.cancel()
        self.statustimer = threading.Timer(3, lambda: runcoro(self.update_status(self.status))).start()

    async def move(self, channel):
        """Moves the embed message to a new channel; can also be used to move the musicplayer to the front

        Args:
            channel (discord.Channel): The channel to move to
        """

        logger.debug("Moving gui")

        await self.ui_m.delete()
        self.ui_m.channel = channel
        await self.ui_m.usend()


def runcoro(async_function):
    """Runs an asynchronous function without needing to use await - useful for lambda

    Args:
        async_function (Coroutine): The asynchronous function to run
    """

    future = asyncio.run_coroutine_threadsafe(async_function, client.loop)
    result = future.result()
    return result
