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


def get_imports(filenames):
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
    for module_name in get_names():
        for file in os.listdir("{}/{}".format(config.MODULES_DIR, module_name)):
            file = file[:-3]
            if file not in filenames:
                # Requested file does not exist in module
                continue
            import_name = ".modules.{}.{}".format(module_name, file)
            imported_file = importlib.import_module(import_name, "modis")
            imports[file].append(imported_file)

    return imports


def get_import_specific(filename, module_name):
    """Get a specific import from a module.

    Args:
        filename (str): The file to import.
        module_name (str) : The module to import from.

    Returns:
        imports (file): The imported file.
    """

    # Import requested files for each module
    if module_name not in os.listdir(config.MODULES_DIR):
        return
    if filename + ".py" not in os.listdir("{}/{}".format(config.MODULES_DIR, module_name)):
        return
    import_name = ".modules.{}.{}".format(module_name, filename)
    return importlib.import_module(import_name, "modis")


# UNUSED
def get_path(filenames):
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
    for module_name in get_names():
        for file in os.listdir("{}/{}".format(config.MODULES_DIR, module_name)):
            if file not in filenames:
                # Requested file does not exist in module
                continue
            file_path = "{}/{}/{}".format(config.MODULES_DIR, module_name, file)
            files[file].append(file_path)

    return files
