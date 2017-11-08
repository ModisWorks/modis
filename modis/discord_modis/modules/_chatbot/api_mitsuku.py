import logging

import requests
import lxml.html
import io

logger = logging.getLogger(__name__)

url = 'https://kakko.pandorabots.com/pandora/talk?botid=f6a012073e345a08&amp;skin=chat'


def get_botcust2():
    """Gets a botcust2, used to identify a speaker with Mitsuku

    Returns:
        botcust2 (str): The botcust2 identifier
    """
    logger.debug("Getting new botcust2")

    # Set up http request packages
    params = {
        'botid': 'f6a012073e345a08',
        'amp;skin': 'chat'
    }
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch, br',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive',
        'DNT': '1',
        'Host': 'kakko.pandorabots.com',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/58.0.3029.110 Safari/537.36'
    }

    # Get response from http POST request to url
    logger.debug("Sending POST request")
    response = requests.post(
        url,
        params=params,
        headers=headers
    )
    logger.debug("POST response {}".format(response))

    # Try to extract Mitsuku response from POST response
    try:
        result = response.headers['set-cookie'][9:25]
        logger.debug("Getting botcust2 successful")
    except IndexError:
        result = False
        logger.critical("Getting botcust2 from html failed")

    return result


def query(botcust2, message):
    """Sends a message to Mitsuku and retrieves the reply

    Args:
        botcust2 (str): The botcust2 identifier
        message (str): The message to send to Mitsuku

    Returns:
        reply (str): The message Mitsuku sent back
    """
    logger.debug("Getting Mitsuku reply")

    # Set up http request packages
    params = {
        'botid': 'f6a012073e345a08',
        'amp;skin': 'chat'
    }
    headers = {
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Length': str(len(message) + 34),
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': 'botcust2=' + botcust2,
        'DNT': '1',
        'Host': 'kakko.pandorabots.com',
        'Origin': 'https://kakko.pandorabots.com',
        'Referer': 'https://kakko.pandorabots.com/pandora/talk?botid=f6a012073e345a08&amp;skin=chat',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/58.0.3029.110 Safari/537.36'
    }
    data = {
        'botcust2': botcust2,
        'message': message
    }

    # Get response from http POST request to url
    logger.debug("Sending POST request")
    response = requests.post(
        url,
        params=params,
        headers=headers,
        data=data
    )
    logger.debug("POST response {}".format(response))

    # Parse response
    parsed = lxml.html.parse(io.StringIO(response.text)).getroot()
    try:
        result = parsed[1][2][0][2].tail[1:]
        logger.debug("Getting botcust2 successful")
    except IndexError:
        result = False
        logger.critical("Getting botcust2 from html failed")

    return result
