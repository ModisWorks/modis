import logging

import tkinter.ttk as ttk

logger = logging.getLogger(__name__)


class Frame(ttk.Frame):
    def __init__(self, parent):
        super(Frame, self).__init__(parent)

        logger.debug("Initialising frame")
