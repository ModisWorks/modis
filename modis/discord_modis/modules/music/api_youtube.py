import logging
from urllib.parse import urlparse

import googleapiclient.discovery
import soundcloud
from soundcloud.resource import Resource, ResourceList

from modis import datatools

logger = logging.getLogger(__name__)

ytdiscoveryapi = None
scclient = None


def build_api():
    """Build the YouTube API for future use"""
    data = datatools.get_data()
    if "google_api_key" not in data["discord"]["keys"]:
        logger.warning("No API key found with name 'google_api_key'")
        logger.info("Please add your Google API key with name 'google_api_key' " +
                    "in data.json to use YouTube features of the music module")
        return False

    logger.debug("Building YouTube discovery API")
    ytdevkey = data["discord"]["keys"]["google_api_key"]
    try:
        global ytdiscoveryapi
        ytdiscoveryapi = googleapiclient.discovery.build("youtube", "v3", developerKey=ytdevkey)
        logger.debug("YouTube API build successfull")
        return True
    except Exception as e:
        logger.exception(e)
        logger.warning("HTTP error connecting to YouTube API, YouTube won't be available")
        return False


def build_sc_api():
    """Build the SoundCloud API for future use"""
    data = datatools.get_data()
    if "soundcloud_client_id" not in data["discord"]["keys"]:
        logger.warning("No API key found with name 'google_api_key'")
        logger.info(
            "Please add your SoundCloud client id with name 'soundcloud_client_id' " +
            "in data.json to use Soundcloud features of the music module")
        return False

    try:
        global scclient
        scclient = soundcloud.Client(client_id=data["discord"]["keys"]["soundcloud_client_id"])
        logger.debug("SoundCloud build successfull")
        return True
    except Exception as e:
        logger.exception(e)
        return False


def parse_query(query, ilogger):
    """
    Gets either a list of videos from a query, parsing links and search queries and playlists

    Args:
        query (str): The YouTube search query
        ilogger (logging.logger): The logger to log API calls to

    Returns:
        queue (list): The items obtained from the YouTube search
    """

    # Try parsing this as a link
    p = urlparse(query)
    logger.debug("Query: {}".format(p))
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
                return get_queue_from_playlist(yturl_parts["list"])
            elif "v" in yturl_parts:
                return [["https://www.youtube.com/watch?v={}".format(yturl_parts["v"]), query]]
        elif "soundcloud" in p.netloc:
            if scclient is None:
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

                logger.debug(track_list)
                if track_list is not None:
                    return track_list
                else:
                    return [[query, query]]
            except Exception as e:
                logger.exception(e)
            return [[query, query]]
        else:
            logger.debug("Using url: {}".format(query))
            return [[query, query]]

    return get_ytvideos(query, ilogger)


def get_ytvideos(query, ilogger):
    """
    Gets either a list of videos from a playlist or a single video, from the first result of a YouTube search

    Args:
        query (str): The YouTube search query
        ilogger (logging.logger): The logger to log API calls to

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
    ilogger.debug("Queueing {}".format(title))

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


def get_sc_tracks(result):
    if result.kind == "track":
        logger.debug("SoundCloud Track {}".format(result.title))
        return [[result.permalink_url, result.title]]
    elif result.kind == "user":
        track_list = []
        logger.debug("SoundCloud User {}".format(result.username))
        tracks = scclient.get("/users/{}/tracks".format(result.id))
        for t in tracks:
            track_list.append([t.permalink_url, t.title])

        return track_list
    elif result.kind == "playlist":
        track_list = []
        logger.debug("SoundCloud Playlist {}".format(result.title))
        tracks = result.tracks
        for t in tracks:
            track_list.append([t["permalink_url"], t["title"]])

        return track_list

    return None


build_api()
build_sc_api()
