import requests
import lxml.html
import io

import datetime

url = 'https://kakko.pandorabots.com/pandora/talk?botid=f6a012073e345a08&amp;skin=chat'


def get_botcust2():
    """Gets a botcust2, used to identify a speaker with Mitsuku

    Returns:
        botcust2 (str): The botcust2 identifier
    """

    from ._constants import pipe_api_mitsuku
    time = datetime.datetime.now()
    tree_item = pipe_api_mitsuku.insert("", 0, text="get_botcust2()", values=(["", "", time]), open=True)

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
    time1 = datetime.datetime.now()
    tree_item1 = pipe_api_mitsuku.insert(tree_item, 0, text="HTTP POST", values=(["", "", time1]))
    response = requests.post(
        url,
        params=params,
        headers=headers
    )
    pipe_api_mitsuku.item(tree_item1, 0, values=(["", str(response), time1]))

    # Try to extract Mitsuku response from POST response
    time2 = datetime.datetime.now()
    tree_item2 = pipe_api_mitsuku.insert(tree_item, 1, text="Parse", values=([str(response), "", time2]))
    try:
        result = response.headers['set-cookie'][9:25]
    except IndexError:
        result = False
    pipe_api_mitsuku.item(tree_item2, 1, values=([str(response), str(result), time2]))

    pipe_api_mitsuku.insert(tree_item, 2, text="Done", values=(["", "", datetime.datetime.now()]))
    pipe_api_mitsuku.item(tree_item, values=(["", str(result), time]), open=False)
    return result


def query(botcust2, message):
    """Sends a message to Mitsuku and retrieves the reply

    Args:
        botcust2 (str): The botcust2 identifier
        message (str): The message to send to Mitsuku

    Returns:
        reply (str): The message Mitsuku sent back
    """

    from ._constants import pipe_api_mitsuku
    time = datetime.datetime.now()
    tree_item = pipe_api_mitsuku.insert("", 0, text="query()", values=([message, "", time]), open=True)

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
    time1 = datetime.datetime.now()
    tree_item1 = pipe_api_mitsuku.insert(tree_item, 0, text="HTTP POST", values=([message, "", time1]))
    response = requests.post(
        url,
        params=params,
        headers=headers,
        data=data
    )
    pipe_api_mitsuku.item(tree_item1, values=([message, str(response), time1]))

    # Parse response
    time2 = datetime.datetime.now()
    tree_item2 = pipe_api_mitsuku.insert(tree_item, 1, text="Parse", values=([str(response), "", time2]))
    parsed = lxml.html.parse(io.StringIO(response.text)).getroot()
    try:
        result = parsed[1][2][0][2].tail[1:]
    except IndexError:
        result = False
    pipe_api_mitsuku.item(tree_item2, values=([str(response), str(result), time2]))

    pipe_api_mitsuku.insert(tree_item, 2, text="Done", values=(["", "", datetime.datetime.now()]))
    pipe_api_mitsuku.item(tree_item, values=([message, str(result), time]), open=False)
    return result
