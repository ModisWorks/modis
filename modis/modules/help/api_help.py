import os

from modis.tools import help


def get_help_datapacks(module_name, server_prefix):
    """
    Get the help datapacks for a module

    Args:
        module_name (str): The module to get help data for
        server_prefix (str): The command prefix for this server

    Returns:
        datapacks (list): The help datapacks for the module
    """

    datapacks = help.get_formatted(module_name, server_prefix)

    if datapacks:
        return datapacks
    else:
        return [("Help", module_name + "does not have any help data.")]


def get_help_commands(server_prefix):
    """
    Get the help commands for all modules

    Args:
        server_prefix: The server command prefix

    Returns:
        datapacks (list): A list of datapacks for the help commands for all the modules
    """

    datapacks = []

    _dir = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__)))
    for module_name in os.listdir("{}/../".format(_dir)):
        if not module_name.startswith("_") and not module_name.startswith("!"):
            help_command = "`{}help {}`".format(server_prefix, module_name)
            datapacks.append((module_name, help_command, True))

    return datapacks
