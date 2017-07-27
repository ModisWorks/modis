import logging
import sys

logger = logging.getLogger(__name__)
logger.setLevel("DEBUG")

# formatter = logging.Formatter('%(asctime)s %(levelname)s: %(name)s - %(message)s')
formatter = logging.Formatter("{asctime} {levelname:8} {name} - {message}", style="{")
printhandler = logging.StreamHandler(sys.stdout)
printhandler.setFormatter(formatter)
filehandler = logging.FileHandler("modis.log")
filehandler.setFormatter(formatter)

logger.addHandler(printhandler)
logger.addHandler(filehandler)

logger.info("----------------NEW INSTANCE----------------")
logger.info("Loading Modis")


def console(discord_token, discord_client_id, google_api_key):
    """Starts Modis in console format

    Args:
        discord_token (str): The bot token for your Discord application
        discord_client_id: The bot's client ID
        google_api_key: A Google API key with YouTube API enabled
    """

    logger.info("Starting Modis in console")

    import threading
    import asyncio

    logger.debug("Loading packages")
    from modis.discord_modis import main as discord_modis_console
    from modis.reddit_modis import main as reddit_modis_console
    from modis.facebook_modis import main as facebook_modis_console

    # Create threads
    logger.debug("Initiating threads")
    loop = asyncio.get_event_loop()
    discord_thread = threading.Thread(target=discord_modis_console.start, args=[
        discord_token,
        discord_client_id,
        google_api_key,
        loop
    ])
    reddit_thread = threading.Thread(target=reddit_modis_console.start, args=[

    ])
    facebook_thread = threading.Thread(target=facebook_modis_console.start, args=[

    ])

    # Run threads
    logger.debug("Starting threads")
    discord_thread.start()
    reddit_thread.start()
    facebook_thread.start()

    logger.debug("Root startup completed")


def gui(discord_token, discord_client_id, google_api_key):
    """Starts Modis in gui format

        Args:
            discord_token (str): The bot token for your Discord application
            discord_client_id: The bot's client ID
            google_api_key: A Google API key with YouTube API enabled
        """

    logger.info("Starting Modis in GUI")

    import tkinter as tk
    import tkinter.ttk as ttk

    logger.debug("Loading packages")
    from modis.discord_modis import gui as discord_modis_gui
    from modis.reddit_modis import gui as reddit_modis_gui
    from modis.facebook_modis import gui as facebook_modis_gui

    logger.debug("Initialising window")

    # Setup the root window
    root = tk.Tk()
    root.minsize(width=1400, height=600)
    root.geometry("1400x600")
    root.title("Modis Control Panel")

    # Setup the notebook
    notebook = ttk.Notebook(root)
    notebook.grid(
        column=0,
        row=0,
        padx=0,
        pady=0,
        sticky="W E N S"
    )

    # Configure stretch ratios
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    notebook.columnconfigure(0, weight=1)
    notebook.rowconfigure(0, weight=1)

    # Add tabs
    logger.debug("Adding packages to window")
    notebook.add(discord_modis_gui.Frame(
        notebook,
        discord_token,
        discord_client_id,
        google_api_key
    ), text="Discord")
    notebook.add(reddit_modis_gui.Frame(
        notebook
    ), text="Reddit")
    notebook.add(facebook_modis_gui.Frame(
        notebook
    ), text="Facebook")

    logger.debug("GUI initialised")

    # Run the window UI
    root.mainloop()
