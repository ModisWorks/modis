---
title: Setup
permalink: /setup/
---

# Installing Modis
If you want to run Modis for yourself, you'll need a bunch of different files, which we still can't seem to get right every time.
Hopefully this guide will make it easier to install Modis for all of us.

## Python 3.6
### Windows
Modis runs on Python 3.6. If you don't have a recent version of Python running on your machine, you'll need to get it on the [Official Python website](https://www.python.org/downloads/release).
Any release starting with 3.6 should work.
As of writing, the current latest 3.6 release is [3.6.3](https://www.python.org/downloads/release/python-363/).

Once you've found the release you want, go to its download page and scroll down to find a bunch of installation files.
Pick the one that matches your OS and architecture and install Python.

When you're installing Python on Windows, make sure you check the option that adds Python to PATH. This makes it a bit easier later on when we're installing packages.

### OS X
[Homebrew](https://brew.sh/) is a package manager for OS X. It will make setting up Modis easier and you should install it if you haven't already. To install Python, open Terminal and run `brew install python`.

## Python packages
You can find all the package requirements in the requirements.txt file.
To install the packages, open a command processor (CMD or Terminal for Windows and OS X) and type `pip install [packagename]`.

Below are a list of commands you'll need to run as of writing if you're too lazy to check requirements.txt:

- `pip install discord.py`
- `pip install youtube-dl`
- `pip install pynacl`
- `pip install google-api-python-client`
- `pip install requests`
- `pip install lxml`
- `pip install praw`


## FFmpeg
### Windows
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

### OS X
If you're using Homebrew, just run `brew install ffmpeg` and `brew install opus` in Terminal. This will install the required libraries for voice and audio that Modis needs.

## Modis package
Now you have all the requirements for Modis installed, but you still need to download Modis.
You can get the latest release on Modis' [release page](https://github.com/Infraxion/modis/releases).
Extract it into a nice, cozy folder.

## Running Modis
Modis is now fully installed, but you still need to make a launch.
We'll be streamlining this in the future so you don't have to do it, but for now, you're going to have to put in some work.
As of writing, the launcher.py file should consist of this:

```python
import modis

DISCORD_TOKEN = "Discord bot token here"
CLIENT_ID = "Discord bot client ID here"

modis.gui(
    discord_token=DISCORD_TOKEN,
    discord_client_id=CLIENT_ID
)
```

To make this file, open up a text editor and paste the text. Save this file as `launcher.py` (and make sure that it's saving as a .py file rather than a .txt file). This file should go in the root directory for Modis (the same one with `requirements.txt`).

To run Modis now, just run `launcher.py`.

*Guides for getting tokens for Discord bots, Reddit, and Google are coming soon.*
