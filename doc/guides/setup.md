---
title: Setup
permalink: /guides/setup/
---
# Installing Modis

If you want to run Modis for yourself there's a few things you'll need to install. You might already have some of these installed, so if you know what you're doing feel free to skip those steps.

## Python 3.6

### Python on Windows

Modis runs on Python 3.6. If you don't have a recent version of Python running on your machine, you'll need to get it on the [Official Python website](https://www.python.org/downloads/release).
Any release starting with 3.6 should work.
As of writing, the current latest 3.6 release is [3.6.6](https://www.python.org/downloads/release/python-366/).

> Python 3.7 and later is not compatible with the discord.py API that Modis uses, and therefore Python 3.7 installations will not work with Modis.

Once you've found the release you want, go to its download page and scroll down to find a bunch of installation files.
Pick the one that matches your OS and architecture and install Python.

When you're installing Python on Windows, make sure you check the option that adds Python to PATH. This makes it a bit easier later on when we're installing packages.

### Python on OS X

[Homebrew](https://brew.sh/) is a package manager for OS X. It will make setting up Modis easier and you should install it if you haven't already. To install Python, open Terminal and run `brew install python`.

## FFmpeg

FFmpeg is required for Modis to use audio and voice features of Discord (such as playing music with the `music` module). If you don't need any modules that use voice functionality then you can skip this step.

### FFmpeg on Windows

For the audio stuff to work on Windows, you'll need the FFmpeg library in your PATH.
Go to the FFmpeg org's [official website](https://www.ffmpeg.org/download.html) to get a download for FFmpeg.

> *DON'T* press the big green download button. That gives you an uncompiled version of FFmpeg. We totally have not made this mistake multiple times before.

Look further down for the OS icons, pick the one you're using and download, and unzip and copy the download to a cozy place such as Program Files.

Now we need to add the /bin folder to PATH.

- Go to start and just search "path".
- One of the results should be "Edit environment variables for your account".
- Click on it, then in the window that pops up double-click on the "Path" line.
- If you do the top one it applies to your account only, the bottom on applies to all accounts (up to you).
- Click on "Browse" in the window that pops up and find the /bin folder inside the extracted FFmpeg build.
- Click "OK" or "Apply" or whatever until everything is all nice and packed up.

Restart your computer so that Windows updates everything correctly, and continue with the next step.

### FFmpeg on OS X

If you're using Homebrew, just run `brew install ffmpeg --with-opus` in Terminal. This will install the required libraries for voice and audio that Modis needs. Restart your computer after the package has downloaded and continue with the next step.

## Getting Modis

Now that you have the basics done, you want to install Modis. First, you'll want to use pip to install Modis to install all the packages and requirements that Modis needs. In a command window, run `pip3 install modis --upgrade` to install the latest version of Modis. If everything goes well and there are no errors, then you can start making a file to launch Modis from.

## Running Modis

Modis is now fully installed, but you still need to make a way to run it. You'll need to make a Python file to run it. First: import the `modis` packages, then call `modis.gui` with your Discord Bot Token and Discord Bot Client ID.

> If you don't know how to make your own Discord Bot, have a look at the [Making a Discord Bot](./api-keys.md#making-a-discord-bot) section for step-by-step instructions on getting the Discord token and client id.

The `launcher.py` file should look like this:

```python
import modis

DISCORD_TOKEN = "Discord bot token here"
CLIENT_ID = "Discord bot client ID here"

modis.gui(
    discord_token=DISCORD_TOKEN,
    discord_client_id=CLIENT_ID
)
```

To run Modis now, just run `python launcher.py` from the directory that `launcher.py` is in.

> If you are running Modis on a system without `tkinter` installed, or you just really like command windows, you will need to change `modis.gui` to `modis.console`.

### Installing the whole thing

The best bit about Modis is that it's really easy to make it your own! Once you have it working with the `pip` install and a `launcher.py` file, you should download the latest release on Modis' [release page](https://github.com/Infraxion/modis/releases). Extract it into a nice, cozy folder that you can run it from.

To run this version of Modis, you'll need to use your `launcher.py` file from above and put it in the root directory (the one with `requirements.txt`). You can run Modis the same way, but it'll use your code now instead of the code from `pip`. You can edit this to do what you want: tweak our modules, or look at our other guides and make your own!

## Troubleshooting

If you still have problems, see the [Troubleshooting](../documentation/troubleshooting.md) section for solutions to some common problems. If you don't find a solution there, then feel free to join our Discord Server to ask your questions.

*Guides for getting tokens for Discord bots, Reddit, and Google are coming soon.*
