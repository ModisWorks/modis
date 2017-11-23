import logging
import os
import sys
import time

from modis import datatools

file_dir = os.path.dirname(os.path.realpath(__file__))
logs_dir = "{}/../logs/".format(file_dir)
if not os.path.isdir(logs_dir):
    os.mkdir(logs_dir)

logger = logging.getLogger(__name__)
logger.setLevel("INFO")
if datatools.has_data():
    data = datatools.get_data()
    if "log_level" in data:
        logger.setLevel(data["log_level"])

formatter = logging.Formatter("{asctime} {levelname:8} {name} - {message}", style="{")

printhandler = logging.StreamHandler(sys.stdout)
printhandler.setFormatter(formatter)
filehandler = logging.FileHandler("{}/{}.log".format(logs_dir, time.time()))
filehandler.setFormatter(formatter)

logger.addHandler(printhandler)
logger.addHandler(filehandler)

logger.info("----------------NEW INSTANCE----------------")
logger.info("Loading Modis")

datatools.log_data()


def cmd():
    """Start Modis in command line format."""

    logger.info("Starting Modis in console")

    state, response = datatools.get_compare_version()
    logger.info(response)

    logger.debug("Loading packages")
    from modis import main

    logger.debug("Initiating threads")
    import asyncio
    loop = asyncio.get_event_loop()
    main.start(loop)

    logger.debug("Root startup completed")


def gui(discord_token, discord_client_id):
    """
    Start Modis in gui format.

    Args:
        discord_token (str): The bot token for your Discord application
        discord_client_id: The bot's client ID
    """

    logger.info("Starting Modis in GUI")

    import tkinter as tk

    logger.debug("Loading packages")
    from modis import gui

    logger.debug("Initialising window")

    # Setup the root window
    root = tk.Tk()
    root.minsize(width=800, height=400)
    root.geometry("800x600")
    root.title("Modis Control Panel")
    # Icon
    root.iconbitmap(r"{}/assets/modis.ico".format(file_dir))

    # Setup the notebook
    discord = gui.Frame(root)
    discord.grid(column=0, row=0, padx=0, pady=0, sticky="W E N S")
    # Configure stretch ratios
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    discord.columnconfigure(0, weight=1)
    discord.rowconfigure(0, weight=1)

    logger.debug("GUI initialised")

    # Run the window UI
    root.mainloop()
