import tkinter as tk
import tkinter.ttk as ttk

import threading
import asyncio


class Frame(ttk.Frame):
    def __init__(self, parent, discord_token, discord_client_id, google_api_key):
        """The main window frame for Modis

        Args:
            parent: A tk or ttk object
        """

        super(Frame, self).__init__(parent)

        # Bot control panel
        botcontrol = BotControl(self, discord_token, discord_client_id, google_api_key)
        botcontrol.grid(
            column=0,
            row=1,
            columnspan=2,
            padx=8,
            pady=8,
            sticky="W E N"
        )

        # Module tabs
        moduletabs = ModuleTabs(self)
        moduletabs.grid(
            column=0,
            row=0,
            padx=8,
            pady=8,
            sticky="W E N S"
        )

        # Log
        log = Log(self)
        log.grid(
            column=1,
            row=0,
            padx=8,
            pady=8,
            sticky="W E N S"
        )

        # Status bar
        statusbar = StatusBar(self)
        statusbar.grid(
            column=0,
            row=2,
            columnspan=2,
            sticky="W E S"
        )

        # Configure stretch ratios
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)


class BotControl(ttk.Labelframe):
    def __init__(self, parent, discord_token, discord_client_id, google_api_key):
        """Modis control panel

        Args:
            parent: A tk or ttk object
        """

        super(BotControl, self).__init__(
            parent,
            padding=8,
            text="Modis control panel")

        self.discord_thread = None

        # Stop button
        self.button_stop = ttk.Button(
            self,
            command=lambda: self.stop(),
            text="Stop Modis"
        )
        self.button_stop.grid(
            column=0,
            row=0,
            padx=4,
            pady=4,
            sticky="E S"
        )
        self.button_stop.state(["disabled"])

        # Start button
        self.button_start = ttk.Button(
            self,
            command=lambda: self.start(discord_token, discord_client_id, google_api_key),
            text="Start Modis"
        )
        self.button_start.grid(
            column=0,
            row=1,
            padx=4,
            pady=4,
            sticky="E S"
        )

        # Configure stretch ratios
        self.columnconfigure(0, weight=1)

    def start(self, discord_token, discord_client_id, google_api_key):
        from modis.discord_modis import main as discord_main

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        self.discord_thread = threading.Thread(target=discord_main.start, args=[
            discord_token,
            discord_client_id,
            google_api_key,
            loop
        ])
        self.discord_thread.start()

        self.button_stop.state(['!disabled'])
        self.button_start.state(['disabled'])

    def stop(self):
        from ._client import client
        asyncio.run_coroutine_threadsafe(client.logout(), client.loop)

        self.button_stop.state(['disabled'])
        self.button_start.state(['!disabled'])


class ModuleTabs(ttk.Labelframe):
    def __init__(self, parent):
        """The notebook showing the tabs for all the modules

        Args:
            parent: A tk or ttk object
        """

        super(ModuleTabs, self).__init__(
            parent,
            padding=8,
            text="Module tabs"
        )

        # Module tabs notebook
        self.module_notebook = ttk.Notebook(self)
        self.module_notebook.grid(
            column=0,
            row=0,
            padx=4,
            pady=4,
            sticky="W E N S"
        )

        # Configure stretch ratios
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # Add initial tab
        self.module_notebook.add(ttk.Frame(self), text="No modules loaded")


class Log(ttk.Labelframe):
    def __init__(self, parent):
        """The text box showing Python console log

        Args:
            parent: A tk or ttk object
        """

        super(Log, self).__init__(
            parent,
            padding=8,
            text="Python console log")

        # Log text box
        log = tk.Text(self)
        log.grid(
            column=0,
            row=0,
            padx=4,
            pady=4,
            sticky="W E N S"
        )
        log.insert("end", "Welcome to Modis for Discord Beta v0.2.3\n")

        # Vertical Scrollbar
        scrollbar = ttk.Scrollbar(
            self,
            orient="vertical",
            command=log.yview
        )
        scrollbar.grid(
            column=1,
            row=0,
            sticky="N S")
        log['yscrollcommand'] = scrollbar.set

        # Horizontal Scrollbar
        scrollbar = ttk.Scrollbar(
            self,
            orient="horizontal",
            command=log.xview
        )
        scrollbar.grid(
            column=0,
            row=1,
            sticky="W E")
        log['xscrollcommand'] = scrollbar.set

        # Rediect Python console output to log text box
        import sys

        class StdoutRedirector:
            def __init__(self, text_widget):
                self.text_widget = text_widget

            def write(self, string):
                self.text_widget.insert("end", string)
                self.text_widget.see("end")

            def flush(self):
                pass

            def isatty(self):
                return True

        sys.stdout = StdoutRedirector(log)
        sys.stderr = StdoutRedirector(log)

        # Configure stretch ratios
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)


class StatusBar(ttk.Frame):
    def __init__(self, parent):
        """The statusbar at the bottom

        Args:
            parent: A tk or ttk object
        """

        super(StatusBar, self).__init__(parent)

        # Status bar
        self.statusbar = ttk.Label(
            self,
            # textvariable=self.status,
            text="OFFLINE",
            padding=2,
            # borderwidth=1,
            # relief="sunken",
            background="#FFBBBB",
            anchor="center"
        )
        self.statusbar.grid(
            column=0,
            row=0,
            sticky="W E"
        )

        # Configure stretch ratios
        self.columnconfigure(0, weight=1)
