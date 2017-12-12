import asyncio
import logging
import threading
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
import webbrowser
import json

from modis.tools import data, config

logger = logging.getLogger(__name__)


class Frame(tk.Frame):
    """A tab containing the core controls of the bot"""

    def __init__(self, parent):
        """Create the frame.

        Args:
            parent: A tk or ttk object.
        """

        super(Frame, self).__init__(parent)

        # Add elements
        info = self.Info(self)
        control = self.Control(self)
        log = self.Log(self)

        # Grid elements
        info.grid(column=0, row=0, padx=8, pady=8, stick="W E N S")
        control.grid(column=1, row=0, padx=8, pady=8, sticky="W E N S")
        log.grid(column=0, columnspan=2, row=1, padx=8, pady=8, sticky="W E N S")

        # Configure stretch ratios
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)

    class Info(ttk.LabelFrame):
        """The control panel for the Modis bot."""

        def __init__(self, parent):
            """Create the frame.

            Args:
                parent: A tk or ttk object.
            """

            super(Frame.Info, self).__init__(parent, padding=8, text="Info")

            # Variables
            self.invite_text = tk.StringVar(value="Paste Client ID here for invite link")

            # Add elements
            def hyperlink_website(event):
                webbrowser.open_new("https://infraxion.github.io/modis/")

            def hyperlink_discord(event):
                webbrowser.open_new("https://infraxion.github.io/modis/")

            def hyperlink_invite(event):
                webbrowser.open_new("https://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions=0".format(self.invite_text.get()))

            image = tk.PhotoImage(file=__file__[:-16] + "assets/64t.png")
            logo = tk.Label(self, image=image)
            logo.image = image

            name = tk.Label(self, text="Welcome to Modis c:", justify="left")
            website = tk.Label(self, text="Website", fg="blue", cursor="hand2")
            website.bind("<Button-1>", hyperlink_website)
            discord = tk.Label(self, text="Discord server", fg="blue", cursor="hand2")
            discord.bind("<Button-1>", hyperlink_discord)

            clientid_entry = ttk.Entry(self, textvariable=self.invite_text)
            invite_link = tk.Label(self, text="Invite bot to server", fg="blue", cursor="hand2")
            invite_link.bind("<Button-1>", hyperlink_invite)

            # Grid elements
            logo.grid(column=0, row=0, rowspan=3, padx=4, pady=4, sticky="W")

            name.grid(column=1, row=0, padx=4, pady=4, sticky="W")
            website.grid(column=1, row=1, padx=4, pady=0, sticky="W")
            discord.grid(column=1, row=2, padx=4, pady=0, sticky="W")

            clientid_entry.grid(column=0, columnspan=2, row=3, padx=4, pady=4, sticky="W E")
            invite_link.grid(column=0, columnspan=2, row=4, padx=4, pady=0, sticky="W")

            # Configure stretch ratios
            self.columnconfigure(0, weight=0)
            self.columnconfigure(1, weight=1)
            self.rowconfigure(0, weight=0)
            self.rowconfigure(1, weight=0)
            self.rowconfigure(2, weight=0)
            self.rowconfigure(3, weight=0)
            self.rowconfigure(4, weight=0)

    class Control(ttk.Labelframe):
        """The control panel for the Modis bot."""

        def __init__(self, parent):
            """Create the frame.

            Args:
                parent: A tk or ttk object.
            """

            super(Frame.Control, self).__init__(parent, padding=8, text="Control")

            # Variables
            self.datapath = tk.StringVar(value=config.DATAFILE)

            self.token = tk.StringVar(value=data.cache["keys"]["discord_token"])

            self.state = "off"
            self.button_text = tk.StringVar(value="Start Modis")

            # Add elements
            datapath_label = ttk.Label(self, text="Data file path:")
            datapath_entry = ttk.Entry(self, textvariable=self.datapath, state="readonly")
            datapath_button = ttk.Button(self, command=self.set_data_location, text="Change")

            token_label = ttk.Label(self, text="Discord bot token:")
            token_entry = ttk.Entry(self, textvariable=self.token, show="*")

            start_button = ttk.Button(self, command=self.toggle, textvariable=self.button_text)

            # Grid elements
            datapath_label.grid(column=0, row=0, padx=4, pady=4, stick="E")
            datapath_entry.grid(column=1, row=0, padx=4, pady=4, sticky="W E")
            datapath_button.grid(column=2, row=0, padx=4, pady=4, sticky="E")

            token_label.grid(column=0, row=1, padx=4, pady=4, sticky="E")
            token_entry.grid(column=1, columnspan=2, row=1, padx=4, pady=4, sticky="W E")

            start_button.grid(column=2, columnspan=3, row=3, padx=4, pady=4, sticky="E")

            # Configure stretch ratios
            self.columnconfigure(0, weight=0)
            self.columnconfigure(1, weight=1)
            self.columnconfigure(2, weight=0)
            self.rowconfigure(0, weight=0)
            self.rowconfigure(1, weight=0)
            self.rowconfigure(2, weight=1)
            self.rowconfigure(3, weight=0)

        def set_data_location(self):
            try:
                self.datapath.set(filedialog.askopenfile().name)
            except AttributeError:
                logger.warning("Data file not changed")
                return

            old = config.DATAFILE
            config.DATAFILE = self.datapath.get()

            try:
                data.get()
            except json.decoder.JSONDecodeError:
                logger.error("Chosen file is not a valid json; reverting changes")
                self.datapath.set(old)
                config.DATAFILE = old
                data.get()
                return

            if not data.is_valid(data.cache):
                logger.error("Chosen file is not a valid Modis data file; reverting changes")
                self.datapath.set(old)
                config.DATAFILE = old
                data.get()
                return

            logger.warning("data file changed to " + config.DATAFILE)

        def toggle(self):
            """Toggle Modis on or off."""

            if self.state == 'off':
                self.start()
            elif self.state == 'on':
                self.stop()

        def start(self):
            """Start Modis and log it into Discord."""

            self.button_text.set("Stop Modis")
            self.state = "on"

            logger.warning("Starting Modis")
            statuslog = logging.getLogger("globalstatus")
            statuslog.info("1")

            data.cache["keys"]["discord_token"] = self.token.get()
            data.write()

            from modis import main
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            thread = threading.Thread(target=main.start, args=[loop])
            thread.start()

        def stop(self):
            """Stop Modis and log out of Discord."""

            self.button_text.set("Start Modis")
            self.state = "off"

            # Stop Modis
            logger.warning("Stopping Modis")
            statuslog = logging.getLogger("globalstatus")
            statuslog.info("0")
            from modis.main import client
            asyncio.run_coroutine_threadsafe(client.logout(), client.loop)

    class Log(ttk.Labelframe):
        """The text box showing the logging output"""

        def __init__(self, parent):
            """Create the frame.

            Args:
                parent: A tk or ttk object.
            """

            super(Frame.Log, self).__init__(parent, padding=8, text="Log")

            # Add elements
            log_panel = tk.Text(self, wrap="none")

            formatter = logging.Formatter("{levelname:8} {name} - {message}", style="{")
            handler = self.PanelHandler(log_panel)
            handler.setFormatter(formatter)

            root_logger = logging.getLogger("modis")
            root_logger.addHandler(handler)

            log_panel.configure(background="#202020")
            log_panel.tag_config('CRITICAL', foreground="#FF00AA")
            log_panel.tag_config('ERROR', foreground="#FFAA00")
            log_panel.tag_config('WARNING', foreground="#00AAFF")
            log_panel.tag_config('INFO', foreground="#AAAAAA")
            log_panel.tag_config('DEBUG', foreground="#444444")

            yscrollbar = ttk.Scrollbar(self, orient="vertical", command=log_panel.yview)
            xscrollbar = ttk.Scrollbar(self, orient="horizontal", command=log_panel.xview)
            log_panel['yscrollcommand'] = yscrollbar.set
            log_panel['xscrollcommand'] = xscrollbar.set

            # Grid elements
            log_panel.grid(column=0, row=0, sticky="W E N S")
            yscrollbar.grid(column=1, row=0, sticky="N S")
            xscrollbar.grid(column=0, row=1, sticky="W E")

            # Configure stretch ratios
            self.columnconfigure(0, weight=1)
            self.rowconfigure(0, weight=1)

        class PanelHandler(logging.Handler):
            def __init__(self, text_widget):
                logging.Handler.__init__(self)

                self.text_widget = text_widget
                self.text_widget.config(state=tk.DISABLED)

            def emit(self, record):
                msg = self.format(record)
                msg_level = logging.Formatter("{levelname}", style="{").format(record)
                # Remove '.modis' from start of logs
                msg = msg[:9] + msg[15:]
                # Exceptions
                if msg_level.startswith("ERROR"):
                    msg_level = "ERROR"

                self.text_widget.config(state=tk.NORMAL)
                self.text_widget.insert("end", msg + "\n", msg_level)
                self.text_widget.config(state=tk.DISABLED)
                self.text_widget.see("end")
