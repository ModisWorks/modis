import json as _json
import os as _os

_dir = _os.path.dirname(_os.path.realpath(__file__))
_datafile = "{}\\data.json".format(_dir)


def get_serverdata():
    """Gets the current serverdata dict from the serverdata.json file

    Returns:
        serverdata (dict): Parsed serverdata.json file
    """

    with open(_datafile, 'r') as file:
        return _json.load(file)


def write_serverdata(serverdata):
    """Writes an updated serverdata dict to the serverdata.json file

    Args:
        serverdata (dict): The updated serverdata dict
    """

    with open(_datafile, 'w') as file:
        _json.dump(serverdata, file, indent=2)
