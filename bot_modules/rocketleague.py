import discord
import requests
import json
import lxml.html as html
import io

client = None
prefix = '/'


def rl(player):
    response = requests.get('https://rocketleague.tracker.network/profile/steam/' + player)
    parsed = html.parse(io.StringIO(response.text)).getroot()
    try:
        playerid = parsed[1][6][0][4][0][1][0][2][0].attrib['href'][10:]
        name = parsed[0][2].text[31:]
    except (IndexError, KeyError):
        return discord.Embed(
            title="That SteamID doesn't exist.",
            type='rich',
            description='You can get your SteamID by going to your profile page and looking at the url, '
                        'or you can set a custom ID by going to edit profile on your profile page.',
            colour=0x0088FF)
    else:
        response = requests.post(
            'https://rocketleague.tracker.network/live/data',
            json={"playerIds": [playerid]})
        response = json.loads(response.text)

        stats = []
        try:
            for statpack in response['players'][0]['Stats']:
                field = statpack['Value']['Label']
                value = str(statpack['Value']['DisplayValue'])
                if statpack['Value']['Percentile']:
                    percentile = str(statpack['Value']['Percentile'])
                else:
                    percentile = None
                stats.append((field, value, percentile))
        except (IndexError, KeyError):
            return discord.Embed(
                title="Couldn't get stats off RLTrackerNetwork.",
                type='rich',
                description='Maybe the API changed, please tell Infraxion.',
                colour=0x0088FF)

        try:
            int(player)
        except ValueError:
            response = requests.get('http://steamcommunity.com/id/' + player)
        else:
            response = requests.get('http://steamcommunity.com/profile/' + player)
        parsed = html.parse(io.StringIO(response.text)).getroot()
        try:
            dp = parsed[0][29].attrib['href']
        except (IndexError, KeyError):
            dp = 'https://rocketleague.media.zestyio.com/' \
                 'rocket-league-logos-vr-white.f1cb27a519bdb5b6ed34049a5b86e317.png'

        return create_gui(stats, dp, name)


def create_gui(stats, dp, name):
    gui = discord.Embed(
        title="Rocket League Stats: " + name,
        type='rich',
        description="*Stats obtained from [Rocket League Tracker Network](https://rocketleague.tracker.network/)*",
        colour=0x0088FF)

    gui.set_thumbnail(url=dp)

    gui.set_author(
        name="Modis",
        url="https://infraxion.github.io/modis/",
        icon_url="https://rocketleague.tracker.network/favicon.ico")

    for stat in stats:
        if stat[0] in ["Duel 1v1", "Doubles 2v2", "Solo Standard 3v3", "Standard 3v3"]:
            name = "__" + stat[0] + "__"
            value = "**" + stat[1] + "**"
        else:
            name = stat[0]
            value = stat[1]

        if stat[2]:
            value = value + " *(Top " + stat[2] + "%)*"

        gui.add_field(
            name=name,
            value=value)

    gui.set_footer(
        text="Modis Rocket League stats by Infraxion",
        icon_url='https://www.google.com/s2/favicons?domain=www.rocketleaguegame.com')

    return gui


def init(iclient, iprefix):
    print("Loading rocketleague...")

    global client
    client = iclient
    global prefix
    prefix = iprefix


async def on_message(message):
    # Get message info
    server = message.server
    author = message.author
    channel = message.channel
    content = message.content
    # Server commands
    if server is not None and author != channel.server.me and content.startswith(prefix):
        # Parse message
        package = content.split(" ")
        command = package[0][1:]
        args = package[1:]

        # Commands
        if command == 'rl':
            await client.send_typing(channel)
            await client.send_message(channel, embed=rl(' '.join(args)))
