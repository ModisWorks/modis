# MODIS
Latest release: [0.2.3 ALPHA](https://github.com/Infraxion/modis/releases/tag/0.2.3) (It's pretty outdated)
Our first beta should be coming soon; by the end of Nov.




## About Modis
Modis is a Discord bot that runs with a GUI and is designed to be as modular as possible so that anyone with some basic Python knowledge can quickly and easily create new modules that run on the bot.



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



## Installing Modis
If you want to run Modis for yourself, you'll need a bunch of different files, which we still can't seem to get right every time.
Hopefully this guide will make it easier to install Modis for all of us.

### Python 3.6
Modis runs on Python 3.6. Get it on the [Official Python website](https://www.python.org/downloads/release).
Any release starting with 3.6 should work.
As of writing, the current latest 3.6 release is [3.6.3](https://www.python.org/downloads/release/python-363/).

Once you've found the release you want, go to its download page and scroll down to find a bunch of installation files.
Pick the one that matches your OS and architecture and install Python.

When you're installing Python, make sure you check the option that adds Python to PATH.
This makes it a bit easier later on when we're installing packages.

### Python packages
You can find all the package requirements in the requirements.txt file.
To install them, open up CMD and type `pip install [packagename]`.
If you added Python to PATH, this should work without any problems, otherwise you'll need to go to the python install folder, find pip.exe, shift-right click and use "Open PowerShell window here".

Below are a list of commands you'll need to run as of writing if you're too lazy to check requirements.txt:

- `pip install discord.py`
- `pip install youtube-dl`
- `pip install pynacl`
- `pip install google-api-python-client`
- `pip install requests`
- `pip install lxml`
- `pip install praw`

### FFmpeg
For the audio stuff to work, you'll need the FFmpeg library in your PATH.
Go to the FFmpeg org's [official website](https://www.ffmpeg.org/download.html) to get a download for FFmpeg.
*DON'T* press the big green download button.
That gives you an uncompiled version of FFmpeg.
We totally have not made this mistake multiple times before.

Look further down for the OS icons, pick the one you're using and download.
Unzip and copy the download to a cozy place such as Program Files.

Now we need to add the /bin folder to PATH.
Go to start and just search "path".
One of the results should be "Edit environment variables for your account".
Click on it, then in the window that pops up double-click on the "Path" line.
If you do the top one it applies to your account only, the bottom on applies to all accounts.
Up to you.
Click on "Browse" in the window that pops up and find the /bin folder inside the extracted FFmpeg build.
Click "OK" or "Apply" or whatever until everything is all nice and packed up.

### Modis package
Now you have all the requirements for Modis installed, but you still need to download Modis.
You can get the latest release on Modis' [release page](https://github.com/Infraxion/modis/releases).
Extract it into a nice, cozy folder.

### Running Modis
Modis is now fully installed, but you still need to make a launcher and create a data.json file.
We'll be streamlining this in the future so you don't have to do it, but for now, you're going to have to put in some work.
As of writing, the launcher.py file should consist of this:

```
import modis

DISCORD_TOKEN = "Discord bot token here"
CLIENT_ID = "Discord bot client ID here"

modis.gui(
    discord_token=DISCORD_TOKEN,
    discord_client_id=CLIENT_ID
)
```

The base data.json file should consist of this:
```
{
  "discord": {
    "client_id": "",
    "token": "",
    "keys": {
      "google_api_key": "",
      "reddit_api_client_id": "",
      "reddit_api_client_secret": "",
      "reddit_api_user_agent": ""
    },
    "servers": {}
  }
}
```

To make these files, open up notepad, paste the text, and save as launcher.py and data.json respectively.
Remember to set file type to "All files".
The two files should go in the same directory as requirements.txt.

To run Modis, just double click launcher.py.

*Guides for getting tokens for Discord bots, Reddit, and Google are coming soon.*
