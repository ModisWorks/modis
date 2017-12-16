"""
This tool retrieves help data from the __info.py files in each module.
"""

import logging

from modis.tools import moduledb

logger = logging.getLogger(__name__)


def get_raw(module_name):
    """Get a dict from a __info.py.

    Args:
        module_name (str): The name of the module to get help for.

    Returns:
        data (OrderedDict): The dict of the help.json
    """

    info = moduledb.get_import_specific("__info", module_name)

    if not info:
        # Info file does not exist in module
        return {}
    if not info.HELP_DATAPACKS:
        # Info file does not contain help data
        return {}
    return info.HELP_DATAPACKS


def get_md(module_name, prefix="!"):
    """Load help text from a __info.py and format into markdown datapacks.

    Args:
        module_name (str): The name of the module to get help for.
        prefix (str): The prefix to use for commands.

    Returns:
        datapacks (list): The formatted data.
    """

    info = moduledb.get_import_specific("__info", module_name)
    if not info:
        # Info file does not exist in module
        return []
    elif not info.HELP_DATAPACKS:
        # Info file does not contain help data
        return []
    help_contents = info.HELP_DATAPACKS

    # Format the content
    datapacks = []
    for heading in help_contents.keys():
        content = ""
        if "commands" not in heading.lower():
            # Format as regular string
            content += help_contents[heading]
        else:
            # Format as command description
            for command in help_contents[heading]:
                if "name" not in command:
                    # Entry is not a command
                    continue

                content += "- `" + prefix + command["name"]
                if "params" in command:
                    # Entry contains extra parameters
                    for param in command["params"]:
                        content += " -{}".format(param)
                content += "`: "

                if "description" in command:
                    # Entry contains a command description
                    content += command["description"]
                content += "\n"
        datapacks.append((heading, content, False))

    return datapacks
