"""
This file can be thought of as a save file. The file itself isn't edited but
contains references to variables in RAM, making it easy for other modules to
access global variables.
"""

import os as _os

ROOT_DIR = _os.path.dirname(_os.path.realpath(__file__))

client = None
