"""WELCOME TO MODIS

These docstrings will guide you through how Modis' internals work, and get you started with developing for Modis.

For more help, go to our website at https://modisworks.github.io/ or join our discord (click "connect" in the Discord embed on the website) where other developers will be glad to help you out :)

Have fun!
"""

import logging
from modis.tools import data, config, log

# Update data.json cache
data.pull()

# Setup logging
logger = logging.getLogger(__name__)
log.init_print(logger)
log.init_file(logger)


def cmd() -> None:
    """Starts Modis without the GUI."""

    logger.info("Starting Modis")

    # Setup Modis event loop
    import asyncio
    from modis import main

    loop = asyncio.get_event_loop()
    asyncio.set_event_loop(loop)

    # Start Modis
    main.start(loop)


def gui() -> None:
    """Starts Modis with the GUI."""

    logger.info("Starting Modis console GUI")

    # Start Modis console GUI
    import tkinter as tk
    from modis.gui import window

    # Setup the root window
    root = tk.Tk()
    root.minsize(width=800, height=400)
    root.geometry("800x600")
    root.title("Modis Control Panel")
    try:
        root.iconbitmap("{}/assets/modis.ico".format(__file__[:-11]))
    except tk.TclError:
        logger.warning("Could not resolve asset path")

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
