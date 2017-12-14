import asyncio
import logging
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

        # Define window close action
        def on_closing():
            try:
                from modis import main
                if main.client and main.client.loop:
                    asyncio.run_coroutine_threadsafe(main.client.logout(), main.client.loop)
            except RuntimeError:
                pass
            except Exception as e:
                logger.exception(e)

            parent.destroy()
            import sys
            sys.exit(0)
        parent.protocol("WM_DELETE_WINDOW", on_closing)

        # Configure styles
        s = ttk.Style()
        s.configure(
            "modis1.TNotebook",
            tabmargins=[0, 0, -1, 0],
            tabposition="wn"
        )
        s.configure(
            "modis1.TNotebook.Tab",
            padding=8,
            width=10
        )
        s.map(
            "modis1.TNotebook.Tab",
            expand=[
                ("selected", [0, 0, 1, 0]),
                ("active", [0, 0, 1, 0])
            ]
        )

        # Add elements
        statusbar = StatusBar(self)

        nav = ttk.Notebook(self, style="modis1.TNotebook")
        from modis.gui.tabs import core, config, modules
        nav.add(core.Frame(nav), text="Global")
        nav.add(config.Frame(nav), text="Config")
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
        """reate the status bar.

        Args:
            parent: A tk or ttk object.
        """

        super(StatusBar, self).__init__(parent)

        # Add elements
        self.status = tk.StringVar()
        self.statusbar = ttk.Label(self, textvariable=self.status, padding=2, anchor="center")
        statuslog = logging.getLogger("globalstatus")
        statuslog.setLevel("INFO")
        statushandler = self.StatusLogHandler(self.statusbar, self.status)
        statuslog.addHandler(statushandler)

        # Grid elements
        self.statusbar.grid(column=0, row=0, sticky="W E")

        # Configure stretch ratios
        self.columnconfigure(0, weight=1)

        # Set default status
        statuslog.info("0")

    class StatusLogHandler(logging.Handler):
        def __init__(self, statusbar, stringvar):
            """Update the global status via a log handler

            Args:
                statusbar (ttk.Label): The statusbar to manage.
                stringvar (tk.StringVar): The status text variable.
            """

            logging.Handler.__init__(self)

            self.statusbar = statusbar
            self.stringvar = stringvar
            self.text = ""
            self.colour = "#FFFFFF"

        def emit(self, record):
            record = self.format(record)
            if record == "0":
                self.text = "OFFLINE"
                self.colour = "#FFAA00"
            elif record == "1":
                self.text = "STARTING"
                self.colour = "#00AAFF"
            elif record == "2":
                self.text = "ONLINE"
                self.colour = "#AAFF00"
            elif record == "3":
                self.text = "ERROR"
                self.colour = "#FF00AA"

            self.stringvar.set(self.text)
            self.statusbar.config(background=self.colour)
