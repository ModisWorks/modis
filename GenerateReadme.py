"""Generate a README.md file for Modis"""

from modis.tools import config, moduledb, version, help


def add_md(text, s, level=0):
    """Appends text to a markdown.

    Args:
        text (str): The old text.
        s (str): The text to append.
        level (int): The markdown level of the appended text.

    Returns:
        text (str): The updated text
    """

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
    """Appends an unordered list to a markdown.

    Args:
        text (str): The old text.
        ul (list): The list to append.

    Returns:
        text (str): The updated text.
    """

    text += "\n"
    for li in ul:
        text += "- " + li + "\n"
    text += "\n"

    return text


# Init
readme = ""
module_names = moduledb.get_modules()
module_files = moduledb.get_file(["_help.json"])["_help.json"]

# Title
readme = add_md(readme, "MODIS", 1)
readme = add_md(readme, "Latest release: [v{0}{1}]({2}/{0})".format(
    version.VERSION,
    " Beta" if version.VERSION[0] < "1" else "",
    "https://github.com/Infraxion/modis/releases/tag"
))

# About
readme = add_md(readme, "About Modis", 2)
readme = add_md(readme, "Modis is a Discord bot that runs with a GUI and is "
                        "designed to be as modular as possible so that anyone "
                        "with some basic Python knowledge can quickly and "
                        "easily create new modules that run on the bot.")

# Module list
readme = add_md(readme, "Current Modules", 2)
readme = add_md(readme, "There are currently {} available modules:".format(len(module_names)))
module_list = []
for m in module_names:
    datapack = help.get_help_data(m)
    if "About" in datapack.keys():
        info = "`{}` - {}".format(m, datapack["About"])
    else:
        info = "`{}`".format(m)
    module_list.append(info)
readme = add_ul(readme, [m for m in module_list])
readme = add_md(readme, "More detailed information about each module can be "
                        "found in the [docs](https://infraxion.github.io/modis"
                        "/documentation/#modules).")

# Write file
newreadme_path = "{}/README.md".format(config.ROOT_DIR)
with open(newreadme_path, 'w') as file:
    file.write(readme)
