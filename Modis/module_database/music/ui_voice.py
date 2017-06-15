from share import *

from . import api_youtube

import random as _random


class MusicPlayer:
    def __init__(self, channel, linked_embed_ui=None):
        """Runs the voice UI side of the music player

        Args:
            channel (discord.Channel):
            linked_embed_ui (ui_embed.MusicPlayer):
        """

        self.channel = channel
        self.ui_m = linked_embed_ui

        self.speaker = None
        self.player = None

        self.queue = []
        self.volume = 10

        self.ready = False

    async def create(self):
        """Connects to voice"""

        if self.channel:
            if self.ui_m:
                await self.ui_m.update_status("Connecting to voice")

            self.speaker = await client.join_voice_channel(self.channel)

            self.ready = True
        else:
            await self.destroy()
            await self.ui_m.reset("You're not connected to a voice channel.")

    async def enqueue(self, query):
        """Queues songs based on either a YouTube search or a link

        Args:
            query (str): Either a search term or a link
        """

        # Non-YouTube
        if "/" in query and "youtube" not in query:
            self.queue.append([query, query])
            # INFORM QUEUE OF NON-YT LINK

        # YouTube
        else:
            self.queue = self.queue + api_youtube.get_ytvideos(query, self.ui_m)

        if self.ui_m:
            await self.ui_m.update_queue(self.queue)

    async def play(self):
        """Plays the next song in the queue"""

        # Queue has items
        if self.queue:
            if self.ui_m:
                await self.ui_m.update_status("Loading next song")

            song = self.queue[0][0]
            songname = self.queue[0][1]

            self.player = await self.speaker.create_ytdl_player(song, after=lambda: runcoro(self.after()))

            self.player.volume = self.volume / 100
            self.player.start()

            self.queue.pop(0)

            if self.ui_m:
                await self.ui_m.update_queue(self.queue)
                await self.ui_m.update_status("Playing")
                await self.ui_m.update_nowplaying(songname)

        # Queue exhausted
        else:
            await self.destroy()
            await self.ui_m.reset("Finished queue")

    async def after(self):
        """Function that is called after a song finishes playing"""

        if self.player.error is None:
            await self.play()
        else:
            await self.destroy()
            if self.ui_m:
                await self.ui_m.reset("Encountered an error while playing :/")

    async def destroy(self):
        """Disconnects from voice and stops any players, and resets all variables"""

        self.queue = []

        try:
            self.player.stop()
            await self.speaker.disconnect()
        except AttributeError:
            pass
        except discord.NotFound:
            pass

        self.speaker = None
        self.player = None

        self.volume = 10

        self.ready = False

    async def skip(self, number=1):
        """Skips a specified number of songs

        Args:
            number (int): The number of songs to skip, defaults to 1
        """

        if self.ui_m:
            await self.ui_m.update_status("Skipping")

        for i in range(number - 1):
            try:
                self.queue.pop(0)
            except IndexError:
                pass

        try:
            self.player.stop()
        except AttributeError:
            pass

    async def shuffle(self):
        """Shuffles the queue"""

        if self.ui_m:
            await self.ui_m.temp_update_status("Shuffling")

        _random.shuffle(self.queue)

        if self.ui_m:
            await self.ui_m.update_queue(self.queue)
            await self.ui_m.temp_update_status("Shuffled")

    async def pause(self):
        """Pauses the player"""

        try:
            if self.player.is_playing():
                if self.ui_m:
                    await self.ui_m.update_status("Paused")

                self.player.pause()
            else:
                if self.ui_m:
                    await self.ui_m.update_status("Playing")

                self.player.resume()
        except AttributeError:
            pass

    async def vol_down(self):
        """Reduces the volume to the next multiple of 10"""

        if self.volume > 0:
            if self.ui_m:
                await self.ui_m.temp_update_status("Volume down")

            self.volume = (10 * ((self.volume + 9) // 10)) - 10

            if self.ui_m:
                await self.ui_m.update_volume(self.volume)

            try:
                self.player.volume = self.volume / 100
            except AttributeError:
                pass
        else:
            if self.ui_m:
                await self.ui_m.temp_update_status("Already at minimum volume")

    async def vol_up(self):
        """Increases the volume to the next multiple of 10"""

        if self.volume < 100:
            if self.ui_m:
                await self.ui_m.temp_update_status("Volume up")

            self.volume = (10 * (self.volume // 10)) + 10

            if self.ui_m:
                await self.ui_m.update_volume(self.volume)

            try:
                self.player.volume = self.volume / 100
            except AttributeError:
                pass
        else:
            if self.ui_m:
                await self.ui_m.temp_update_status("Already at maximum volume")

    async def set_vol(self, volume):
        """Sets the volume to a specified value

        Args:
            volume (int): The value to set the volume to
        """

        if 0 <= volume <= 200:
            if self.ui_m:
                await self.ui_m.temp_update_status("Setting volume")

            self.volume = volume

            if self.ui_m:
                await self.ui_m.update_volume(self.volume)

            try:
                self.player.volume = self.volume / 100
            except AttributeError:
                pass
        else:
            if self.ui_m:
                await self.ui_m.temp_update_status("Volume must be between 0 and 200%")
