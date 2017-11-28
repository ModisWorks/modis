# MODIS

Latest release: [v0.4.0 Beta](https://github.com/Infraxion/modis/releases/tag/0.4.0)

## About Modis

Modis is an highly modular, open-source Discord bot that runs with a console GUI. Our goal is to make Modis as easy to host as possible, so that any Discord user can host their own bot. Modis is also designed to be very easy to develop for; it's modularised in a way that makes it very easy to understand for anyone familiar with the discord.py Python library.

We hope that this bot introduces more novices to the painful world of software development and networking, and provides seasoned devs with something to procrastinate their deadline on. Have fun!

## Current Modules

There are currently 10 available modules:

- `!core` - Manages all the behind the scenes stuff that runs the internal APIs the modules use.
- `bethebot` - Modis can't really have conversations with your server members, but you can fake it by taking control!
- `gamedeals` - Posts current hot posts above an upvote threshold of a particular subreddit. It's set to /r/gamedeals by default so you can make sure you don't miss any sales!
- `help` - Modis is a big bot, so this module helps to alleviate the learning cliff by allowing easy access to command definitions inside Discord.
- `hex` - Displays hex colours if it sees them in your messages. Handy for graphic designers and programmers.
- `manager` - Provides essential server management tools for server owners, such as activating and deactivating modules, changing the command prefix, and various moderation tools.
- `music` - Modis' flagship module - a music player featuring a live-updating GUI with a progress bar, queue display, and more. The GUI also has working media buttons for easy control without needing to know any commands. The player supports songs and playlists for YouTube, Spotify, and SoundCloud, and can play most online audio sources.
- `replies` - Allows server owners to easily set the bot to reply to specific phrases.
- `rocketleague` - Looks up your Rocket League rank and stats; currently supported for Steam, XBox, and PS4 players.
- `tableflip` - The best module.

More detailed information about each module and how to use them can be found in the [docs](https://infraxion.github.io/modis/documentation/#modules).
