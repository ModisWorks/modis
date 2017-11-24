import logging
import os
import asyncio
import importlib
import threading
import tkinter as tk
import tkinter.ttk as ttk

from modis.tools import helptools

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
                from modis.cache import client
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
        nav.add(TabCore(nav), text="Global")
        nav.add(TabAPI(nav), text="API")
        nav.add(TabData(nav), text="Data")
        nav.add(TabModules(nav), text="Modules")

        # Grid elements
        statusbar.grid(column=0, row=1, sticky="W E S")
        nav.grid(column=0, row=0, sticky="W E N S")

        # Configure stretch ratios
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)


class TabCore(tk.Frame):
    """A tab containing the core controls of the bot"""

    def __init__(self, parent):
        """Create the frame.

        Args:
            parent: A tk or ttk object.
        """

        super(TabCore, self).__init__(parent)

        # Log
        log = self.CoreLog(self)
        log.grid(column=0, row=0, padx=8, pady=8, sticky="W E N S")

        # Bot control panel
        botcontrol = self.CoreControl(self)
        botcontrol.grid(column=0, row=1, padx=8, pady=8, sticky="W E S")

        # Configure stretch ratios
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=0)

    class CoreControl(ttk.Labelframe):
        """The control panel for the Modis bot."""

        def __init__(self, parent):
            """Create the frame.

            Args:
                parent: A tk or ttk object.
            """

            super(TabCore.CoreControl, self).__init__(parent, padding=8, text="Modis control panel")

            logger.debug("Initialising main control panel")

            # Toggle button
            self.state = "off"
            self.button_text = tk.StringVar(value="Start Modis")
            self.button = ttk.Button(self, command=lambda: self.toggle(), textvariable=self.button_text)
            self.button.grid(column=3, row=1, padx=4, pady=4, sticky="W E N S")

            # Configure stretch ratios
            self.columnconfigure(0, weight=1)
            self.columnconfigure(1, weight=2)

        def toggle(self):
            """Toggle Modis on or off."""

            if self.state == 'off':
                self.start()
            elif self.state == 'on':
                self.stop()

        def start(self):
            """Start Modis and log it into Discord."""

            self.button_text.set("Stop Modis")
            self.state = "on"

            # Start Modis
            logger.debug("Starting Modis")
            from modis import main

            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

            thread = threading.Thread(target=main.start, args=[loop])
            thread.start()

        def stop(self):
            """Stop Modis and log out of Discord."""

            self.button_text.set("Start Modis")
            self.state = "off"

            # Stop Modis
            logger.info("Stopping Modis")
            from modis.cache import client
            asyncio.run_coroutine_threadsafe(client.logout(), client.loop)

    class CoreLog(ttk.Labelframe):
        """The text box showing the logging output"""

        def __init__(self, parent):
            """Create the frame.

            Args:
                parent: A tk or ttk object.
            """

            logger.debug("Initialising log panel")

            super(TabCore.CoreLog, self).__init__(parent, padding=8, text="Python console log")

            # Log text box
            log_panel = tk.Text(self, wrap="none")
            log_panel.grid(column=0, row=0, sticky="W E N S")

            # Vertical scrollbar
            scrollbar = ttk.Scrollbar(self, orient="vertical",
                                      command=log_panel.yview)
            scrollbar.grid(column=1, row=0, sticky="N S")
            log_panel['yscrollcommand'] = scrollbar.set

            # Horizontal scrollbar
            scrollbar = ttk.Scrollbar(self, orient="horizontal",
                                      command=log_panel.xview)
            scrollbar.grid(column=0, row=1, sticky="W E")
            log_panel['xscrollcommand'] = scrollbar.set

            # Add log panel as a handler to root logger
            # Get logger
            discord_logger = logging.getLogger("modis")

            # Setup format
            formatter = logging.Formatter("{levelname:8} {name} - {message}",
                                          style="{")

            # Setup handler
            class PanelHandler(logging.Handler):
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
                    msg = msg[:9] + msg[15:]
                    self.text_widget.config(state=tk.NORMAL)
                    self.text_widget.insert("end", msg + "\n")
                    self.text_widget.config(state=tk.DISABLED)
                    self.flush()

            panel_handler = PanelHandler(log_panel)
            panel_handler.setFormatter(formatter)
            discord_logger.addHandler(panel_handler)

            # Configure stretch ratios
            self.columnconfigure(0, weight=1)
            self.rowconfigure(0, weight=1)


class TabAPI(tk.Frame):
    """A tab containing all the controls for API keys and data"""

    def __init__(self, parent):
        """Create the frame.

        Args:
            parent: A tk or ttk object.
        """

        super(TabAPI, self).__init__(parent)


class TabData(tk.Frame):
    """A tab containing controls for the data.json"""

    def __init__(self, parent):
        """Create the frame.

        Args:
            parent: A tk or ttk object.
        """

        super(TabData, self).__init__(parent)

        self.image = tk.PhotoImage(file=__file__[:-13] + "assets/data.png")
        self.label = tk.Label(self, image=self.image)
        self.label.grid()


