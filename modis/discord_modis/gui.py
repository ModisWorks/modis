"""Base GUI for Modis."""

import asyncio
import logging
import os
import threading
import tkinter as tk
import tkinter.ttk as ttk

from modis import datatools, helptools

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

        # Status bar
        statusbar = StatusBar(self)
        statusbar.grid(column=0, row=1, sticky="W E S")

        # Create the main control panel
        nav = ttk.Notebook(self)
        module_frame = ModuleFrame(nav)
        nav.add(GlobalFrame(nav, discord_token, discord_client_id, module_frame, statusbar), text="Global")
        nav.add(module_frame, text="Modules")
        nav.grid(column=0, row=0, sticky="W E N S")

        def on_closing():
            """Called when the window closes"""
            try:
                from ._client import client
                if client.loop:
                    asyncio.run_coroutine_threadsafe(client.logout(), client.loop)
            except RuntimeError:
                pass
            except Exception as e:
                logger.exception(e)

            parent.destroy()
            import sys
            sys.exit(0)

        parent.protocol("WM_DELETE_WINDOW", on_closing)

        # Configure stretch ratios
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # Update with version data
        datatools.log_compare_version(logger)


class GlobalFrame(tk.Frame):
    """The frame that has all global elements for the bot"""

    def __init__(self, parent, discord_token, discord_client_id, module_frame, status_bar):
        super(GlobalFrame, self).__init__(parent)

        # Log
        log = Log(self)
        log.grid(column=0, row=0, padx=8, pady=8, sticky="W E N S")

        # Bot control panel
        botcontrol = BotControl(self, discord_token, discord_client_id, module_frame, status_bar)
        botcontrol.grid(
            column=0, row=1, padx=8, pady=8, sticky="W E S")

        # Configure stretch ratios
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=0)


class ModuleFrame(tk.Frame):
    """The frame that has all global elements for the bot"""

    def __init__(self, parent):
        """
        Create a new module frame and add it to the given parent.

        Args:
            parent: A tk or ttk object
        """

        super(ModuleFrame, self).__init__(parent)
        logger.debug("Initialising module tabs")

        # Setup styles
        style = ttk.Style()
        style.configure("Module.TFrame", background="white")

        self.module_buttons = {}
        self.current_button = None

        # Module view
        self.module_list = ttk.Frame(self, width=150, style="Module.TFrame")
        self.module_list.grid(column=0, row=0, padx=0, pady=0, sticky="W E N S")
        self.module_list.columnconfigure(0, weight=1)
        self.module_list.rowconfigure(0, weight=0)
        self.module_list.rowconfigure(1, weight=1)
        # Header
        header = tk.Label(self.module_list, text="Modules", bg="white", fg="#484848")
        header.grid(column=0, row=0, padx=0, pady=0, sticky="W E N")
        # Module selection list
        self.module_selection = ttk.Frame(self.module_list, style="Module.TFrame")
        self.module_selection.grid(column=0, row=1, padx=0, pady=0, sticky="W E N S")
        self.module_selection.columnconfigure(0, weight=1)
        # Module UI view
        self.module_ui = ttk.Frame(self)
        self.module_ui.grid(column=1, row=0, padx=0, pady=0, sticky="W E N S")
        self.module_ui.columnconfigure(0, weight=1)
        self.module_ui.rowconfigure(0, weight=1)

        self.clear_modules()

        # Configure stretch ratios
        self.columnconfigure(0, minsize=150)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

    def clear_modules(self):
        """Clears all modules from the list"""
        for child in self.module_selection.winfo_children():
            child.destroy()

        self.clear_ui()

        tk.Label(self.module_ui, text="Start Modis and select a module").grid(
            column=0, row=0, padx=0, pady=0, sticky="W E N S")

        if self.current_button is not None:
            self.current_button.config(bg="white")

        self.module_buttons = {}
        self.current_button = None

    def clear_ui(self):
        """Clears everything in the UI"""
        for child in self.module_ui.winfo_children():
            child.destroy()

    def add_module(self, module_name, module_ui):
        """
        Adds a module to the list

        Args:
            module_name (str): The name of the module
            module_ui: The function to call to create the module's UI
        """
        m_button = tk.Label(self.module_selection, text=module_name, bg="white", anchor="w")
        m_button.grid(column=0, row=len(self.module_selection.winfo_children()), padx=0, pady=0, sticky="W E N S")

        self.module_buttons[module_name] = m_button
        m_button.bind("<Button-1>", lambda e: self.module_selected(module_name, module_ui))

    def module_selected(self, module_name, module_ui):
        """
        Called when a module is selected

        Args:
            module_name (str): The name of the module
            module_ui: The function to call to create the module's UI
        """
        if self.current_button == self.module_buttons[module_name]:
            return

        self.module_buttons[module_name].config(bg="#cacaca")
        if self.current_button is not None:
            self.current_button.config(bg="white")
        self.current_button = self.module_buttons[module_name]

        self.clear_ui()

        try:
            # Create the UI
            module_ui_frame = ModuleUIBaseFrame(self.module_ui, module_name, module_ui)
            module_ui_frame.grid(column=0, row=0, sticky="W E N S")
        except Exception as e:
            logger.error("Could not load UI for {}".format(module_name))
            logger.exception(e)
            # Create a error UI
            tk.Label(self.module_ui, text="Could not load UI for {}".format(module_name)).grid(
                column=0, row=0, padx=0, pady=0, sticky="W E N S")


