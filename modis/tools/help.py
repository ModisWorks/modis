import logging

from modis.tools import moduledb

logger = logging.getLogger(__name__)


# def get(module_name):
#     """Get a dict from a __info.py
#
#     Args:
#         module_name (str): The name of the module to get help for.
#
#     Returns:
#         data (OrderedDict): The dict of the help.json
#     """
#
#     info = moduledb.get_import_specific("!info", module_name)
#
#     if not info:
#         return {}
#     if not info.HELP_DATAPACKS:
#         return {}
#     return info.HELP_DATAPACKS


def get_formatted(module_name, prefix="!"):
    """Load help text from a __info.py and format into datapacks.

    Args:
        module_name (str): The name of the module to get help for.
        prefix (str): The prefix to use for commands.

    Returns:
        datapacks (list): The formatted data.
    """

    help_contents = {}
    datapacks = []

    info = moduledb.get_import_specific("__info", module_name)
    if not info:
        pass
    if not info.HELP_DATAPACKS:
        pass
    else:
        help_contents = info.HELP_DATAPACKS

    # Add the content
    for d in help_contents.keys():
        heading = d
        content = ""

        if "commands" in d.lower():
            for c in help_contents[d]:
                if "name" not in c:
                    continue

                content += "- `"
                command = prefix + c["name"]
                content += "{}".format(command)
                if "params" in c:
                    for param in c["params"]:
                        content += " [{}]".format(param)
                content += "`: "
                if "description" in c:
                    content += c["description"]
                content += "\n"
        else:
            content += help_contents[d]

        datapacks.append((heading, content, False))

    return datapacks
