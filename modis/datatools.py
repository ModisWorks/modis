"""Read and write json data."""

import json as _json
import os as _os

_dir = _os.path.dirname(_os.path.realpath(__file__))
_datafile = "data.json".format(_dir)


def has_data() -> bool:
    """
    Checks whether or not a data.json file has been created

    Returns:
        exists (bool): True if a data file exists, False otherwise
    """

    return _os.path.exists(_datafile)


def get_data() -> dict:
    """
    Get the current data dict of Discord from the data.json file

    Returns:
        data (dict): Parsed data.json file
    """

    with open(_datafile, 'r') as file:
        return _json.load(file)


def write_data(data: dict):
    """
    Write the data to the data.json file

    Args:
        data (dict): The updated data dictionary for Modis
    """
    with open(_datafile, 'w') as file:
        _json.dump(data, file, indent=2)
