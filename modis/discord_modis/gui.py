"""Base GUI for Modis."""

import logging

import tkinter as tk
import tkinter.ttk as ttk

import threading
import asyncio

logger = logging.getLogger(__name__)


class Frame(ttk.Frame):
    """The main window frame for Modis."""

    def __init__(self, parent, discord_token, discord_client_id):
        """
        Create a new main window frame.

        Args:
            parent: A tk or ttk object
        """
        super(Frame, self).__init__(parent)

        logger.debug("Initialising frame")

        # Log
        log = Log(self)
        log.grid(column=1, row=0, padx=8, pady=8, sticky="W E N S")

        # Bot control panel
        botcontrol = BotControl(self, discord_token, discord_client_id)
        botcontrol.grid(
            column=0, row=1, columnspan=2, padx=8, pady=8, sticky="W E N")

        # Module tabs
        moduletabs = ModuleTabs(self)
        moduletabs.grid(column=0, row=0, padx=8, pady=8, sticky="W E N S")

        # Status bar
        statusbar = StatusBar(self)
        statusbar.grid(column=0, row=2, columnspan=2, sticky="W E S")

        # Configure stretch ratios
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)


class BotControl(ttk.Labelframe):
    """The control panel for the Modis bot."""

    def __init__(self, parent, discord_token, discord_client_id):
        """
        Create a new control panel and add it to the parent.

        Args:
            parent: A tk or ttk object
        """
        logger.debug("Initialising main control panel")

        super(BotControl, self).__init__(
            parent, padding=8, text="Modis control panel")

        self.discord_thread = None

        # Key name
        self.key_name = tk.StringVar()
        ttk.Label(self, text="API Key Name:").grid(column=0, row=0, padx=4, pady=4, sticky="W E S")
        self.text_key_name = ttk.Entry(self, textvariable=self.key_name)
        self.text_key_name.grid(column=0, row=1, padx=4, pady=4, sticky="W E N S")
        # Key value
        self.key_val = tk.StringVar()
        ttk.Label(self, text="API Key Value:").grid(column=1, row=0, padx=4, pady=4, sticky="W E S")
        self.text_key_value = ttk.Entry(self, textvariable=self.key_val)
        self.text_key_value.grid(column=1, row=1, padx=4, pady=4, sticky="W E N S")
        # Callbacks for text edit
        self.key_name.trace("w", lambda name, index, mode, sv=self.key_name: self.key_changed())
        self.key_val.trace("w", lambda name, index, mode, sv=self.key_val: self.key_changed())
        # Add key button
        self.button_key_add = ttk.Button(
            self, command=lambda: self.key_add(), text="Add API Key")
        self.button_key_add.grid(column=2, row=1, padx=4, pady=4, sticky="W E N S")
        self.button_key_add.state(["disabled"])

        # Stop button
        self.button_stop = ttk.Button(
            self, command=lambda: self.stop(), text="Stop Modis")
        self.button_stop.grid(column=3, row=0, padx=4, pady=4, sticky="W E N S")
        self.button_stop.state(["disabled"])

        # Start button
        self.button_start = ttk.Button(
            self, command=lambda: self.start(discord_token, discord_client_id), text="Start Modis")
        self.button_start.grid(column=3, row=1, padx=4, pady=4, sticky="W E N S")

        # Configure stretch ratios
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)

    def start(self, discord_token, discord_client_id):
        """Start Modis and log it into Discord."""
        self.button_stop.state(['!disabled'])
        self.button_start.state(['disabled'])

        logger.info("----------------STARTING DISCORD MODIS----------------")

        from modis.discord_modis import main

        logger.debug("Creating event loop")
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        self.discord_thread = threading.Thread(
            target=main.start,
            args=[discord_token, discord_client_id, loop])
        logger.debug("Starting event loop")
        self.discord_thread.start()

    def stop(self):
        """Stop Modis and log it out of Discord."""
        self.button_stop.state(['disabled'])
        self.button_start.state(['!disabled'])

        logger.info("Stopping Discord Modis")

        from ._client import client
        asyncio.run_coroutine_threadsafe(client.logout(), client.loop)


    def key_changed(self):
        """Checks if the key name and value fields have been set, and updates the add key button"""
        if self.key_name.get() and self.key_val.get():
            self.button_key_add.state(["!disabled"])
        else:
            self.button_key_add.state(["disabled"])


    def key_add(self):
        """Adds the current API key to the bot's data"""
        from .. import datatools
        data = datatools.get_data()

        if "keys" not in data["discord"]:
            data["discord"]["keys"] = {}

        is_key_new = False
        if not self.key_name.get() in data["discord"]["keys"]:
            is_key_new = True
        elif data["discord"]["keys"][self.key_name.get()] == self.key_val.get():
            logger.info("API key '{}' already has value '{}'".format(self.key_name.get(), self.key_val.get()))
            return

        data["discord"]["keys"][self.key_name.get()] = self.key_val.get()
        datatools.write_data(data)

        key_text = "added" if is_key_new else "updated"
        logger.info("API key '{}' {} with value '{}'".format(self.key_name.get(), key_text, self.key_val.get()))


