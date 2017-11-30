import logging
from urllib.parse import urlparse

import googleapiclient.discovery
import soundcloud
import spotipy
from soundcloud.resource import Resource, ResourceList
from spotipy.oauth2 import SpotifyClientCredentials

from modis import datatools

logger = logging.getLogger(__name__)

ytdiscoveryapi = None
scclient = None
spclient = None

SOURCE_TO_NAME = {
    "soundcloud": "SoundCloud",
    "twitchstream": "Twitch",
    "youtube": "YouTube"
}


def build_yt_api():
    """Build the YouTube API for future use"""
    data = datatools.get_data()
    if "google_api_key" not in data["discord"]["keys"]:
        logger.warning("No API key found with name 'google_api_key'")
        logger.info("Please add your Google API key with name 'google_api_key' "
                    "in data.json to use YouTube features of the music module")
        return False

    logger.debug("Building YouTube discovery API")
    ytdevkey = data["discord"]["keys"]["google_api_key"]

    try:
        global ytdiscoveryapi
        ytdiscoveryapi = googleapiclient.discovery.build("youtube", "v3", developerKey=ytdevkey)
        logger.debug("YouTube API build successful")
        return True
    except Exception as e:
        logger.exception(e)
        logger.warning("HTTP error connecting to YouTube API, YouTube won't be available")
        return False


def build_sc_api():
    """Build the SoundCloud API for future use"""
    data = datatools.get_data()
    if "soundcloud_client_id" not in data["discord"]["keys"]:
        logger.warning("No API key found with name 'soundcloud_client_id'")
        logger.info("Please add your SoundCloud client id with name 'soundcloud_client_id' "
                    "in data.json to use Soundcloud features of the music module")
        return False

    try:
        global scclient
        scclient = soundcloud.Client(client_id=data["discord"]["keys"]["soundcloud_client_id"])
        logger.debug("SoundCloud build successful")
        return True
    except Exception as e:
        logger.exception(e)
        return False


def build_spotify_api():
    """Build the Spotify API for future use"""
    data = datatools.get_data()
    if "spotify_client_id" not in data["discord"]["keys"]:
        logger.warning("No API key found with name 'spotify_client_id'")
        logger.info("Please add your Spotify client id with name 'spotify_client_id' "
                    "in data.json to use Spotify features of the music module")
        return False
    if "spotify_client_secret" not in data["discord"]["keys"]:
        logger.warning("No API key found with name 'spotify_client_secret'")
        logger.info("Please add your Spotify client secret with name 'spotify_client_secret' "
                    "in data.json to use Spotify features of the music module")
        return False

    try:
        global spclient
        client_credentials_manager = SpotifyClientCredentials(
                data["discord"]["keys"]["spotify_client_id"],
                data["discord"]["keys"]["spotify_client_secret"])
        spclient = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
        logger.debug("Spotify build successful")
        return True
    except Exception as e:
        logger.exception(e)
        return False


