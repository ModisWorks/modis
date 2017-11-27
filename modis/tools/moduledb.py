import importlib
import logging
import os

from modis.tools import config

logger = logging.getLogger(__name__)


def get_modules():
    """Get a list of the names of all available modules.

    Returns:
        module_names (list): List of strings of module names.
    """

    logger.debug("Retrieving list of modules")

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


def get_py(filenames):
    """Get a dictionary with imported Python module files organised by name.

    Args:
        filenames (list): The names to scan.

    Returns:
        imports (dict): The imported files.
    """

    # Setup imports dict
    imports = {}
    for filename in filenames:
        imports[filename] = []

    # Import requested files for each module
    for module_name in get_modules():
        for file in os.listdir("{}/{}".format(config.MODULES_DIR, module_name)):
            file = file[:-3]
            if file not in filenames:
                # Requested file does not exist in module
                continue
            import_name = ".modules.{}.{}".format(module_name, file)
            imported_file = importlib.import_module(import_name, "modis")
            imports[file].append(imported_file)

    return imports


# TODO implement getting filepaths I'm too tired to do it atm
def get_file(filenames):
    """Get a dictionary with file paths organised by file name.

    Args:
        filenames (list): The file names to scan.

    Returns:
        files (dict): The file paths.
    """

    # Setup files dict
    files = {}
    for filename in filenames:
        files[filename] = []

    # Get paths for each file
    for module_name in get_modules():
        for file in os.listdir("{}/{}".format(config.MODULES_DIR, module_name)):
            file = file[:-3]
            if file not in filenames:
                # Requested file does not exist in module
                continue
            import_name = ".modules.{}.{}".format(module_name, file)
            imported_file = importlib.import_module(import_name, "modis")
            files[file].append(imported_file)

    return files
