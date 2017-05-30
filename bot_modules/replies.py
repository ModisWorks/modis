import json

client = None

modulename = "rocketleague"
creator = "Infraxion"


def init(iclient):
    print("Loading {} by {}".format(modulename, creator))

    global client
    client = iclient


def get_replies():
    file = open("replies.json", 'r')
    return json.load(file)


async def say(channel, message):
    await client.send_typing(channel)
    await client.send_message(channel, content=message, tts=False, embed=None)


async def vsay(channel, message):
    await client.send_typing(channel)
    await client.send_message(channel, content=message, tts=True, embed=None)


async def on_message(message):
    # Get message info
    server = message.server
    author = message.author
    channel = message.channel
    content = message.content

    # Server replies
    if server is not None and author != channel.server.me:
        replies = get_replies()
        for i in replies['normal'].keys():
            if i in content.lower().replace(' ', ''):
                await say(channel, replies['normal'][i])
        for i in replies['tts'].keys():
            if i in content.lower().replace(' ', ''):
                await vsay(channel, replies['tts'][i])
