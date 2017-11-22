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

#### SoundCloud

To search SoundCloud, use `soundcloud` or `sc` before your query.

- `!play sc [query]`: Searches SoundCloud using the query and plays the first song
- `!play sc song [query]`: Searches SoundCloud using the query and plays the first song
- `!play sc songs [query]`: Searches SoundCloud using the query and plays the top songs that match the query
- `!play sc user [query]`: Searches SoundCloud for a user and plays their most recent songs
- `!play sc playlist [query]`: Searches SoundCloud for a playlist and queues songs from the first result
- `!play sc tagged [query]`: Searches SoundCloud for songs with a given tag and plays the top songs with that tag
- `!play sc genre [query]`: Searches SoundCloud for songs with a given genre and plays the top songs with that genre

All these commands will work for any commands in the `!play` family, for example: `!playshuffle sc genre house` will play the top songs on SoundCloud in the 'house' genre in a random order.

### pause

- `!pause`: Pauses the currently playing song

### resume

- `!resume`: Resumes the currently playing song

### shuffle

- `!shuffle`: Randomly shuffles the remaining songs in the queue

### skip

- `!skip`: Skips the current song
- `!skip [n]`: Skips [n] songs

### loop

- `!loop on`: Tells the music module to loop all songs from this session after the queue is empty
- `!loop shuffle`: Tells the music module to loop all songs from this session in a random order after the queue is empty
- `!loop off`: Tells the music module not to loop any songs once the queue is empty

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
