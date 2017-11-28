import json
import logging
from collections import OrderedDict

from modis.tools import config

logger = logging.getLogger(__name__)


def get(module_name):
    """Get a dict from a _help.json

    Args:
        module_name (str): The name of the module to get help for.

    Returns:
        data (OrderedDict): The dict of the help.json
    """

    try:
        with open("{}/{}/_help.json".format(config.MODULES_DIR, module_name), 'r') as file:
            return json.load(file, object_pairs_hook=OrderedDict)
    except FileNotFoundError:
        logger.warning("No help data for " + module_name)
        return {}
    except Exception as e:
        logger.error("Could not load file for " + module_name)
        logger.exception(e)
        return {}


def get_formatted(module_name, prefix="!"):
    """Load help text from a _help.json and format into datapacks.

    Args:
        module_name (str): The name of the module to get help for.
        prefix (str): The prefix to use for commands.

    Returns:
        datapacks (list): The formatted data.
    """

    help_contents = get(module_name)

    datapacks = []

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
