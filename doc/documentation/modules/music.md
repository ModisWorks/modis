# music


## Play Commands

- `!play [query/link]`: Starts playing the first result of the query or link, or adds it to the end of the queue if something is already playing
- `!playnow [query/link]`: Stops playing the current song and starts playing the first result of the query or link
- `!playnext [query/link]`: Starts playing the first result of the query or link after the current song has finished
- `!playshuffle [query/link]`: Plays the first result of the query or link in a random order
- `!insert [index] [query/link]`: Adds the first result of the query of link at the given index


## Music Player Commands

- `!pause`: Pauses the currently playing song
- `!resume`: Resumes the currently playing song
- `!shuffle`: Randomly shuffles the remaining songs in the queue
- `!skip [n]`: Skips [n] songs
- `!rewind [n]`: Rewinds the queue [n] songs
- `!remove [index]`: Removes the song from the queue at [index], you can remove a range of songs by giving the index in the form #-#
- `!volume [v]`: Sets the volume to [v]% (must be between 0% and 200%)
- `!stop`: Stops the currently playing song, clears the queue, and disconnects from voice
- `!destroy`: Stops and removes the music player


## SoundCloud Commands

- `!play sc [query]`: Searches SoundCloud using the query and plays the first song
- `!play sc song [query]`: Searches SoundCloud using the query and plays the first song
- `!play sc songs [query]`: Searches SoundCloud using the query and plays the top songs that match the query
- `!play sc user [query]`: Searches SoundCloud for a user and plays their most recent songs
- `!play sc playlist [query]`: Searches SoundCloud for a playlist and queues songs from the first result
- `!play sc tagged [query]`: Searches SoundCloud for songs with a given tag and plays the top songs with that tag
- `!play sc genre [query]`: Searches SoundCloud for songs with a given genre and plays the top songs with that genre


## Utility Commands

- `!loop [off/on/shuffle]`: Sets the loop state for this session: 'off' will stop looping, 'on' will loop everything played this session when the queue finishes, 'shuffle' will shuffle before looping
- `!settopic`: Sets Modis to update this channel's topic with the currently playing song
- `!cleartopic`: Stops Modis from updating this channel's topic with the currently playing song
- `!front`: Moves the music player to the front of the channel the command was sent from


## Documentation

To see all commands, go to the Music Module Documentation at https://infraxion.github.io/modis/documentation/modules/music/

## About

music plays videos and playlists from YouTube, and music files stored on the internet.

## Creators

Infraxion and YtnomSnrub
