import logging

import googleapiclient.discovery
from urllib.parse import urlparse
from modis import datatools

logger = logging.getLogger(__name__)

ytdiscoveryapi = None


def build_api():
    data = datatools.get_data()
    if "google_api_key" not in data["discord"]["keys"]:
        logger.critical("No API key found with name 'google_api_key'")
        logger.info("Please add your google API key with name 'google_api_key' int the control panel")
        return False

    logger.debug("Building YouTube discovery API")
    ytdevkey = data["discord"]["keys"]["google_api_key"]
    try:
        global ytdiscoveryapi
        ytdiscoveryapi = googleapiclient.discovery.build("youtube", "v3", developerKey=ytdevkey)
        logger.debug("Build successfull")
        return True
    except:
        logger.critical("HTTP error connecting to YouTube API, build failed")
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
    if p and p.scheme and p.netloc and p.query:
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


build_api()
