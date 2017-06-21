import discord

import json as _json
import os as _os
import asyncio as _asyncio

apikeys = {}
client_id = ""
game = ""
prefix = ""

client = discord.Client()


def get_serverdata():
    """Gets the current serverdata dict from the serverdata.json file

    Returns:
        serverdata (dict): Parsed serverdata.json file
    """

    with open(_os.path.dirname(_os.path.realpath(__file__)) + "\\" + "serverdata.json", 'r') as file:
        return _json.load(file)


def write_serverdata(new_serverdata):
    """Writes an updated serverdata dict to the serverdata.json file

    Args:
        new_serverdata (dict): The updated serverdata dict
    """

    with open(_os.path.dirname(_os.path.realpath(__file__)) + "\\" + "serverdata.json", 'w') as file:
        _json.dump(new_serverdata, file, indent=2)


def runcoro(async_function):
    """Runs an asynchronous function without needing to use await - useful for lambda

    Args:
        async_function (Coroutine): The asynchronous function to run
    """

    future = _asyncio.run_coroutine_threadsafe(async_function, client.loop)
    result = future.result()
    return result
