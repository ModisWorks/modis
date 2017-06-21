def console(discord_token, discord_client_id, google_api_key):
    """Starts Modis in console format

    Args:
        discord_token (str): The bot token for your Discord application
        discord_client_id: The bot's client ID
        google_api_key: A Google API key with YouTube API enabled
    """

    import threading
    import asyncio

    # Import bots
    from modis.discord_modis import main as discord_main
    from modis.reddit_modis import main as reddit_main
    from modis.facebook_modis import main as facebook_main

    # Create threads
    loop = asyncio.get_event_loop()
    discord_thread = threading.Thread(target=discord_main.start,  args=[
            discord_token,
            discord_client_id,
            google_api_key,
            loop
    ])
    reddit_thread = threading.Thread(target=reddit_main.start, args=[

    ])
    facebook_thread = threading.Thread(target=facebook_main.start, args=[

    ])

    # Run threads
    discord_thread.start()
    reddit_thread.start()
    facebook_thread.start()


def gui(discord_token, discord_client_id, google_api_key):
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
    main.columnconfigure(0, weight=1)
    main.rowconfigure(0, weight=1)

    # Add tabs
    main.add(discord_gui.Frame(
        main,
        discord_token,
        discord_client_id,
        google_api_key
    ), text="Discord")
    main.add(reddit_gui.Frame(
        main
    ), text="Reddit")
    main.add(facebook_gui.Frame(
        main
    ), text="Facebook")

    # Run the window UI
    root.mainloop()
