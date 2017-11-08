import os

from modis import helptools


def get_help_datapacks(module_name, server_prefix):
    """
    Get the help datapacks for a module

    Args:
        module_name (str): The module to get help data for
        server_prefix (str): The command prefix for this server

    Returns:
        datapacks (list): The help datapacks for the module
    """

    _dir = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__)))
    module_dir = "{}/../{}".format(_dir, module_name, "_help.json")
    if os.path.isdir(module_dir):
        module_help_path = "{}/{}".format(module_dir, "_help.json")

        if os.path.isfile(module_help_path):
            return helptools.get_help_datapacks(module_help_path, server_prefix)
        else:
            return [("Help", "{} does not have a help.json file".format(module_name), False)]
    else:
        return [("Help", "No module found called {}".format(module_name), False)]


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
        if not module_name.startswith("_"):
            help_command = "`{}help {}`".format(server_prefix, module_name)
            datapacks.append((module_name, help_command, True))

    return datapacks
