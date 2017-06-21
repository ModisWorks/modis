import json as _json
import os as _os

_dir = _os.path.dirname(_os.path.realpath(__file__))
_datafile = "data.json".format(_dir)


def get_data():
    """Gets the current data dict of Discord from the data.json file

    Returns:
        data (dict): Parsed data.json file
    """

    with open(_datafile, 'r') as file:
        return _json.load(file)["discord"]


def write_data(data):
    """Writes an updated data dict to the data.json file

    Args:
        data (dict): The updated data dict of Discord
    """

    print("written data")

    temp = get_data()
    temp["discord"] = data

    with open(_datafile, 'w') as file:
        _json.dump(temp, file, indent=2)
