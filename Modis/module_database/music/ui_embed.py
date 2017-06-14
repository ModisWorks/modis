from globalvars import *

from .._tools import ui_embed
from ._constants import *


class MusicPlayer:
    def __init__(self, channel, queue_length=9):
        """Runs the embed UI side of the music player

        Args:
            channel (discord.Channel): The text channel to run the embed UI on
            queue_length (int): The amount of songs to display in the queue, defaults to 9
        """

        self.channel = channel
        self.queue_length = queue_length

        self.ui_m = None

        self.new_embed_ui()

        self.ready = False

    def new_embed_ui(self):
        """Create the embed UI object and save it to self"""

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
            modulename=modulename,
            creator=creator,
            colour=0x88FF00,
            datapacks=datapacks
        )

    def reset_embed_ui(self):
        """Resets the current embed UI object"""

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

        self.reset_embed_ui()
        await self.update_status(reason)

    async def update_nowplaying(self, songname):
        """Updates the nowplaying field

        Args:
            songname (str): The currently playing song
        """

        self.ui_m.update_data(0, songname)
        await self.ui_m.usend()

    async def update_queue(self, queue):
        """Updates the displayed queue

        Args:
            queue (list): The current queue
        """

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

        self.ui_m.update_data(3, "{}%".format(str(volume)))
        await self.ui_m.usend()

    async def update_status(self, message):
        """Updates the status field

        Args:
            message (str): The new status
        """

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
