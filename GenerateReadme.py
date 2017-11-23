"""Generate a README.md file for Modis"""

import os

from modis import data, helptools

readme = ""


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


def add_ul(text, ul):
    """Adds an unordered list to the readme"""
    text += "\n"
    for li in ul:
        text += "- " + li + "\n"
    text += "\n"

    return text


# Get modules
filepath = os.path.dirname(os.path.realpath(__file__))
database_dir = "{}/modis/discord_modis/modules".format(filepath)
module_list = os.listdir(database_dir)

# Title
readme = add_md(readme, "MODIS", 1)
latest_release = "Latest release: [v{0}{1}]({2}/{0})".format(data.version,
                                                             " Beta" if data.version[0] < "1" else "",
                                                             "https://github.com/Infraxion/modis/releases/tag")
readme = add_md(readme, latest_release)

# About
readme = add_md(readme, "About Modis", 2)
modis_about = """Modis is a Discord bot that runs with a GUI and is designed to be as modular as possible so that anyone with some basic Python knowledge can quickly and easily create new modules that run on the bot."""
readme = add_md(readme, modis_about)

# Module list
readme = add_md(readme, "Current Modules", 2)
module_names = []
for module_name in module_list:
    if len(module_name) > 0 and module_name[0] != "!" and module_name[0] != "_":
        module_names.append("`{}`".format(module_name))
readme = add_md(readme, "There are currently {} modules:".format(len(module_names)))
readme = add_ul(readme, module_names)

for module_name in module_list:
    if len(module_name) > 0 and module_name[0] != "!" and module_name[0] != "_":
        module_dir = "{}/{}".format(database_dir, module_name)
        module_help_path = "{}/{}".format(module_dir, "_help.json")

        if os.path.isfile(module_help_path):
            datepacks = helptools.get_help_datapacks(module_help_path, "!")
            readme = add_md(readme, module_name, 3)

            for d in datepacks:
                if d[0] == "About":
                    readme = add_md(readme, d[1])

# Commands
readme = add_md(readme, "Documentation", 2)
readme = add_md(readme,
                "More detailed information about each module can be found in the [Documentation](https://infraxion.github.io/modis/documentation/#modules).")

newreadme_path = "{}/README.md".format(filepath)
with open(newreadme_path, 'w') as file:
    file.write(readme)
