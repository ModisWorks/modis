"""Generate a README.md file for Modis"""

from modis.tools import help, config


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


moduledoc = ""

# Get module
module_name = input("Module name: ")

# Get help data
datapacks = help.get_formatted(module_name, "!")
if datapacks:
    moduledoc = add_md(moduledoc, module_name, 1)
    for d in datapacks:
        moduledoc = add_md(moduledoc, d[0], 2)
        moduledoc = add_md(moduledoc, d[1])

    print(moduledoc)
    newreadme_path = "{}/../{}.md".format(config.ROOT_DIR, module_name)
    with open(newreadme_path, 'w') as file:
        file.write(moduledoc)
