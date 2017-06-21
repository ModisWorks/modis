## About Modis
Modis is a Discord bot that runs with a GUI and is designed to be as modular as possible so that anyone with some Python knowledge can quickly and easily create new modules that run on the bot.

## Currently available modules
There are currently 5 modules in Modis:
- music
- replies
- tableflip
- chatbot
- rocketleague

Information about each module is detailed below.

### music
A music player with an interactive GUI using reactions as buttons.

**Commands:**
- `!play [YouTube search OR url]`: Creates the player GUI if it doesn't yet exist and queues either the first result of a YouTube search or the audio from the url.
- `!pause`: Pauses the player.
- `!skip [n]`: Skips `n` songs, or skips one if `n` is not included.
- `!shuffle`: Shuffles the songs in the queue.
- `!stop`: Stops the player and clears the queue.
- `!volume [n]`: Sets the volume to `n`%. `n` can be any integer from 0 to 200.
- `!destroy`: Removes the GUI and resets everything. Handy if something is messed up.
- `!front` or `!movehere`: Moves the GUI to the channel you're currently in. If it's already in your channel it gets moved to the bottom where you can see it.

### replies
Replies uses a json file to make it easy for users to make the bot say things in reply to specific messages.

### tableflip
A fun module that puts the table back whenever someone flips it.

### chatbot
Whenever the bot is mentioned this module can connect to either cleverbot.io or Mitsuku and get a chatbot reply to the message it was mentioned in.

### rocketleague
Gets Rocket League stats of players using Rocket League Tracker Network. Currently only works for Steam players.

**Commands:**
- `!rl [steamid]` Shows the Rocket League stats of the Steam user `steamid`.