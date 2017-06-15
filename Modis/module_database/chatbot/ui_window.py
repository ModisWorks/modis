from tools import ui_window
from share import *

pagename = "Chatbot"
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
        module_pipes["chatbot"] = apicalls.display


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
                "call",
                "time"
            ],
            displaycolumns=[
                "call",
                "time"
            ],
            show=["headings"]
        )
        self.display.grid(
            column=0,
            row=0,
            padx=pad_element,
            pady=pad_element,
            sticky="W E N S"
        )
        self.display.column('call', width=128, anchor='e')
        self.display.heading('call', text='Call')
        self.display.column('time', anchor='w')
        self.display.heading('time', text='Timestamp')

        # Configure stretch ratios
        self.rowconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
