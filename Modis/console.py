def init():
    """Runs the Modis console"""

    import tkinter as tk
    import console_elements.main_window as mwgen

    # Setup the root window
    root = tk.Tk()
    root.minsize(width=1280, height=720)
    root.geometry("1280x720")
    root.title("Modis Console")

    # Main frame
    main_window = mwgen.UI(root)
    main_window.grid()

    # Configure stretch ratios
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    # Run the window UI
    root.mainloop()
