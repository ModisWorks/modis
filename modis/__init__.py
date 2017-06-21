def console(token_discord):
    import threading
    import asyncio

    # Import bots
    from modis.discord_modis import main as discord_main
    from modis.reddit_modis import main as reddit_main
    from modis.facebook_modis import main as facebook_main

    # Create threads
    loop = asyncio.get_event_loop()
    discord_thread = threading.Thread(target=discord_main.start, args=[token_discord, loop])
    reddit_thread = threading.Thread(target=reddit_main.start, args=[])
    facebook_thread = threading.Thread(target=facebook_main.start, args=[])

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
    main.add(discord_gui.Frame(main))
    main.add(reddit_gui.Frame(main))
    main.add(facebook_gui.Frame(main))

    # Run the window UI
    root.mainloop()
