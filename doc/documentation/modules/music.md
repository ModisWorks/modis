---
title: Music Module
permalink: /documentation/modules/music/
---
# Music

The music module allows you to play videos and playlists from YouTube, as well as other sources such as SoundCloud, or streaming from places like Twitch or online radio services.

## Commands

### play

- `!play [query/link]`: Starts playing the first result of the query or link
- `!playnext [query/link]`: Starts playing the query or link after the current song has finished
- `!playnow [query/link]`: Stops playing the current song and starts playing the query or link
- `!playshuffle [query/link]`: Adds the first result of the query or link to the queue, and shuffles the queue

### pause

- `!pause`: Pauses the currently playing song

### resume

- `!resume`: Resumes the currently playing song

### shuffle

- `!shuffle`: Randomly shuffles the remaining songs in the queue

### skip

- `!skip`: Skips the current song
- `!skip [n]`: Skips [n] songs

### remove

- `!remove [index]`: Removes the song from the queue at [index]
- `!remove all`: Removes all songs from the queue

### rewind

- `!rewind [n]`: Rewinds the queue [n] songs
- `!restart`: Restarts the current song

### volume

- `!volume [v]`: Sets the volume to [v]% (must be between 0% and 200%)

### stop

- `!stop`: Stops the currently playing song, clears the queue, and disconnects from voice

### topic

- `!settopic`: Sets Modis to update this channel's topic with the currently playing song
- `!cleartopic`: Stops Modis from updating this channel's topic with the currently playing song

### destroy

- `!destroy`: Stops and removes the music player

### front

- `!front`: Moves the music player to the front of the channel the command was sent from
