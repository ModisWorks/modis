---
title: Ping Pong Module
permalink: /guides/ping-pong/
---
# Ping Pong Module

In this guide you will learn, step by step, how to make a basic 'ping pong' module for Modis. This guide assumes you already have Modis set up and working, if not check out the [Installing Modis](./setup.md) guide.

After completing this you will know how to:

* Set up a message receiver
* Send messages to Discord
* Listen for commands
* Create a `_help.json` file for a module
* Activate and deactivate your module

> This guide describes commands using the default `!` prefix, but the code will work no matter what the server prefix is set to. If following this guide with a different prefix, just change the `!` at the start of commands to whatever your server prefix is. The server prefix can be found at any time by @mentioning Modis.

## Making a new module

Modis looks in the `modis\discord-modis\modules\` folder for Discord modules. To start making our module, make a new folder there called `pingpong`.

![Module folder structure](https://github.com/Infraxion/modis/raw/gh-pages/doc/guides/img/pingpongfolder.png?raw=true "Module folder structure")

## Listening for messages

To listen to Discord events, a module needs a file with the name of the event. For a message, the file should be named `on_message.py` (a full list of Discord events can be found on the [events page](../documentation/events.md)). To start listening to messages, create a file names `on_message.py` in your `pingpong` folder, and define a new function called `on_message` with a `message` parameter. This function *must* be marked as `async` for it to work.

```python
async def on_message(message):
    print("message received")
```

Next, we want to check if the message says `ping`, and if it does we want to respond with `pong`. We also want to check that the message is sent by a user, and not by Modis. To do this, we'll need to import `client` from `discord_modis`.

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

Now, if you run Modis and send `ping` to a server that Modis is in, Modis should respond with `pong`.

## Commands

Most Modis modules work by using commands to interact with Modis. A command starts with a prefix (`!` by default) followed by the command name. Some commands also have arguments. In this section, we'll expand our ping pong module to use a `ping` command and accept a number argument, and respond with a message containing `pong` repeated as many times as the number argument.

First, we need to check that the message starts with the server command prefix. To do this we'll need to import `datatools` from `modis`.

> The server command prefix can be changed by using the `!prefix [new prefix]` command.

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

Next, we want to parse the argument. This must be an integer, so any non-integer values will be rejected. It also must not be too large, or Discord will get upset because we tried to send too many 'pong's.

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
            arg = ' '.join(package[1:])

            # Only send one pong if no arg is specified
            if not arg:
                arg = "1"

            # Check that the command is 'ping'
            if command == "ping":
                try:
                    # Try and parse the argument
                    repeats = int(arg)
                except ValueError:
                    # Could not parse, respond with an error
                    response = "'{}' is not a number".format(arg)
                    await client.send_typing(message.channel)
                    await client.send_message(message.channel, response)
                    return

                # Check that there aren't going to be too many 'pong's
                if repeats >= 200:
                    response = "'{}' is too many pongs".format(repeats)
                    await client.send_typing(message.channel)
                    await client.send_message(message.channel, response)
                    return

                # Check that there are going to be enough 'pong's
                if repeats <= 0:
                    response = "'{}' is not enough pongs".format(repeats)
                    await client.send_typing(message.channel)
                    await client.send_message(message.channel, response)
                    return

                # Respond with "pong"s
                response = ("pong " * repeats).strip()
                if response:
                    await client.send_typing(message.channel)
                    await client.send_message(message.channel, response)
```

If you run Modis now, and type `!ping 4` into your server, you should get a response of `pong pong pong pong` from Modis.

## Help

All modules in Modis should have a `_help.json` file. This is what the `help` module looks for when generating help information. To begin, create a `_help.json` file in your `pingpong` folder.

`_help.json` files should contain an array of commands, with the key `Commands`, and an about string with the key `About`. The `_help.json` for the `pingpong` module should look something like this.

```js
{
  "Commands": [
    {
      "name": "ping",
      "params": ["n"],
      "description": "Sends a message with [n] 'pong's"
    }
  ],
  "About": "A module to pong your pings."
}
```

If the `_help.json` file is formatted correctly, then running `!help pingpong` should give a response with the data from `_help.json`.

Custom heading are also accepted, and will be formatted in the help message.

## Activating and deactivating the module

So that users can control your module, you should allow it to be deactivated on a per-server basis. To do this, make a `_data.py` file in the `pingpong` module. The `_data.py` contains information specific to your module. Most importantly, Modis creates the `sd_structure` dictionary in the `data.json` for each server Modis is in, which allows you to store settings and objects on a per-server basis.

```python
modulename = "PingPong"

creator = "<your name>"

sd_structure = {
    "activated": True
}
```

Then, in our `on_message.py`, we want to add some code to abort the function if the module is not activated. After we declare `data = datatools.get_data()`, add the following:

```python
# Check to see if the module has been activated
if not data["discord"]["servers"][message.server.id][_data.modulename]["activated"]:
    return
```

You'll also need to import `_data.py`, so your `on_message.py` should now look something like this:

```python
from modis import datatools
from modis.discord_modis.modules.pingpong import _data
from ..._client import client


async def on_message(message):
    # Get the data from the data.json
    data = datatools.get_data()
    # Check to see if the module has been activated
    if not data["discord"]["servers"][message.server.id][_data.modulename]["activated"]:
        return

    # Only reply to server messages and don't reply to myself
    if message.server is not None and message.author != message.channel.server.me:
        # Get the server prefix from the data
        prefix = data["discord"]["servers"][message.server.id]["prefix"]
        # Check if the message starts with the prefix
        if message.content.startswith(prefix):
            # Parse the message
            package = message.content.split(" ")
            command = package[0][len(prefix):]
            arg = ' '.join(package[1:])

            # Only send one pong if no arg is specified
            if not arg:
                arg = "1"

            # Check that the command is 'ping'
            if command == "ping":
                try:
                    # Try and parse the argument
                    repeats = int(arg)
                except ValueError:
                    # Could not parse, respond with an error
                    response = "'{}' is not a number".format(arg)
                    await client.send_typing(message.channel)
                    await client.send_message(message.channel, response)
                    return

                # Check that there aren't going to be too many 'pong's
                if repeats >= 200:
                    response = "'{}' is too many pongs".format(repeats)
                    await client.send_typing(message.channel)
                    await client.send_message(message.channel, response)
                    return

                # Check that there are going to be enough 'pong's
                if repeats <= 0:
                    response = "'{}' is not enough pongs".format(repeats)
                    await client.send_typing(message.channel)
                    await client.send_message(message.channel, response)
                    return

                # Respond with "pong"s
                response = ("pong " * repeats).strip()
                if response:
                    await client.send_typing(message.channel)
                    await client.send_message(message.channel, response)
```

Enabling and disabling `pingpong` by using the `!activate pingpong` and `!deactivate pingpong` should now work.

## Summary

These are the basics for any module for Modis. The documentation has more information about Modis' features, or you can look at the other modules to figure out how things works for yourself.
