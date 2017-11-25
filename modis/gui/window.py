import logging
import asyncio
import tkinter as tk
import tkinter.ttk as ttk

logger = logging.getLogger(__name__)


class RootFrame(ttk.Frame):
    """The main window frame for Modis."""

    def __init__(self, parent):
        """Create the frame.

        Args:
            parent: A tk or ttk object.
        """

        super(RootFrame, self).__init__(parent)

        logger.debug("Initialising root frame")

        # Define window close action
        def on_closing():
            """Called when the window closes"""
            try:
                from modis.common import client
                if client and client.loop:
                    asyncio.run_coroutine_threadsafe(client.logout(), client.loop)
            except RuntimeError:
                pass
            except Exception as e:
                logger.exception(e)

            parent.destroy()
            import sys
            sys.exit(0)
        parent.protocol("WM_DELETE_WINDOW", on_closing)

        # Add elements
        statusbar = StatusBar(self)

        nav = ttk.Notebook(self)
        from modis.gui.tabs import core, api, data, modules
        nav.add(core.Frame(nav), text="Global")
        nav.add(api.Frame(nav), text="API")
        nav.add(data.Frame(nav), text="Data")
        nav.add(modules.Frame(nav), text="Modules")

        # Grid elements
        statusbar.grid(column=0, row=1, sticky="W E S")
        nav.grid(column=0, row=0, sticky="W E N S")

        # Configure stretch ratios
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)


class StatusBar(ttk.Frame):
    """The status bar at the bottom of the UI."""

    def __init__(self, parent):
        """
        Create the status bar.

        Args:
            parent: A tk or ttk object
        """

        logger.debug("Initialising status bar")

        super(StatusBar, self).__init__(parent)

        # Add element - label
        self.status = tk.StringVar()
        self.statusbar = ttk.Label(self, textvariable=self.status, padding=2,
                                   anchor="center")
        self.statusbar.grid(column=0, row=0, sticky="W E")

        # Configure stretch ratios
        self.columnconfigure(0, weight=1)

        # Set default status
        self.set(0)

    def set(self, status):
        """Set the status.

        Args:
            status (int): 0-=offline, 1=starting, 2=online
        """

        text = ""
        colour = "#FFFFFF"
        if status == 0:
            text = "OFFLINE"
            colour = "#FF4444"
        elif status == 1:
            text = "STARTING"
            colour = "#FFAA00"
        elif status == 2:
            text = "ONLINE"
            colour = "#AAFF00"

        self.status.set(text)
        self.statusbar.config(background=colour)
