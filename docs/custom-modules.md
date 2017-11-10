# Custom Modules
In this guide you will learn, step by step, how to make a basic 'ping pong' module for Modis.

This guide assumes you already have Modis set up and working, if not check out the (Installing Modis guide)[./getting-started.md]

After completing this you will know how to:
* Set up a message receiver
* Send messages to Discord
* Listen for commands
* Create a `help.json` file for a module
* Activate and deactivate your module
* Use Modis' embed features


## Making a new module
Modis looks in the `modis\discord-modis\modules\` folder for Discord modules. To start making our module, make a new folder there called `pingpong`.

![Module folder structure](./img/pingpongfolder.png?raw=true "Module folder structure")


## Listening for messages
To listen to Discord events, a module needs a file with the name of the event. For a message, the file should be named `on_message.py` (a full list of Discord events can be found on the [events page](./events.md)). To start listening to messages, create a file names `on_message.py` in your `pingpong` folder, and define a new function called `on_message` with a `message` parameter. This function *must* be marked as `async` for it to work.

```python
async def on_message(message):
    print("message received")
```

Next, we want to check if the message says `"ping"`, and if it does we want to respond with `"pong"`. We also want to checkt that the message is sent by a user, and not by Modis. To do this, we'll need to import `client` from `discord_modis`.

```python
from ..._client import client


async def on_message(message):
    # Only reply to server messages and don't reply to myself
    if message.server is not None and message.author != message.channel.server.me:
        # Check the content of the message
        if message.content == "ping":
            # Respond with 'pong'
            await client.send_typing(message.channel)
            await client.send_message(message.channel, "pong")
```

Now, if you run Modis and send "ping" to a server that Modis is in, Modis should respond with "pong".

## Commands

Most Modis modules work by using commands to interact with Modis. A command starts with a prefix (`!` by default) followed by the command name. Some commands also have arguments. In this section, we'll expand our ping pong module to use a `ping` command and accept a number argument, and respond with a message containing `pong` repeated as many times as the number argument.

First, we need to check that the message starts with the server command prefix. To do this we'll need to import datatools from modis.

```python
from ..._client import client
from modis import datatools


async def on_message(message):
    # Get the data from the data.json
    data = datatools.get_data()
    # Only reply to server messages and don't reply to myself
    if message.server is not None and message.author != message.channel.server.me:
        # Get the server prefix from the data
        prefix = data["discord"]["servers"][message.server.id]["prefix"]
        # Check if the message starts with the prefix
        if message.content.startswith(prefix):
            # Parse the message
            package = message.content.split(" ")
            command = package[0][len(prefix):]

            # Check that the command is 'ping'
            if command == "ping":
                # Respond with "pong"
                await client.send_typing(message.channel)
                await client.send_message(message.channel, "pong")
```
