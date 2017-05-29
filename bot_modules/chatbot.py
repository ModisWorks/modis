import requests
import json
import lxml.html as html
import io

client = None

cleverbotio = None
mitsuku = None


class CleverBotIO:
    def __init__(self):
        self.user = 'PIspeR8IQDBhZjVw'
        self.key = 'oCMB8W70esq2VFEHEhtP4lKt3wzcuaQE'
        self.nick = 'Infraxion'

        body = {
            'user': self.user,
            'key': self.key,
            'nick': self.nick
        }

        requests.post('https://cleverbot.io/1.0/create', json=body)

    def query(self, text):
        body = {
            'user': self.user,
            'key': self.key,
            'nick': self.nick,
            'text': text
        }
        response = requests.post('https://cleverbot.io/1.0/ask', json=body)
        response = json.loads(response.text)

        if response['status'] == 'success':
            return response['response']
        else:
            return "```Could not contact Cleverbot :c```"


class Mitsuku:
    def __init__(self):
        self.params = {
            'botid': 'f6a012073e345a08',
            'amp;skin': 'chat'
        }

        init_headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch, br',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive',
            'DNT': '1',
            'Host': 'kakko.pandorabots.com',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/58.0.3029.110 Safari/537.36'
        }
        response = requests.post(
            'https://kakko.pandorabots.com/pandora/talk?botid=f6a012073e345a08&amp;skin=chat',
            params=self.params,
            headers=init_headers
        )

        self.botcust2 = response.headers['set-cookie'][9:25]

    def query(self, message):
        data = {
            'botcust2': self.botcust2,
            'message': message
        }
        headers = {
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Content-Length': str(len(message) + 34),
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie': 'botcust2=' + self.botcust2,
            'DNT': '1',
            'Host': 'kakko.pandorabots.com',
            'Origin': 'https://kakko.pandorabots.com',
            'Referer': 'https://kakko.pandorabots.com/pandora/talk?botid=f6a012073e345a08&amp;skin=chat',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/58.0.3029.110 Safari/537.36'
        }
        response = requests.post(
            'https://kakko.pandorabots.com/pandora/talk?botid=f6a012073e345a08&amp;skin=chat',
            params=self.params,
            headers=headers,
            data=data
        )
        parsed = html.parse(io.StringIO(response.text)).getroot()
        try:
            return parsed[1][2][0][2].tail[1:]
        except IndexError:
            return "Couldn't get response from Mitsuku. Maybe the API changed, please tell Infraxion."


def init(iclient):
    print("Loading clvrbot...")

    global client
    client = iclient

    global cleverbotio
    cleverbotio = CleverBotIO()
    global mitsuku
    mitsuku = Mitsuku()


async def say(channel, message):
    await client.send_typing(channel)
    await client.send_message(channel, content=message)


async def on_message(message):
    # Get message info
    server = message.server
    author = message.author
    channel = message.channel
    content = message.content

    # Server replies
    if server is not None and author != channel.server.me:
        if channel.server.me in message.mentions:
            content = content.replace("<@" + str(channel.server.me.id) + ">", '')
            await client.send_typing(channel)
            reply = mitsuku.query(content)
            await say(channel, reply)
