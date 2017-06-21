from ...tools import ui_window
from tkinter import ttk

pagename = "chatbot"
pad_element = 2


class Page(ui_window.Page):
    def __init__(self, parent):
        """The module tab for chatbot

        Args:
            parent: tk or ttk obkect
        """

        super(Page, self).__init__(parent)

        # API call log
        apicalls = APICalls(self)

        apicalls.grid(
            column=0,
            row=0,
            padx=pad_element,
            pady=pad_element,
            sticky="W E N S"
        )

        # Configure stretch ratios
        self.rowconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # Register dynamic elements globally
        from . import _constants
        _constants.pipe_api_mitsuku = apicalls.display


class APICalls(ui_window.Frame):
    def __init__(self, parent):
        """The tree showing all API calls made to Mitsuku

        Args:
            parent: tk or ttk object
        """

        super(APICalls, self).__init__(parent, "Mitsuku API calls")

        # API call history tree
        self.display = ttk.Treeview(
            self,
            columns=[
                "input",
                "output",
                "time"
            ]
        )
        self.display.grid(
            column=0,
            row=0,
            padx=pad_element,
            pady=pad_element,
            sticky="W E N S"
        )
        self.display.column("input", width=100, minwidth=100, stretch=True, anchor="w")
        self.display.heading("input", text="Input")
        self.display.column("output", width=100, minwidth=100, stretch=True, anchor="w")
        self.display.heading("output", text="Output")
        self.display.column("time", width=160, minwidth=160, stretch=False, anchor="center")
        self.display.heading("time", text="Time")

        # Vertical scrollbar
        scrollbar = ttk.Scrollbar(
            self,
            orient="vertical",
            command=self.display.yview
        )
        scrollbar.grid(
            column=1,
            row=0,
            sticky="N S")
        self.display['yscrollcommand'] = scrollbar.set

        # Horizontal scrollbar
        scrollbar = ttk.Scrollbar(
            self,
            orient="horizontal",
            command=self.display.xview
        )
        scrollbar.grid(
            column=0,
            row=1,
            sticky="W E")
        self.display['xscrollcommand'] = scrollbar.set

        # Configure stretch ratios
        self.rowconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
