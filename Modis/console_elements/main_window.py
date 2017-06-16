import tkinter as tk
import tkinter.ttk as ttk

from ..tools import ui_window

pipe_moduletabs = None
pipe_statusbar = None


class UI(ttk.Frame):
    def __init__(self, parent):
        """The main window frame for Modis

        Args:
            parent: A tk or ttk object
        """

        super(UI, self).__init__(parent)

        # Bot control panel
        botcontrol = BotControl(parent)
        botcontrol.grid(
            column=0,
            row=1,
            columnspan=2,
            padx=8,
            pady=8,
            sticky="W E N"
        )

        # Module tabs
        moduletabs = ModuleTabs(parent)
        moduletabs.grid(
            column=0,
            row=0,
            padx=8,
            pady=8,
            sticky="W E N S"
        )

        # Log
        log = Log(parent)
        log.grid(
            column=1,
            row=0,
            padx=8,
            pady=8,
            sticky="W E N S"
        )

        # Status bar
        statusbar = StatusBar(parent)
        statusbar.grid(
            column=0,
            row=2,
            columnspan=2,
            sticky="W E S"
        )

        # Configure stretch ratios
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # Export dynamic elements
        global pipe_statusbar
        pipe_statusbar = statusbar.statusbar
        global pipe_moduletabs
        pipe_moduletabs = moduletabs.module_notebook


class BotControl(ui_window.Frame):
    def __init__(self, parent):
        """Modis control panel

        Args:
            parent: A tk or ttk object
        """

        super(BotControl, self).__init__(parent, "Modis control panel")

        from .. import main

        global pipe_statusbar
        global pipe_moduletabs

        # stop button
        self.button_stop = ttk.Button(
            self,
            command=lambda: main.stop(pipe_statusbar, pipe_moduletabs, self),
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
            command=lambda: main.thread_init(pipe_statusbar, pipe_moduletabs, self),
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


class ModuleTabs(ui_window.Frame):
    def __init__(self, parent):
        """The notebook showing the tabs for all the modules

        Args:
            parent: A tk or ttk object
        """

        super(ModuleTabs, self).__init__(parent, "Module tabs")

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


class Log(ui_window.Frame):
    def __init__(self, parent):
        """The text box showing Python console log

        Args:
            parent: A tk or ttk object
        """

        super(Log, self).__init__(parent, "Python console log")

        # Log text box
        log = tk.Text(self)
        log.grid(
            column=0,
            row=0,
            padx=4,
            pady=4,
            sticky="W E N S"
        )
        log.insert("end", "Welcome to Modis Beta v2.2\n")

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

        class StdoutRedirector(object):
            def __init__(self, text_widget):
                self.text_widget = text_widget

            def write(self, string):
                self.text_widget.insert("end", string)
                self.text_widget.see("end")

        sys.stdout = StdoutRedirector(log)

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
