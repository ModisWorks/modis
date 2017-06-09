import discord


class EmbedGUI:
    def __init__(
            self,
            title,
            description,
            datapacks=None,
            colour=0xAAFF00,
            thumbnail=None,
            modulename="Modis",
            creator="anonymous",
    ):
        """

        :param string title: GUI title, in bold
        :param string description: GUI description
        :param list datapacks: Tuples of (title, data)
        :param int colour: Colour of line on left, default 0xAAFF00
        :param thumbnail: Picture shown in top right corner
        :param modulename: Name of your module
        :param creator: Your name/screen name
        """
        self.title = title
        self.description = description
        self.datapacks = datapacks
        self.colour = colour
        self.thumbnail = thumbnail
        self.modulename = modulename
        self.creator = creator

        self.built_embed = self.build()
        self.sent_embed = None

    def build(self):
        """

        :return: discord.Embed object
        """
        embed = discord.Embed(
            title=self.title,
            type='rich',
            description=self.description,
            colour=self.colour)

        embed.set_thumbnail(url=self.thumbnail)

        embed.set_author(
            name="Modis",
            url="https://infraxion.github.io/modis/",
            icon_url="http://infraxion.ddns.net/modis/logo128t.png")

        if self.datapacks:
            for pack in self.datapacks:
                embed.add_field(
                    name=pack[0],
                    value=pack[1]
                )

        embed.set_footer(
            text="{} module by {}".format(self.modulename, self.creator),
            icon_url="http://infraxion.ddns.net/modis/{}16.jpg".format(self.creator)
        )

        return embed

    async def update(self, client, channel):
        """
        Edits existing GUI if available, otherwise sends new GUI
        :param discord.Client() client: The discord client to send from
        :param discord.channel channel: The discord channel to send the GUI to
        """
        await client.send_typing(channel)
        if self.sent_embed:
            try:
                await client.edit_message(self.sent_embed, embed=self.built_embed)
            except discord.NotFound:
                pass
        else:
            self.sent_embed = await client.send_message(channel, embed=self.built_embed)