class ModuleUIBaseFrame(ttk.Frame):
    """A base frame for a module's UI"""

    def __init__(self, parent, module_name, module_ui):
        """
        Create a new base for a module UI

        Args:
            parent: A tk or ttk object
            module_name (str): The name of the module
            module_ui: The _ui.py file to add for the module
        """

        super(ModuleUIBaseFrame, self).__init__(parent, padding=8)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        if module_ui is not None:
            # Module UI frame
            module_ui.ModuleUIFrame(self).grid(row=0, column=0, sticky="W E N S")
        else:
            logger.debug("No _ui.py found for '{}'".format(module_name))

        # Help frame
        help_frame = ttk.LabelFrame(self, padding=8, text="Help")
        help_frame.grid(row=1, column=0, sticky="W E N S")
        help_frame.columnconfigure(0, weight=1)
        help_frame.rowconfigure(0, weight=1)
        # Find the help path
        _dir = os.path.realpath(
            os.path.join(os.getcwd(), os.path.dirname(__file__)))
        help_path = "{}/modules/{}/{}".format(_dir, module_name, "_help.json")
        if os.path.isfile(help_path):
            # Load the text
            helptools.add_help_text(help_frame, help_path)
        else:
            # Default message
            tk.Label(help_frame, text="No _help.json file found for '{}'".format(module_name)).grid(row=0, column=0,
                                                                                                    sticky="W E N S")


class BotControl(ttk.Labelframe):
    """The control panel for the Modis bot."""

    def __init__(self, parent, discord_token, discord_client_id, module_frame, status_bar):
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

        # Module frame
        self.module_frame = module_frame
        # Status bar
        self.status_bar = status_bar

        # Toggle button
        self.state = "off"
        self.button_toggle_text = tk.StringVar(value="Start Modis")
        self.button_toggle = ttk.Button(
            self, command=lambda: self.toggle(discord_token, discord_client_id), textvariable=self.button_toggle_text)
        self.button_toggle.grid(column=3, row=1, padx=4, pady=4, sticky="W E N S")

        # Configure stretch ratios
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)

    def toggle(self, discord_token, discord_client_id):
        """Toggles Modis on or off"""
        if self.state == 'off':
            self.start(discord_token, discord_client_id)
        elif self.state == 'on':
            self.stop()

    def start(self, discord_token, discord_client_id):
        """Start Modis and log it into Discord."""
        self.button_toggle_text.set("Stop Modis")
        self.state = "on"

        self.status_bar.set_status(1)

        logger.info("----------------STARTING DISCORD MODIS----------------")

        # Clear the module list
        self.module_frame.clear_modules()

        # Start Modis
        from modis.discord_modis import main
        logger.debug("Creating event loop")
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        self.discord_thread = threading.Thread(
            target=main.start,
            args=[discord_token, discord_client_id, loop, self.module_frame.add_module, self.on_ready])
        logger.debug("Starting event loop")
        self.discord_thread.start()

    async def on_ready(self):
        """Called when the client is ready"""
        self.status_bar.set_status(2)

    def stop(self):
        """Stop Modis and log it out of Discord."""
        self.button_toggle_text.set("Start Modis")
        self.state = "off"

        logger.info("Stopping Discord Modis")

        from ._client import client
        asyncio.run_coroutine_threadsafe(client.logout(), client.loop)
        self.status_bar.set_status(0)

    def key_changed(self):
        """Checks if the key name and value fields have been set, and updates the add key button"""
        if self.key_name.get() and self.key_val.get():
            self.button_key_add.state(["!disabled"])
        else:
            self.button_key_add.state(["disabled"])

    def key_add(self):
        """Adds the current API key to the bot's data"""
        from .main import add_api_key
        add_api_key(self.key_name.get(), self.key_val.get())

        # Clear the text fields
        self.key_name.set("")
        self.key_val.set("")


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
        log.grid(column=0, row=0, sticky="W E N S")
        log.insert("end", "Welcome to Modis for Discord v{}\n".format(datatools.version))

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
                self.text_widget.config(state=tk.DISABLED)

            def flush(self):
                try:
                    self.text_widget.see("end")
                except:
                    pass

            def emit(self, record):
                msg = self.format(record)
                msg = msg[:9] + msg[29:]
                self.text_widget.config(state=tk.NORMAL)
                self.text_widget.insert("end", msg + "\n")
                self.text_widget.config(state=tk.DISABLED)
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

        self.status = tk.StringVar()
        # Status bar
        self.statusbar = ttk.Label(self, textvariable=self.status, padding=2, anchor="center")
        self.statusbar.grid(column=0, row=0, sticky="W E")

        # Configure stretch ratios
        self.columnconfigure(0, weight=1)

        # Set default status
        self.set_status(False)

    def set_status(self, status):
        """
        Updates the status text

        Args:
            status (int): The offline/starting/online status of Modis
                0: offline, 1: starting, 2: online
        """

        text = ""
        colour = "#FFFFFF"
        if status == 0:
            text = "OFFLINE"
            colour = "#EF9A9A"
        elif status == 1:
            text = "STARTING"
            colour = "#FFE082"
        elif status == 2:
            text = "ONLINE"
            colour = "#A5D6A7"

        self.status.set(text)
        self.statusbar.config(background=colour)