def parse_query(query, ilogger):
    """
    Gets either a list of videos from a query, parsing links and search queries
    and playlists

    Args:
        query (str): The YouTube search query
        ilogger (logging.logger): The logger to log API calls to

    Returns:
        queue (list): The items obtained from the YouTube search
    """

    # Try parsing this as a link
    p = urlparse(query)
    if p and p.scheme and p.netloc:
        if "youtube" in p.netloc and p.query and ytdiscoveryapi is not None:
            query_parts = p.query.split('&')
            yturl_parts = {}
            for q in query_parts:
                s = q.split('=')
                if len(s) < 2:
                    continue

                q_name = s[0]
                q_val = '='.join(s[1:])
                # Add to the query
                if q_name not in yturl_parts:
                    yturl_parts[q_name] = q_val

            if "list" in yturl_parts:
                ilogger.info("Queued YouTube playlist from link")
                return get_queue_from_playlist(yturl_parts["list"])
            elif "v" in yturl_parts:
                ilogger.info("Queued YouTube video from link")
                return [["https://www.youtube.com/watch?v={}".format(yturl_parts["v"]), query]]
        elif "soundcloud" in p.netloc:
            if scclient is None:
                ilogger.error("Could not queue from SoundCloud API, using link")
                return [[query, query]]
            try:
                result = scclient.get('/resolve', url=query)

                track_list = []
                if isinstance(result, ResourceList):
                    for r in result.data:
                        tracks = get_sc_tracks(r)
                        if tracks is not None:
                            for t in tracks:
                                track_list.append(t)
                elif isinstance(result, Resource):
                    tracks = get_sc_tracks(result)
                    if tracks is not None:
                        for t in tracks:
                            track_list.append(t)

                if track_list is not None and len(track_list) > 0:
                    ilogger.info("Queued SoundCloud songs from link")
                    return track_list
                else:
                    ilogger.error("Could not queue from SoundCloud API")
                    return [[query, query]]
            except Exception as e:
                logger.exception(e)
                ilogger.error("Could not queue from SoundCloud API, using link")
                return [[query, query]]
        elif "spotify" in p.netloc:
            if spclient is None:
                ilogger.error("Could not resolve song from Spotify API, No Key?")
                return []
            else:
                url_to_uri = ("spotify"+p.path).replace("/",":")
                return parse_query(url_to_uri, ilogger)
        else:
            ilogger.debug("Using url: {}".format(query))
            return [[query, query]]

    args = query.split(' ')
    if len(args) == 0:
        ilogger.error("No query given")
        return []
    #--------Spotify Patch--------
    uri = query.split(":")
    if uri[0].lower() in ["spotify"] and spclient is not None:
        if spclient is None:
            ilogger.error("Host does not support Spotify")
            return []

        try:
            if len(uri) > 2 and uri[1] in ["album", "artist", "track", "user"]:
                query_type = uri[1].lower()
                query_search = ' '.join(uri[2:])
            else:
                ilogger.error("Error malformed Spotify URI/URL")
                return []

            query_type = query_type.replace('user', 'playlist')
            spotify_tracks = get_sp_tracks(query_type, query_search)
            logger.debug("Queueing Yotube search: {}".format(spotify_tracks))
            ilogger.info("Queued Spotify {} URI: {}".format(query_type, query_search))
            return get_ytvideos_from_list(spotify_tracks)
    #This sends the track name and artist found with the spotifyAPI to youtube
    #--------Spotify Patch--------
        except Exception as e:
            logger.exception(e)
            ilogger.error("Error queueing from Spotify")
            return []
    elif args[0].lower() in ["sc", "soundcloud"]:
        if scclient is None:
            ilogger.error("Host does not support SoundCloud")
            return []

        try:
            requests = ['song', 'songs', 'track', 'tracks', 'user', 'playlist', 'tagged', 'genre']
            if len(args) > 2 and args[1] in requests:
                query_type = args[1].lower()
                query_search = ' '.join(args[2:])
            else:
                query_type = 'track'
                query_search = ' '.join(args[1:])
            query_type = query_type.replace('song', 'track')
            ilogger.info("Queueing SoundCloud {}: {}".format(query_type, query_search))
            soundcloud_tracks = search_sc_tracks(query_type, query_search)
            ilogger.info("Queued SoundCloud {}: {}".format(query_type, query_search))
            return soundcloud_tracks
        except Exception as e:
            logger.exception(e)
            ilogger.error("Could not queue from SoundCloud")
            return []
    elif args[0].lower() in ["yt", "youtube"] and ytdiscoveryapi is not None:
        if ytdiscoveryapi is None:
            ilogger.error("Host does not support YouTube")
            return []

        try:
            query_search = ' '.join(args[1:])
            ilogger.info("Queued Youtube search: {}".format(query_search))
            return get_ytvideos(query_search)
        except Exception as e:
            logger.exception(e)
            ilogger.error("Could not queue YouTube search")
            return []

    if ytdiscoveryapi is not None:
        ilogger.info("Queued YouTube search: {}".format(query))
        return get_ytvideos(query)
    else:
        ilogger.error("Host does not support YouTube".format(query))
        return []


def get_ytvideos_from_list(queries):
    """
    Gets either a list of videos from a playlist or a single video, using the
    first result of a YouTube search

    Args:
        queries (list): A list of queries to make

    Returns:
        queue (list): The items obtained from the YouTube search
    """
    queue = []
    if isinstance(queries, str) == True:
        results = get_ytvideos(queries)
        if len(results) > 0:
            queue.append(results[0])
    else:
        for query in queries:
            results = get_ytvideos(query)
            if len(results) > 0:
                queue.append(results[0])

    return queue


def get_ytvideos(query):
    """
    Gets either a list of videos from a playlist or a single video, using the
    first result of a YouTube search

    Args:
        query (str): The YouTube search query

    Returns:
        queue (list): The items obtained from the YouTube search
    """

    queue = []
    # Search YouTube
    search_result = ytdiscoveryapi.search().list(
            q=query,
            part="id,snippet",
            maxResults=1,
            type="video,playlist"
    ).execute()

    if not search_result["items"]:
        return []

    # Get video/playlist title
    title = search_result["items"][0]["snippet"]["title"]

    # Queue video if video
    if search_result["items"][0]["id"]["kind"] == "youtube#video":
        # Get ID of video
        videoid = search_result["items"][0]["id"]["videoId"]

        # Append video to queue
        queue.append(["https://www.youtube.com/watch?v={}".format(videoid), title])

    # Queue playlist if playlist
    elif search_result["items"][0]["id"]["kind"] == "youtube#playlist":
        queue = get_queue_from_playlist(search_result["items"][0]["id"]["playlistId"])
    return queue


