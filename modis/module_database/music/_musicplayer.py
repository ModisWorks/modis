from . import ui_embed
from . import ui_voice


class MusicPlayer:
    def __init__(self, server_id):
        """Locks onto a server for easy management of various UIs

        Args:
            server_id (str): The Discord ID of the server to lock on to
        """

        self.ui_m = None
        self.ui_v = None

        self.server_id = server_id

        self.ready = False

    async def init(self, author, text_channel):
        """Creates the UIs

        Args:
            author (discord.Member): The user that the voice ui will seek
            text_channel (discord.Channel): The channel for the embed ui to run in
        """

        # Create embed UI
        if self.ui_m is None:
            self.ui_m = ui_embed.MusicPlayer(text_channel)
            await self.ui_m.create()

        # Create voice UI
        self.ui_v = ui_voice.MusicPlayer(author.voice_channel, self.ui_m)
        await self.ui_v.create()

        # Mark serverlock ready if both voice and embed UIs are ready
        return all((self.ui_m.ready, self.ui_v.ready))

    async def play(self, author, text_channel, arg):
        """The play command

        Args:
            author (discord.Member): The member that called the command
            text_channel (discord.Channel): The channel where the command was called
            arg (str): The argument that was passed with the command
        """

        # Create UIs
        if not self.ready:
            self.ready = await self.init(author, text_channel)

        if self.ready:
            # Add the query to queue
            await self.ui_v.enqueue(arg)

            # Start playing if not yet playing
            if self.ui_v.player is None:
                await self.ui_v.play()

    async def pause(self):
        """The pause command"""

        if self.ready:
            await self.ui_v.pause()

    async def stop(self):
        """The stop command"""

        if self.ready:
            await self.ui_v.destroy()

            if self.ui_m:
                await self.ui_m.reset("Stopped")

            self.ready = False

    async def destroy(self, reason=None):
        """The destroy command

        Args:
            reason (str): The reason for destroying the player; will be sent as a separate message after destruction
        """

        if self.ready:
            await self.ui_v.destroy()
            self.ui_v = None

            if self.ui_m:
                await self.ui_m.destroy(reason)
            self.ui_m = None

        self.ready = False

    async def skip(self, num=1):
        """The skip command

        Args:
            num (int): The number of items to skip
        """

        if self.ui_v and self.ready:
            try:
                arg = int(num)
            except TypeError:
                if self.ui_m:
                    await self.ui_m.temp_update_status("Skip argument must be a number")
            else:
                await self.ui_v.skip(arg)

    async def shuffle(self):
        """The shuffle command"""

        if self.ui_v and self.ready:
            await self.ui_v.shuffle()

    async def volume(self, value):
        """The volume command

        Args:
            value (str): The value to set the volume to
        """

        if self.ui_v and self.ready:
            if value == '+':
                await self.ui_v.vol_up()

            elif value == '-':
                await self.ui_v.vol_down()

            else:
                try:
                    value = int(value)
                except ValueError:
                    if self.ui_m:
                        await self.ui_m.temp_update_status("Volume argument must be +, -, or a %")
                else:
                    await self.ui_v.set_vol(value)