class TabModules(tk.Frame):
    """A tab containing UI pages for all the modules"""

    def __init__(self, parent):
        """Create the frame.

        Args:
            parent: A tk or ttk object.
        """

        super(TabModules, self).__init__(parent)
        logger.debug("Initialising module tabs")

        # Setup styles
        style = ttk.Style()
        style.configure("Module.TFrame", background="white")

        self.module_buttons = {}
        self.current_button = None

        # Add elements
        self.module_list = ttk.Frame(self, width=150, style="Module.TFrame")
        self.header = tk.Label(self.module_list, text="Modules", bg="white", fg="#484848")
        self.module_selection = ttk.Frame(self.module_list, style="Module.TFrame")
        self.module_ui = ttk.Frame(self)

        # Grid elements
        self.module_list.grid(column=0, row=0, padx=0, pady=0, sticky="W E N S")
        self.header.grid(column=0, row=0, padx=0, pady=0, sticky="W E N")
        self.module_selection.grid(column=0, row=1, padx=0, pady=0, sticky="W E N S")
        self.module_ui.grid(column=1, row=0, padx=0, pady=0, sticky="W E N S")

        # Configure stretch ratios
        self.module_list.columnconfigure(0, weight=1)
        self.module_list.rowconfigure(0, weight=0)
        self.module_list.rowconfigure(1, weight=1)
        self.module_selection.columnconfigure(0, weight=1)
        self.module_ui.columnconfigure(0, weight=1)
        self.module_ui.rowconfigure(0, weight=1)

        self.columnconfigure(0, minsize=150)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        self.scan()

    def add(self, module_name, module_ui):
        """Adds a module to the list.

        Args:
            module_name (str): The name of the module.
            module_ui (import): The function to call to create the module's UI.
        """

        m_button = tk.Label(self.module_selection, text=module_name, bg="white", anchor="w")
        m_button.grid(column=0, row=len(self.module_selection.winfo_children()), padx=0, pady=0, sticky="W E N S")

        self.module_buttons[module_name] = m_button
        m_button.bind("<Button-1>", lambda e: self.select(module_name, module_ui))

    def scan(self):
        database_dir = "C:/Data/GitHub/modis/modis/modules"
        # Iterate through modules
        for module_name in os.listdir(database_dir):
            module_dir = "{}/{}".format(database_dir, module_name)

            if not os.path.isdir(module_dir):
                continue
            if module_name.startswith("_"):
                continue

            files = os.listdir(module_dir)
            if "_ui.py" in files:
                logger.debug("Importing UI for {} module".format(module_name))
                import_name = ".discord_modis.modules.{}.{}".format(module_name, "_ui")
                self.add(module_name, importlib.import_module(import_name, "modis"))
            else:
                logger.debug("No UI for {} module".format(module_name))
                self.add(module_name, None)

    def select(self, module_name, module_ui):
        """Called when a module is selected.

        Args:
            module_name (str): The name of the module
            module_ui (import): The function to call to create the module's UI
        """

        if self.current_button == self.module_buttons[module_name]:
            return

        self.module_buttons[module_name].config(bg="#cacaca")
        if self.current_button is not None:
            self.current_button.config(bg="white")
        self.current_button = self.module_buttons[module_name]

        self.destroy()

        try:
            # Create the UI
            module_ui_frame = self.ModuleFrame(self.module_ui, module_name, module_ui)
            module_ui_frame.grid(column=0, row=0, sticky="W E N S")
        except Exception as e:
            logger.error("Could not load UI for {}".format(module_name))
            logger.exception(e)
            # Create a error UI
            tk.Label(self.module_ui, text="Could not load UI for {}".format(module_name)).grid(
                column=0, row=0, padx=0, pady=0, sticky="W E N S")

    def clear(self):
        """Clears all modules from the list."""

        for child in self.module_selection.winfo_children():
            child.destroy()

        self.destroy()

        tk.Label(self.module_ui, text="Start Modis and select a module").grid(
            column=0, row=0, padx=0, pady=0, sticky="W E N S")

        if self.current_button is not None:
            self.current_button.config(bg="white")

        self.module_buttons = {}
        self.current_button = None

    def destroy(self):
        """Clears everything in the UI."""

        for child in self.module_ui.winfo_children():
            child.destroy()

    class ModuleFrame(ttk.Frame):
        """The base frame for a module's UI."""

        def __init__(self, parent, module_name, module_ui):
            """Create the frame.

            Args:
                parent: A tk or ttk object.
                module_name (str): The name of the module.
                module_ui (import): The _ui.py file to add for the module.
            """

            super(TabModules.ModuleFrame, self).__init__(parent, padding=8)

            # Add elements
            self.help_frame = ttk.LabelFrame(self, padding=8, text="Help")

            # Find the help path
            _dir = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
            help_path = "{}/modules/{}/{}".format(_dir, module_name, "_help.json")
            if os.path.isfile(help_path):
                # Load the text
                helptools.add_help_text(self.help_frame, help_path)
            else:
                # Default message
                tk.Label(self.help_frame, text="No _help.json file found for '{}'".format(module_name)).grid(row=0, column=0, sticky="W E N S")

            # Grid elements
            if module_ui is not None:
                module_ui.ModuleUIFrame(self).grid(row=0, column=0, sticky="W E N S")
                self.help_frame.grid(row=1, column=0, sticky="W E N S")

            # Configure stretch ratios
                self.help_frame.columnconfigure(0, weight=1)
                self.help_frame.rowconfigure(0, weight=1)

            self.columnconfigure(0, weight=1)
            self.rowconfigure(1, weight=1)


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
