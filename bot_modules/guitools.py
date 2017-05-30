import discord


class Embed:
    def __init__(
            self,
            title,
            description,
            datapacks=None,
            colour=0xAAFF00,
            thumbnail="http://infraxion.ddns.net/modis/logo128t.png",
            modulename="Modis",
            creator="anonymous",
            creatordp="http://infraxion.ddns.net/modis/logo128t.png"
    ):
        self.title = title
        self.description = description
        self.datapacks = datapacks
        self.colour = colour
        self.thumbnail = thumbnail
        self.modulename = modulename
        self.creator = creator
        self.creatordp = creatordp

        self.built_embed = self.build()

    def build(self):
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
                self.embed.add_field(
                    name=pack[0],
                    value=pack[1]
                )

        embed.set_footer(
            text="{} module by {}".format(self.modulename, self.creator),
            icon_url=self.creatordp
        )

        return embed

    async def send(self, client, channel):
        await client.send_typing(channel)
        return await client.send_message(channel, embed=self.built_embed)
