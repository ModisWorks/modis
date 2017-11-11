---
title: Modis
---

# MODIS
Modis is a Discord bot that runs with a GUI and is designed to be as modular as possible so that anyone with some basic Python knowledge can quickly and easily create new modules that run on the bot.


## Getting started
To get started hosting your own version of Modis, check out the [Setup](/setup/) guide.


## Custom modules
If you're interested in making your own modules for Modis, have a look at the [Ping Pong Module](/custom-modules/) guide.


## Currently available modules
There are currently 9 modules in Modis:
- `music` by Infraxion, YtnomSnrub
- `manager` by YtnomSnrub
- `help` by YtnomSnrub
- `replies` by Infraxion
- `chatbot` by Infraxion (not working atm)
- `hex` by YtnomSnrub
- `gamedeals` by Infraxion, YtnomSnrub
- `rocketleague` by Infraxion, YtnomSnrub
- `tableflip` by Infraxion

Information about each module is detailed below.
(All commands assume your prefix is set to `!`)


### music
A music player with an interactive GUI using reactions as buttons.

**Commands:**
- `!play [query/link]`: Creates the player GUI if it doesn't yet exist and queues either the first result of a YouTube search or the audio from the url.
- `!playnext [query/link]`: Starts playing the query or link after the current song has finished.
- `!playnow [query/link]`: Stops playing the current song and starts playing the query or link.
- `!pause`: Pauses the player.
- `!resume`: Unpauses the player.
- `!skip [n]`: Skips `n` songs, or skips one if `n` is not included.
- `!shuffle`: Shuffles the songs in the queue.
- `!volume [n]`: Sets the volume to `n`%. `n` can be any integer from 0 to 200.
- `!stop`: Stops the player and clears the queue.
- `!destroy`: Removes the GUI and resets everything. Handy if something is messed up.
- `!front` or `!movehere`: Moves the GUI to the channel you're currently in. If it's already in your channel it gets moved to the bottom where you can see it.


### manager
Manager allows users to activate and deactivate modules within a server, and change the command prefix for Modis.
More features are planned, including automod.

**Commands**
- `!activate [module]`: Activates the given module for the server.
- `!deactivate [module]`: Deactivates the given module for the server.
- `!prefix [prefix]`: Changes the prefix for the server to `[prefix]`.


### help
Displays information on how to use each module in the Discord channel.

**Commands**
- `!help`: Lists the help command for all modules.
- `!help [module]`: Lists the commands for the specified module.


### replies
Replies uses a json file to make it easy for users to make the bot say things in reply to specific messages.


### chatbot
Whenever the bot is mentioned this module can connect to either cleverbot.io or Mitsuku and get a chatbot reply to the message it was mentioned in.

This bot is currently not working since the Mitsuku API no longer exists.
It'll be back up as soon as we find a good replacement.

### hex
Looks for hex values in your messages, and displays the specified colour if it finds a value.
Hex works with any 3 or 6 digit hex values starting with '#' or '0x'.
It can also be called by command.

**Commands**
- `!hex [value]`: Displays the colour of the given hex value.


### gamedeals
Uses Reddit to find current sales and bundles on popular games.

**Commands**
- `!gamedeals`: Gets the top current game sales from reddit.com/r/gamedeals


### rocketleague
Gets Rocket League stats of players using Rocket League Tracker Network. Currently only works for Steam players.

**Commands:**
- `!rl [steamid]` Shows the Rocket League stats of the Steam user `steamid`.
- `!rlstats [userid] [platform]`: Displays the stats for the given user on the specified platform.


### tableflip
The best module.
