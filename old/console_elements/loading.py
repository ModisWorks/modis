import tkinter.ttk as ttk


class UI(ttk.Frame):
    def __init__(self, parent):
        """A simple frame with a loading bar to use when something is loading

        Args:
            parent: A tk or ttk object
        """

        super(UI, self).__init__(parent)

        # Loading label
        loading_label = ttk.Label(
            self,
            text="Loading"
        )
        loading_label.grid(
            column=1,
            row=1,
            padx=2,
            pady=2
        )

        # Loading bar
        loading_bar = ttk.Progressbar(
            self,
            orient="horizontal",
            length=128,
            mode='indeterminate'
        )
        loading_bar.start(6)
        loading_bar.grid(
            column=1,
            row=2,
            padx=2,
            pady=2
        )

        # Configure stretch ratios
        self.columnconfigure(0, weight=1)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(3, weight=1)
