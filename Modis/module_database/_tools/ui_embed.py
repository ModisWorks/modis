from globalvars import *


class UI:
    def __init__(self, channel, title, description,
                 modulename="Modis", creator="anonymous", colour=0xAAFF00, thumbnail=None, datapacks=()):
        """Initialises variables and builds GUI

        Args:
            channel (discord.Channel): Channel to lock UI to
            title (str): GUI title, in bold
            description (str): GUI description
            modulename (str): Name of your module, default "Modis"
            creator (str): Your name/screen name, default "anonymous"
            colour (int): Colour of line on left, default 0xAAFF00
            thumbnail (str): URL to picture shown in top right corner, default None
            datapacks (list): Contains tuples of (title str, data str, inline bool)
        """

        self.channel = channel
        self.title = title
        self.description = description
        self.modulename = modulename
        self.creator = creator
        self.colour = colour
        self.thumbnail = thumbnail
        self.datapacks = datapacks

        self.built_embed = self.build()
        self.sent_embed = None

    def build(self):
        """Builds Discord embed GUI

        Returns:
            discord.Embed: Built GUI
        """

        embed = discord.Embed(
            title=self.title,
            type='rich',
            description=self.description,
            colour=self.colour)

        if self.thumbnail:
            embed.set_thumbnail(url=self.thumbnail)

        embed.set_author(
            name="Modis",
            url="https://infraxion.github.io/modis/",
            icon_url="http://infraxion.ddns.net/modis/logo128t.png")

        for pack in self.datapacks:
            embed.add_field(
                name=pack[0],
                value=pack[1],
                inline=pack[2]
            )

        embed.set_footer(
            text="{} module by {}".format(self.modulename, self.creator),
            icon_url="http://infraxion.ddns.net/modis/{}16.jpg".format(self.creator)
        )

        return embed

    async def send(self):
        """Send new GUI"""

        await client.send_typing(self.channel)
        self.sent_embed = await client.send_message(self.channel, embed=self.built_embed)

    async def usend(self):
        """Edit existing GUI if available, else send new GUI"""

        if self.sent_embed:
            try:
                await client.edit_message(self.sent_embed, embed=self.built_embed)
            except discord.NotFound:
                self.sent_embed = await client.send_message(self.channel, embed=self.built_embed)
        else:
            await client.send_typing(self.channel)
            self.sent_embed = await client.send_message(self.channel, embed=self.built_embed)

    async def delete(self):
        try:
            await client.delete_message(self.sent_embed)
        except discord.NotFound:
            pass

    def update_data(self, index, data):
        """Updates a particular datapack's data

        Args:
            index (int): The index of the datapack
            data (str): The new value to set for this datapack
        """

        datapack = self.built_embed.to_dict()["fields"][index]
        self.built_embed.set_field_at(index, name=datapack["name"], value=data, inline=datapack["inline"])
