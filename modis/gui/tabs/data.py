import logging
import tkinter as tk
import tkinter.ttk as ttk

logger = logging.getLogger(__name__)


class Frame(tk.Frame):
    """A tab containing controls for the data.json"""

    def __init__(self, parent):
        """Create the frame.

        Args:
            parent: A tk or ttk object.
        """

        super(Frame, self).__init__(parent)

        # Add elements
        tree = self.DataTree(self)

        # Grid elements
        tree.grid(column=0, row=0, padx=8, pady=8, sticky="W E N S")

        # Configure stretch ratios
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

    class DataTree(ttk.LabelFrame):
        """The text box showing the logging output"""

        def __init__(self, parent):
            """Create the tree.

            Args:
                parent: A tk or ttk object.
            """

            super(Frame.DataTree, self).__init__(parent, padding=8, text="Data tree")

            # Data tree
            self.tree = ttk.Treeview(self, columns="val")
            self.tree.column("#0", width=50)
            self.tree.heading("#0", text="Key")
            self.tree.heading("val", text="Value")
            self.update()

            # Vertical scrollbar
            scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
            self.tree['yscrollcommand'] = scrollbar.set

            # Horizontal scrollbar
            scrollbar = ttk.Scrollbar(self, orient="horizontal", command=self.tree.xview)
            self.tree['xscrollcommand'] = scrollbar.set

            # Grid elements
            self.tree.grid(column=0, row=0, sticky="W E N S")
            scrollbar.grid(column=1, row=0, sticky="N S")
            scrollbar.grid(column=0, row=1, sticky="W E")

            # Configure stretch ratios
            self.columnconfigure(0, weight=1)
            self.rowconfigure(0, weight=1)

        def update(self):
            from modis.tools import datatools

            def recursive_add(data, parent=""):
                for key in data:
                    if type(data[key]) is dict:
                        recursive_add(data[key], self.tree.insert(parent, "end", text=key))
                    else:
                        self.tree.insert(parent, "end", text=key, values=str(data[key]))

            recursive_add(datatools.data)
