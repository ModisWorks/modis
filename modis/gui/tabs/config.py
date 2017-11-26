import logging
import tkinter as tk

logger = logging.getLogger(__name__)


class Frame(tk.Frame):
    """A tab containing all the controls for API keys and data"""

    def __init__(self, parent):
        """Create the frame.

        Args:
            parent: A tk or ttk object.
        """

        super(Frame, self).__init__(parent)
