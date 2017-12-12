"""
WELCOME TO MODIS

These docstrings will guide you through how Modis' internals work, and get you
started with developing for Modis.

For more help, go to our website at https://infraxion.github.io/modis/ or join
our discord (click "connect" in the Discord embed on the website) where other
developers will be more than happy to help you.

Have fun!
"""

# Update data.json cache
from modis.tools import data
data.get()


def cmd(data_dir=None):
    """Start Modis in command line."""

    # TODO switch to configtools
    # Set the data dir to the one provided
    if data_dir:
        set_dir(data_dir)

    # Setup the logger
    import logging
    from modis.tools import log
    logger = logging.getLogger(__name__)
    log.init_print(logger)
    log.init_file(logger)

    # Import packages
    import asyncio
    from modis import main

    # Start Modis for command line
    logger.info("Starting Modis")
    loop = asyncio.get_event_loop()
    asyncio.set_event_loop(loop)
    main.start(loop)


def gui(data_dir=None):
    """Start Modis with GUI."""

    # TODO switch to configtools
    # Set the data dir to the one provided
    if data_dir:
        set_dir(data_dir)

    # Setup the logger
    import logging
    from modis.tools import log
    logger = logging.getLogger(__name__)
    log.init_print(logger)
    log.init_file(logger)

    # Import packages
    import tkinter as tk
    from modis.gui import window

    # Start Modis for GUI
    logger.info("Starting GUI")

    # Setup the root window
    root = tk.Tk()
    root.minsize(width=800, height=400)
    root.geometry("800x600")
    root.title("Modis Control Panel")
    root.iconbitmap(__file__[:-11] + "assets/modis.ico")

    # Setup the notebook
    main = window.RootFrame(root)
    main.grid(column=0, row=0, padx=0, pady=0, sticky="W E N S")

    # Configure stretch ratios
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    main.columnconfigure(0, weight=1)
    main.rowconfigure(0, weight=1)

    # Run the window UI
    root.mainloop()


def set_dir(data_dir=None):
    """Set the data directory.

    Args:
        data_dir: The new directory to store data in.
    """

    import os

    if not os.path.isdir(data_dir):
        raise NotADirectoryError("Data dir {} does not exist".format(data_dir))
    else:
        from modis.tools import config
        config.WORK_DIR = data_dir
