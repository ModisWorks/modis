from tools import ui_window
from share import *

pagename = "Chatbot"
pad_element = 2


class Page(ui_window.Page):
    def __init__(self, parent):
        super(Page, self).__init__(parent)

        apicalls = APICalls(self)

        apicalls.grid(
            column=0,
            row=0,
            padx=pad_element,
            pady=pad_element,
            sticky="W E N S"
        )

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)


class APICalls(ui_window.Frame):
    def __init__(self, parent):
        super(APICalls, self).__init__(parent, "Mitsuku API calls")

        self.display = tk.Text(self)

        self.display.grid(
            column=0,
            row=0,
            padx=pad_element,
            pady=pad_element,
            sticky="W E N S"
        )

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
