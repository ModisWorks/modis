import logging

from .... import datatools

import praw

logger = logging.getLogger(__name__)

redditapi = None


def build_api():
    logger.debug("Building Reddit API")
    try:
        global redditapi
        redditapi = praw.Reddit(
            user_agent=datatools.get_data()["discord"]["reddit_api_user_agent"],
            client_id=datatools.get_data()["discord"]["reddit_api_client_id"],
            client_secret=datatools.get_data()["discord"]["reddit_api_client_secret"])
        logger.debug("Build successfull")
        return True
    except:
        logger.critical("Error connecting to Reddit API, build failed")
        return False


def get_top10(threshold=200):
    logger.debug("get_top10 with threshold {}".format(threshold))
    posts = []
    for post in redditapi.subreddit("gamedeals").hot(limit=10):
        if post.score > threshold:
            posts.append((post.title, post.url, post.score))

    return posts

build_api()
