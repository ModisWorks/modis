import logging
import tkinter as tk
import tkinter.ttk as ttk

logger = logging.getLogger(__name__)


class ModuleUIFrame(ttk.Frame):
    """The UI for the music module"""

    def __init__(self, parent):
        """
        Create a new UI for the module

        Args:
            parent: A tk or ttk object
        """

        super(ModuleUIFrame, self).__init__(parent)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        # Set default values
        from ....datatools import get_data
        data = get_data()

        # API Frame
        api_frame = ttk.LabelFrame(self, padding=8, text="Google API")
        api_frame.grid(row=0, column=0, sticky="W E N S")
        api_frame.columnconfigure(0, weight=1)
        # Add key fields
        self.google_api_key = tk.StringVar()
        ttk.Label(api_frame, text="Google API Key").grid(column=0, row=0, sticky="W E N S")
        ttk.Entry(api_frame, textvariable=self.google_api_key).grid(
            column=0, row=1, padx=0, pady=4, sticky="W E N S")
        self.soundcloud_client_id = tk.StringVar()
        ttk.Label(api_frame, text="SoundCloud Client ID").grid(column=0, row=2, sticky="W E N S")
        ttk.Entry(api_frame, textvariable=self.soundcloud_client_id).grid(
            column=0, row=3, padx=0, pady=4, sticky="W E N S")
        ttk.Button(api_frame, command=lambda: self.update_keys(), text="Update API Data").grid(
            column=0, row=4, padx=0, pady=4, sticky="W E N S")

        if "google_api_key" in data["discord"]["keys"]:
            self.google_api_key.set(data["discord"]["keys"]["google_api_key"])
        if "soundcloud_client_id" in data["discord"]["keys"]:
            self.soundcloud_client_id.set(data["discord"]["keys"]["soundcloud_client_id"])

    def update_keys(self):
        """Updates the Google API key with the text value"""
        from ...main import add_api_key
        add_api_key("google_api_key", self.google_api_key.get())
        add_api_key("soundcloud_client_id", self.soundcloud_client_id.get())
