import logging
import os
import tkinter.ttk as ttk

from .._tools import helptools

logger = logging.getLogger(__name__)


class ModuleUIFrame(ttk.Frame):
    """The UI for the manager module"""

    def __init__(self, parent):
        """
        Create a new UI for the module

        Args:
            parent: A tk or ttk object
        """

        super(ModuleUIFrame, self).__init__(parent, padding=8)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        # Help frame
        help_frame = ttk.LabelFrame(self, padding=8, text="Help")
        help_frame.grid(row=1, column=0, sticky="W E N S")
        help_frame.columnconfigure(0, weight=1)
        help_frame.rowconfigure(0, weight=1)
        # Find the help path
        _dir = os.path.realpath(
            os.path.join(os.getcwd(), os.path.dirname(__file__)))
        help_path = "{}/{}".format(_dir, "_help.json")
        # Load the text
        helptools.add_help_text(help_frame, help_path)