def get_queue_from_playlist(playlistid):
    queue = []
    # Get items in playlist
    playlist = ytdiscoveryapi.playlistItems().list(
            playlistId=playlistid,
            part="snippet",
            maxResults=50
    ).execute()

    # Append videos to queue
    for entry in playlist["items"]:
        videoid = entry["snippet"]["resourceId"]["videoId"]
        songname = entry["snippet"]["title"]
        queue.append(["https://www.youtube.com/watch?v={}".format(videoid), songname])

    # For playlists with more than 50 entries
    if "nextPageToken" in playlist:
        counter = 2

        while "nextPageToken" in playlist:
            counter += 1

            # Get items in next page of playlist
            playlist = ytdiscoveryapi.playlistItems().list(
                    playlistId=playlistid,
                    part="snippet",
                    maxResults=50,
                    pageToken=playlist["nextPageToken"]
            ).execute()

            # Append videos to queue
            for entry in playlist["items"]:
                videoid = entry["snippet"]["resourceId"]["videoId"]
                songname = entry["snippet"]["title"]
                queue.append(["https://www.youtube.com/watch?v={}".format(videoid), songname])

    return queue


def search_sc_tracks(query_type, query_search):
    results = []
    if query_type == 'track':
        results = scclient.get("/tracks", q=query_search, filter="public", limit=1)
    elif query_type == 'tracks':
        results = scclient.get("/tracks", q=query_search, filter="public", limit=50)
    elif query_type == 'user':
        results = scclient.get("/users", q=query_search, limit=1)
    elif query_type == 'playlist':
        results = scclient.get("/playlists", q=query_search, limit=1)
    elif query_type == 'tagged':
        while ", " in query_search:
            query_search = query_search.replace(", ", ",").strip()
        results = scclient.get("/tracks", tags=query_search, filter="public", limit=50)
    elif query_type == 'genre':
        while ", " in query_search:
            query_search = query_search.replace(", ", ",").strip()
        results = scclient.get("/tracks", genres=query_search, filter="public", limit=50)

    sc_tracks = []
    for r in results:
        result_tracks = get_sc_tracks(r)
        if result_tracks is not None:
            for t in result_tracks:
                sc_tracks.append(t)

    return sc_tracks


def get_sc_tracks(result):
    if result.kind == "track":
        logger.debug("SoundCloud Track {}".format(result.title))
        return [[result.stream_url, result.title]]
    elif result.kind == "user":
        track_list = []
        logger.debug("SoundCloud User {}".format(result.username))
        tracks = scclient.get("/users/{}/tracks".format(result.id), limit=50)
        for t in tracks:
            track_list.append([t.stream_url, t.title])

        return track_list
    elif result.kind == "playlist":
        track_list = []
        logger.debug("SoundCloud Playlist {}".format(result.title))
        playlist = scclient.get("/playlists/{}".format(result.id), limit=50)
        tracks = playlist.tracks
        for t in tracks:
            track_list.append([t["stream_url"], t["title"]])

        return track_list

    return None

#--------Spotify Patch--------

def get_sp_tracks(query_type, query_search):
    if query_type == 'track':
        results = spclient.track(query_search) # looks up the URI on spotify
        song_name = results['name'] # gather the name of the song by looking for the tag ['name']
        song_artist = results['artists'][0]['name'] # same as before, might only return the first artist, unsure
        query = ("{} by {}".format(song_name,song_artist)) # joins both results
        return(query) # sends query back to parse_query
    elif query_type == 'artist':
        listofsongs = []
        results = spclient.artist_top_tracks(query_search)
        for tracks in results['tracks'][:10]: # finds all tracks in the album
             song_name = tracks['name']
             song_artist = tracks['artists'][0]['name']
             query = ("{} by {}".format(song_name,song_artist))
             listofsongs.append(query)
        return(listofsongs)
    elif query_type == 'album':
        listofsongs = []
        results = spclient.album_tracks(query_search)
        for tracks in results['items']: # finds all tracks in the album
             song_name = tracks['name']
             song_artist = tracks['artists'][0]['name']
             query = ("{} by {}".format(song_name,song_artist))
             listofsongs.append(query)
        return(listofsongs)
    elif query_type == 'playlist':
        listofsongs = []
        get_username = query_search.split(" ")[0]
        get_playlist = query_search.split(" ")[2]
        results = spclient.user_playlist_tracks(get_username, get_playlist)
        for tracks in results['items']: # finds all tracks in the album
             song_name = tracks['track']['name']
             song_artist = tracks['track']['artists'][0]['name']
             query = ("{} by {}".format(song_name,song_artist))
             listofsongs.append(query)
        return(listofsongs)

    return []

#--------Spotify Patch--------

def duration_to_string(duration):
    """
    Converts a duration to a string

    Args:
        duration (int): The duration in seconds to convert

    Returns s (str): The duration as a string
    """

    m, s = divmod(duration, 60)
    h, m = divmod(m, 60)
    return "%d:%02d:%02d" % (h, m, s)


def parse_source(info):
    """
    Parses the source info from an info dict generated by youtube-dl

    Args:
        info (dict): The info dict to parse

    Returns:
        source (str): The source of this song
    """

    if "extractor_key" in info:
        source = info["extractor_key"]
        lower_source = source.lower()

        for key in SOURCE_TO_NAME:
            lower_key = key.lower()
            if lower_source == lower_key:
                source = SOURCE_TO_NAME[lower_key]

        if source != "Generic":
            return source

    if "url" in info and info["url"] is not None:
        p = urlparse(info["url"])
        if p and p.netloc:
            return p.netloc

    return "Unknown"


build_yt_api()
build_sc_api()
build_spotify_api()
