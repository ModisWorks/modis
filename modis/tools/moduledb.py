"""
This tool handles all the module management functions in Modis, including
scanning the module database and importing module files.
"""

import importlib
import logging
import os

from modis.tools import config

logger = logging.getLogger(__name__)


def get_names():
    """Get a list of the names of all available modules.

    Returns:
        module_names (list): List of strings of module names.
    """

    module_names = []
    for module_folder in os.listdir(config.MODULES_DIR):
        if not os.path.isdir("{}/{}".format(config.MODULES_DIR, module_folder)):
            # Is a file, not a folder
            continue
        if module_folder.startswith("_"):
            # Module is manually deactivated
            continue
        module_names.append(module_folder)

    return module_names


def get_imports(filenames):
    """Get a dictionary with imported Python module files organised by name.

    Args:
        filenames (list): The names to scan.

    Returns:
        imports (dict): The imported files.
    """

    # Setup imports dict
    imports = {}

    # Import requested files for each module
    for module_name in get_names():
        imports[module_name] = {}
        for file in os.listdir("{}/{}".format(config.MODULES_DIR, module_name)):
            file = file[:-3]
            if file not in filenames:
                # Requested file does not exist in module
                continue
            import_name = ".modules.{}.{}".format(module_name, file)
            logger.debug("Importing {} from {}".format(file, module_name))
            try:
                imported_file = importlib.import_module(import_name, "modis")
            except Exception as e:
                logger.error("{} from {} failed to import".format(file, module_name))
                logger.exception(e)
                continue
            imports[module_name][file] = imported_file

    return imports


# TODO Deprecate
def get_import_specific(eh_name, module_name):
    """Get a specific import from a module.

    Args:
        eh_name (str): The file to import.
        module_name (str) : The module to import from.

    Returns:
        imports (file): The imported file.
    """

    if module_name not in os.listdir(config.MODULES_DIR):
        # Module does not exist
        return
    if eh_name + ".py" not in os.listdir("{}/{}".format(config.MODULES_DIR, module_name)):
        # File does not exist
        return
    import_name = ".modules.{}.{}".format(module_name, eh_name)
    return importlib.import_module(import_name, "modis")
