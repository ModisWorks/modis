import requests
from pprint import pprint


def send_replay():
    pass


def get_replay():
    response = requests.get(
        "https://www.rocketleaguereplays.com/api/replays?owned",
        params={
            # "owned": ""
        }
    )
    print(response)
    print(response.url)
    pprint(response.json())

    # _id = response.json()['id']
    #
    # response = requests.post(
    #     "https://www.rocketleaguereplays.com/api/replays/{}".format(_id)
    # )
    # print(response)
    # pprint(response.json())


get_replay()
