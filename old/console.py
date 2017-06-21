def init():
    """Runs the Modis console"""

    import tkinter as tk
    from .console_elements import main_window

    # Setup the root window
    root = tk.Tk()
    root.minsize(width=1400, height=600)
    root.geometry("1400x600")
    root.title("Modis Console")

    # Main frame
    main = main_window.UI(root)
    main.grid()

    # Configure stretch ratios
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    # Run the window UI
    root.mainloop()
