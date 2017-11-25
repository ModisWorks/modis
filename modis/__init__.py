"""
WELCOME TO MODIS

These docstrings will guide you through how Modis' internals work, and get you
started with developing for Modis.

For more help, go to our website at https://infraxion.github.io/modis/ or join
our discord (click "connect" in the Discord embed on the website) where other
developers will be more than happy to help you.

Have fun!
"""


def cmd():
    """Start Modis in command line."""

    logger = log_init()
    logger.info("Initialising Modis for command line")

    logger.debug("Importing packages")
    import asyncio
    from modis import main
    from modis.tools import versiontools

    logger.info(versiontools.get_str())

    logger.info("Starting Modis")
    loop = asyncio.get_event_loop()
    asyncio.set_event_loop(loop)
    main.start(loop)


def gui():
    """Start Modis with GUI."""

    logger = log_init()
    logger.info("Initialising Modis for GUI")

    logger.debug("Importing packages")
    import os
    import tkinter as tk
    from modis.gui import window
    from modis.tools import versiontools

    logger.info(versiontools.get_str())

    logger.info("Starting GUI")

    # Setup the root window
    root = tk.Tk()
    root.minsize(width=800, height=400)
    root.geometry("800x600")
    root.title("Modis Control Panel")
    file_dir = os.path.dirname(os.path.realpath(__file__))
    root.iconbitmap(r"{}/assets/modis.ico".format(file_dir))

    # Setup the notebook
    discord = window.RootFrame(root)
    discord.grid(column=0, row=0, padx=0, pady=0, sticky="W E N S")

    # Configure stretch ratios
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    discord.columnconfigure(0, weight=1)
    discord.rowconfigure(0, weight=1)

    # Run the window UI
    root.mainloop()


def log_init():
    """Initialises the root logger.

    Returns:
        logger (logging.logger): The root logger.
    """

    import os
    import logging
    import sys
    import time

    from modis.tools import datatools

    file_dir = os.path.dirname(os.path.realpath(__file__))

    # Create logging directory
    logs_dir = "{}/../logs/".format(file_dir)
    if not os.path.isdir(logs_dir):
        os.mkdir(logs_dir)

    # Creater logger
    logger = logging.getLogger(__name__)

    # Set log level
    datatools.get()
    if "log_level" in datatools.data:
        logger.setLevel(datatools.data["log_level"])
    else:
        datatools.data["log_level"] = "INFO"
        datatools.write()
        logger.setLevel("INFO")

    # Setup logging format
    formatter = logging.Formatter("{asctime} {levelname:8} {name} - {message}",
                                  style="{")

    # Setup logging handlers
    printhandler = logging.StreamHandler(sys.stdout)
    printhandler.setFormatter(formatter)
    filehandler = logging.FileHandler("{}/{}.log".format(logs_dir, time.time()))
    filehandler.setFormatter(formatter)

    logger.addHandler(printhandler)
    logger.addHandler(filehandler)

    # Initial logging messages
    logger.info("----------------NEW INSTANCE----------------")
    logger.info("Loading Modis")

    return logger
