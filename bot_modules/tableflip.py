import string

client = None

tamperdict = None
flipdict = None


def init(iclient):
    print("Loading flipbot...")

    global client
    client = iclient

    make_dicts()


def make_dicts():
    punct = list(string.punctuation)
    punct.remove('(')
    punct.remove(')')
    punct.append(' ')
    punct.append('━')
    punct.append('─')
    tdict = str.maketrans('', '', str(punct))
    fdict = str.maketrans('abcdefghijklmnopqrstuvwxyzɐqɔpǝɟbɥıظʞןɯuodbɹsʇnʌʍxʎz😅🙃😞😟😠😡☹🙁😱😨😰😦😧😢😓😥😭',
                          'ɐqɔpǝɟbɥıظʞןɯuodbɹsʇnʌʍxʎzabcdefghijklmnopqrstuvwxyz😄🙂🙂🙂🙂🙂🙂😀😀🙂😄🙂🙂😄😄😄😁')
    global tamperdict
    tamperdict = tdict
    global flipdict
    flipdict = fdict


async def say(channel, message):
    await client.send_typing(channel)
    await client.send_message(channel, message)


async def flipcheck(channel, content):
    # Prevent tampering with flip
    tamperproof = content.translate(tamperdict)

    # Calculate table length
    length = 0
    for letter in content:
        if letter == "━":
            length += 1.36
        elif letter == "─":
            length += 1
        elif letter == "-":
            length += 0.50

    # Unflip
    if "(╯°□°）╯︵" in tamperproof:
        if "┻┻" in tamperproof:
            putitback = "┬"
            for i in range(int(length)):
                putitback += "─"
            putitback += "┬﻿ ノ( ゜-゜ノ)"
            await say(channel, putitback)
        else:
            flipstart = content.index('︵')
            flipped = content[flipstart+1:]
            flipped = str.lower(flipped).translate(flipdict)
            putitback = ''.join(list(reversed(list(flipped))))
            putitback += "ノ( ゜-゜ノ)"
            await say(channel, putitback)


async def on_message(message):
    # Get message info
    server = message.server
    author = message.author
    channel = message.channel
    content = message.content

    # Server replies
    if server is not None and author != channel.server.me:
        await flipcheck(channel, content)
