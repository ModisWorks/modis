import logging
import tkinter as tk

logger = logging.getLogger(__name__)


class Frame(tk.Frame):
    """A tab containing controls for the data.json"""

    def __init__(self, parent):
        """Create the frame.

        Args:
            parent: A tk or ttk object.
        """

        super(Frame, self).__init__(parent)

        self.image = tk.PhotoImage(file=__file__[:-16] + "assets/data.png")
        self.label = tk.Label(self, image=self.image)
        self.label.grid()
