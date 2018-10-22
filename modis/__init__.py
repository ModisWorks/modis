"""WELCOME TO MODIS

These docstrings will guide you through how Modis' internals work, and get you started with developing for Modis.

For more help, go to our website at https://modisworks.github.io/modis/ or join our discord (click "connect" in the Discord embed on the website) where other developers will be glad to help you out :)

Have fun!
"""

from modis.tools import data, config

# Update data.json cache
data.pull()


def cmd(data_filepath=None):
    """Starts Modis in command line.

    Starts Modis barebones in the console, without a graphical interface.

    Args:
        data_filepath (str): The path to the folder containing the data.json file.
    """

    # Set data.json filepath if specified
    if data_filepath:
        _set_dir(data_filepath)

    # Setup logger
    import logging
    from modis.tools import log
    logger = logging.getLogger(__name__)
    log.init_print(logger)
    log.init_file(logger)
    logger.info("Starting Modis")

    # Setup Modis event loop
    import asyncio
    from modis import main

    loop = asyncio.get_event_loop()
    asyncio.set_event_loop(loop)

    # Start Modis
    main.start(loop)


def gui(data_filepath=None):
    """Starts Modis with GUI.

    Starts the Modis graphical interface, which will let you launch the bot, edit the database and download modules in an easy to use launcher program.

    Args:
        data_filepath: The path to the folder containing the data.json file.
    """

    # Set data.json filepath
    if data_filepath:
        _set_dir(data_filepath)

    # Setup the logger
    import logging
    from modis.tools import log
    logger = logging.getLogger(__name__)
    log.init_print(logger)
    log.init_file(logger)
    logger.info("Starting Modis console GUI")

    # Start Modis console GUI
    import tkinter as tk
    from modis.gui import window

    # Setup the root window
    root = tk.Tk()
    root.minsize(width=800, height=400)
    root.geometry("800x600")
    root.title("Modis Control Panel")
    root.iconbitmap("{}/assets/modis.ico".format(config.WORK_DIR))

    # Add elements
    main = window.RootFrame(root)

    # Grid elements
    main.grid(column=0, row=0, padx=0, pady=0, sticky="W E N S")

    # Configure stretch ratios
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    main.columnconfigure(0, weight=1)
    main.rowconfigure(0, weight=1)

    # Run the root window
    root.mainloop()


def _set_dir(data_dir=None):
    """Sets the data directory.

    If the directory `data_dir` exists, sets the database directory to `data_dir`.

    Args:
        data_dir (str): The directory the data.json file should be located in.
    """

    import os

    if not os.path.isdir(data_dir):
        raise NotADirectoryError("The path {} does not exist".format(data_dir))
    else:
        from modis.tools import config
        config.WORK_DIR = data_dir
