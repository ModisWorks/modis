from ..share import *

pad_frame = 8


class Page(ttk.Frame):
    def __init__(self, parent):
        """Creates a page for the notebook

        Args:
            parent (ttk.Notebook): The notebook to place the page into
        """

        super(Page, self).__init__(
            parent,
            padding=pad_frame,
        )


class Frame(ttk.LabelFrame):
    def __init__(self, parent, label):
        """Creates a frame for a page

        Args:
            parent (tk.Frame): The page to place the frame into
        """
        super(Frame, self).__init__(
            parent,
            padding=pad_frame,
            text=label
        )