class ModuleTabs(ttk.Labelframe):
    """The notebook showing the tabs for all the modules."""

    def __init__(self, parent):
        """
        Create a new notebook and add it to the given parent.

        Args:
            parent: A tk or ttk object
        """
        logger.debug("Initialising module tabs")

        super(ModuleTabs, self).__init__(parent, padding=8, text="Module tabs")

        # Module tabs notebook
        self.module_notebook = ttk.Notebook(self)
        self.module_notebook.grid(
            column=0, row=0, padx=4, pady=4, sticky="W E N S")

        # Configure stretch ratios
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # Add initial tab
        self.module_notebook.add(ttk.Frame(self), text="No modules loaded")


class Log(ttk.Labelframe):
    """The text box showing the Python console log."""

    def __init__(self, parent):
        """
        Create a new text box for the console log.

        Args:
            parent: A tk or ttk object
        """
        logger.debug("Initialising log panel")

        super(Log, self).__init__(parent, padding=8, text="Python console log")

        # Log text box
        log = tk.Text(self, wrap="none")
        log.grid(column=0, row=0, padx=4, pady=4, sticky="W E N S")
        log.insert("end", "Welcome to Modis for Discord Beta v0.2.3\n")

        # Vertical Scrollbar
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=log.yview)
        scrollbar.grid(column=1, row=0, sticky="N S")
        log['yscrollcommand'] = scrollbar.set

        # Horizontal Scrollbar
        scrollbar = ttk.Scrollbar(self, orient="horizontal", command=log.xview)
        scrollbar.grid(column=0, row=1, sticky="W E")
        log['xscrollcommand'] = scrollbar.set

        # Rediect Python console output to log text box
        class LogHandler(logging.Handler):
            def __init__(self, text_widget):
                logging.Handler.__init__(self)

                self.text_widget = text_widget

            def flush(self):
                self.text_widget.see("end")

            def emit(self, record):
                msg = self.format(record)
                msg = msg[:9] + msg[29:]
                self.text_widget.insert("end", msg + "\n")
                self.flush()

        discord_logger = logging.getLogger("modis.discord_modis")
        formatter = logging.Formatter(
            "{levelname:8} {name} - {message}", style="{")
        discord_handler = LogHandler(log)
        discord_handler.setFormatter(formatter)
        discord_logger.addHandler(discord_handler)

        # Configure stretch ratios
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)


class StatusBar(ttk.Frame):
    """The status bar at the bottom of the UI."""

    def __init__(self, parent):
        """
        Create a new status bar.

        Args:
            parent: A tk or ttk object
        """
        logger.debug("Initialising status bar")

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
            anchor="center")
        self.statusbar.grid(column=0, row=0, sticky="W E")

        # Configure stretch ratios
        self.columnconfigure(0, weight=1)
