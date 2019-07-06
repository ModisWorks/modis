"""This tool provides easy access to various external APIs, such as Google API, GitHub API etc."""

import logging

import googleapiclient.discovery
import soundcloud
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from modis.tools import data

logger = logging.getLogger(__name__)


def build_youtube():
    """Builds the YouTube API.

    Returns:
        built_api (googleapiclient.discovery.Resource): Built YouTube API if successful, False if not.
    """

    logger.debug("Building YouTube API")

    if "google_api_key" not in data.cache["keys"]:
        logger.warning("No API key found with name 'google_api_key'. Please enter your Google API key in the music module console to use YouTube for music.")
        return False

    try:
        ytdevkey = data.cache["keys"]["google_api_key"]
        built_api = googleapiclient.discovery.build("youtube", "v3", developerKey=ytdevkey)
        logger.debug("YouTube API build successful")
        return built_api
    except Exception as e:
        logger.exception(e)
        logger.error("Error building YouTube API; YouTube won't be available")
        return False


def build_soundcloud():
    """Builds the SoundCloud API.

    Returns:
        built_api (soundcloud.Client): Built SoundCloud API if successful, False if not.
    """

    logger.debug("Building SoundCloud API")

    if "soundcloud_client_id" not in data.cache["keys"]:
        logger.warning("No API key found with name 'soundcloud_client_id'. Please enter your SoundCloud client id in the music module console to use SoundCloud for music.")
        return False

    try:
        built_api = soundcloud.Client(client_id=data.cache["keys"]["soundcloud_client_id"])
        logger.debug("SoundCloud API build successful")
        return built_api
    except Exception as e:
        logger.exception(e)
        logger.error("Error building SoundCloud API; SoundCloud won't be available")
        return False


def build_spotify():
    """Builds the Spotify API.

    Returns:
        built_api (spotify.Spotify): Built Spotify API if successful, False if not.
    """

    logger.debug("Building Spotify API")

    if "spotify_client_id" not in data.cache["keys"]:
        logger.warning("No API key found with name 'spotify_client_id'. Please enter your Spotify client id in the music module console to use Spotify for music.")
        return False
    if "spotify_client_secret" not in data.cache["keys"]:
        logger.warning("No API key found with name 'spotify_client_secret'. Please enter your Spotify client secret in the music module console to use Spotify for music.")
        return False

    try:
        client_credentials_manager = SpotifyClientCredentials(
            data.cache["keys"]["spotify_client_id"],
            data.cache["keys"]["spotify_client_secret"])
        built_api = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
        logger.debug("Spotify API build successful")
        return built_api
    except Exception as e:
        logger.exception(e)
        logger.error("Error building Spotify API; Spotify won't be available")
        return False


client_youtube = build_youtube()
client_soundcloud = build_soundcloud()
client_spotify = build_spotify()
