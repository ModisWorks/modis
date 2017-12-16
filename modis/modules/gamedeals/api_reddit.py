import logging
import praw

from modis.tools import data

logger = logging.getLogger(__name__)

redditapi = None


def build_api():
    if "reddit_api_user_agent" not in data.cache["keys"] or \
            "reddit_api_client_id" not in data.cache["keys"] or \
            "reddit_api_client_secret" not in data.cache["keys"]:
        logger.warning("For gamedeals to work, please make sure "
                       "\"reddit_api_user_agent\", \"reddit_api_client_id\", "
                       "and \"reddit_api_client_secret\" are all added as API "
                       "keys")

    logger.debug("Building Reddit API")
    try:
        global redditapi
        redditapi = praw.Reddit(
            user_agent=data.cache["keys"]["reddit_api_user_agent"],
            client_id=data.cache["keys"]["reddit_api_client_id"],
            client_secret=data.cache["keys"]["reddit_api_client_secret"])
        logger.debug("Build successfull")
        return True
    except:
        logger.warning("Error connecting to Reddit API, Reddit won't be available")
        return False


def get_top10(threshold=200):
    logger.debug("get_top10 with threshold {}".format(threshold))
    posts = []
    for post in redditapi.subreddit("gamedeals").hot(limit=10):
        if post.score > threshold:
            posts.append((post.title, post.url, post.score))

    return posts


build_api()
