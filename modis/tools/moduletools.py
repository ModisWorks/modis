import logging
import importlib
import os

from modis import common

logger = logging.getLogger(__name__)


def get_modules():
    """Get a list of the names of all available modules.

    Returns:
        module_names (list): List of strings of module names.
    """

    logger.debug("Retrieving list of modules")

    module_names = []

    for module_folder in os.listdir(common.MODULES_DIR):
        if not os.path.isdir("{}/{}".format(common.MODULES_DIR, module_folder)):
            # Is a file, not a folder
            continue
        if module_folder.startswith("_"):
            # Module is manually deactivated
            continue

        module_names.append(module_folder)

    return module_names


def get_files(filenames):
    """Get a dictionary with module files organised by file type.

    Args:
        filenames (list): The file types to import.

    Returns:
        imports (dict): The imported files.
    """

    # Setup imports dict
    imports = {}
    for filename in filenames:
        imports[filename] = []

    # Import requested files for each module
    for module_name in get_modules():
        for file in os.listdir("{}/{}".format(common.MODULES_DIR, module_name)):
            file = file[:-3]
            if file not in filenames:
                # Requested file does not exist in module
                continue
            import_name = ".modules.{}.{}".format(module_name, file)
            imported_file = importlib.import_module(import_name, "modis")
            imports[file].append(imported_file)

    return imports
