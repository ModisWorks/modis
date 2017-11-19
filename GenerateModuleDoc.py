"""Generate a README.md file for Modis"""

import os

from modis import helptools

moduledoc = ""


def add_md(text, s, level=0):
    """Adds text to the readme at the given level"""
    if level > 0:
        if text != "":
            text += "\n"
        text += "#" * level
        text += " "

    text += s + "\n"

    if level > 0:
        text += "\n"

    return text


# Get module
module_name = input("Module name: ")
filepath = os.path.dirname(os.path.realpath(__file__))
module_dir = "{}/modis/discord_modis/modules/{}".format(filepath, module_name)
module_help_path = "{}/{}".format(module_dir, "_help.json")

# Get help data
if os.path.isfile(module_help_path):
    datepacks = helptools.get_help_datapacks(module_help_path, "!")
    moduledoc = add_md(moduledoc, module_name, 1)

    for d in datepacks:
        moduledoc = add_md(moduledoc, d[0], 2)
        moduledoc = add_md(moduledoc, d[1])
else:
    print(module_help_path, "is not a file")

newreadme_path = "{}/{}.md".format(filepath, module_name)
with open(newreadme_path, 'w') as file:
    file.write(moduledoc)
