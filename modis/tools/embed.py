"""
This tool is Modis' embed API. It allows Modis modules to easily create
fancy looking GUIs in the Discord client.
"""

import logging

import discord

from modis import main

logger = logging.getLogger(__name__)

URL = "https://musicbyango.com/modis/"
ICON = "http://musicbyango.com/modis/dp/modis64t.png"


class UI:
    """Enables easy management of Discord embeds."""

    def __init__(self, channel, title, description, modulename="Modis",
                 colour=0xAAFF00, thumbnail=None, image=None, datapacks=()):
        """Initialise variables and build the embed.

        Args:
            channel (discord.Channel): Channel to lock UI to
            title (str): GUI title, in bold
            description (str): GUI description
            modulename (str): Name of your module, default "Modis"
            colour (int): Colour of line on left, default 0xAAFF00
            thumbnail (str): URL to picture shown in top right corner, default None
            datapacks (list): Contains tuples of (title str, data str, inline bool)
        """

        self.channel = channel
        self.title = title
        self.description = description
        self.modulename = modulename
        self.colour = colour
        self.thumbnail = thumbnail
        self.image = image
        self.datapacks = datapacks
        self.datapack_lines = {}

        self.built_embed = self.build()
        self.sent_embed = None

    def build(self):
        """Build the embed.

        Returns:
            discord.Embed: The built embed.
        """

        embed = discord.Embed(
            title=self.title,
            type='rich',
            description=self.description,
            colour=self.colour)

        embed.set_author(
            name="Modis",
            url=URL,
            icon_url=ICON)

        if self.thumbnail:
            embed.set_thumbnail(url=self.thumbnail)

        if self.image:
            embed.set_image(url=self.image)

        self.datapack_lines = {}
        for pack in self.datapacks:
            embed.add_field(name=pack[0], value=pack[1], inline=pack[2])
            self.datapack_lines[pack[0]] = pack

        return embed

    async def send(self):
        """Send the embed message."""

        await main.client.send_typing(self.channel)
        self.sent_embed = await main.client.send_message(self.channel, embed=self.built_embed)

    async def usend(self):
        """Update the existing embed."""

        try:
            await main.client.edit_message(self.sent_embed, embed=self.built_embed)
        except Exception as e:
            # TODO Add exceptions
            logger.exception(e)

    async def delete(self):
        """Delete the existing embed."""

        try:
            await main.client.delete_message(self.sent_embed)
        except Exception as e:
            # TODO Add exceptions
            logger.exception(e)

        self.sent_embed = None

    def update_field(self, title, data):
        """Update a particular field's data.

        Args:
            title (str): The title of the field to update.
            data (str): The new value to set for this datapack.
        """

        if title in self.datapack_lines:
            self.update_data(self.datapack_lines[title], data)
        else:
            logger.warning("No field with title '{}'".format(title))

    def update_colour(self, new_colour):
        """Update the embed's colour.

        Args:
            new_colour (discord.Colour): The new colour for the embed.
        """

        self.built_embed.colour = new_colour

    def update_data(self, index, data):
        """Update a particular datapack's data.

        Args:
            index (int): The index of the datapack.
            data (str): The new value to set for this datapack.
        """

        datapack = self.built_embed.to_dict()["fields"][index]
        self.built_embed.set_field_at(index, name=datapack["name"], value=data, inline=datapack["inline"])
