def console(token_discord):
    import threading
    import asyncio

    # Import bots
    from modis.discord_modis import main as discord_main
    from modis.reddit_modis import main as reddit_main
    from modis.facebook_modis import main as facebook_main

    # Create threads
    loop = asyncio.get_event_loop()
    discord_thread = threading.Thread(target=lambda: discord_main.start(token_discord, loop), args=[])
    reddit_thread = threading.Thread(target=lambda: reddit_main.start(), args=[])
    facebook_thread = threading.Thread(target=lambda: facebook_main.start(), args=[])

    # Run threads
    discord_thread.start()
    reddit_thread.start()
    facebook_thread.start()


def gui():
    import tkinter as tk
    import tkinter.ttk as ttk

    # Import bots
    from modis.discord_modis import gui as discord_gui
    from modis.reddit_modis import gui as reddit_gui
    from modis.facebook_modis import gui as facebook_gui

    # Setup the root window
    root = tk.Tk()
    root.minsize(width=1400, height=600)
    root.geometry("1400x600")
    root.title("Modis Control Panel")

    # Setup the notebook
    main = ttk.Notebook(root)
    main.grid(
        column=0,
        row=0,
        padx=4,
        pady=4,
        sticky="W E N S"
    )

    # Configure stretch ratios
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    # Add tabs
    main.add(discord_gui.Frame())
    main.add(reddit_gui.Frame())
    main.add(facebook_gui.Frame())

    # Run the window UI
    root.mainloop()


# DEPRECATED
def run(apikeys, client_id="", game="", prefix="!"):
    """Runs Modis

    Args:
        apikeys (dict): The API keys required to run Modis and its modules
        client_id (str): The client id of the bot Modis will run on; used to make the invite link
        game (str): The game Modis will be playing; defaults to ""
        prefix (str): The prefix to use for Modis commands; defaults to '!'
    """

    # Import global variable bank
    from . import share

    # Register variables globally
    share.apikeys = apikeys
    share.client_id = client_id
    share.game = game
    share.prefix = prefix

    # Start console
    from . import main
    main.init()


def run_with_console(apikeys, client_id="", game="", prefix="!"):
    """Runs Modis with console ui

    Args:
        apikeys (dict): The API keys required to run Modis and its modules
        client_id (str): The client id of the bot Modis will run on; used to make the invite link
        game (str): The game Modis will be playing; defaults to ""
        prefix (str): The prefix to use for Modis commands; defaults to '!'
    """

    # Import global variable bank
    from . import share

    # Register variables globally
    share.apikeys = apikeys
    share.client_id = client_id
    share.game = game
    share.prefix = prefix

    # Start console
    from . import console
    console.init()
