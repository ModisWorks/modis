import asyncio
import logging
import threading
import tkinter as tk
import tkinter.ttk as ttk

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
        log = self.CoreLog(self)
        botcontrol = self.CoreControl(self)

        # Grid elements
        log.grid(column=0, row=0, padx=8, pady=8, sticky="W E N S")
        botcontrol.grid(column=0, row=1, padx=8, pady=8, sticky="W E S")

        # Configure stretch ratios
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=0)

    class CoreControl(ttk.Labelframe):
        """The control panel for the Modis bot."""

        def __init__(self, parent):
            """Create the frame.

            Args:
                parent: A tk or ttk object.
            """

            super(Frame.CoreControl, self).__init__(parent, padding=8, text="Modis control panel")

            # Toggle button
            self.state = "off"
            self.button_text = tk.StringVar(value="Start Modis")
            self.button = ttk.Button(self, command=lambda: self.toggle(), textvariable=self.button_text)
            self.button.grid(column=3, row=1, padx=4, pady=4, sticky="W E N S")

            # Configure stretch ratios
            self.columnconfigure(0, weight=1)
            self.columnconfigure(1, weight=2)

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

            # Start Modis
            logger.debug("Starting Modis")
            statuslog = logging.getLogger("globalstatus")
            statuslog.info("1")
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
            logger.info("Stopping Modis")
            statuslog = logging.getLogger("globalstatus")
            statuslog.info("0")
            from modis.main import client
            asyncio.run_coroutine_threadsafe(client.logout(), client.loop)

    class CoreLog(ttk.Labelframe):
        """The text box showing the logging output"""

        def __init__(self, parent):
            """Create the frame.

            Args:
                parent: A tk or ttk object.
            """

            super(Frame.CoreLog, self).__init__(parent, padding=8, text="Python console log")

            # Log text box
            log_panel = tk.Text(self, wrap="none")
            log_panel.grid(column=0, row=0, sticky="W E N S")

            # Log colours
            log_panel.tag_config('CRITICAL', foreground="red", underline=True)
            log_panel.tag_config('ERROR', foreground="red")
            log_panel.tag_config('WARNING', foreground="orange")
            log_panel.tag_config('INFO', foreground="black")
            log_panel.tag_config('DEBUG', foreground="dark grey")

            # Vertical scrollbar
            yscrollbar = ttk.Scrollbar(self, orient="vertical", command=log_panel.yview)
            yscrollbar.grid(column=1, row=0, sticky="N S")
            log_panel['yscrollcommand'] = yscrollbar.set

            # Horizontal scrollbar
            xscrollbar = ttk.Scrollbar(self, orient="horizontal", command=log_panel.xview)
            xscrollbar.grid(column=0, row=1, sticky="W E")
            log_panel['xscrollcommand'] = xscrollbar.set

            # Add log panel as a handler to root logger
            # Get logger
            discord_logger = logging.getLogger("modis")

            # Setup format
            formatter = logging.Formatter("{levelname:8} {name} - {message}", style="{")

            # Setup handler
            class PanelHandler(logging.Handler):
                def __init__(self, text_widget):
                    logging.Handler.__init__(self)

                    self.text_widget = text_widget
                    self.text_widget.config(state=tk.DISABLED)

                def flush(self):
                    try:
                        self.text_widget.see("end")
                    except:
                        pass

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
                    self.flush()

            panel_handler = PanelHandler(log_panel)
            panel_handler.setFormatter(formatter)
            discord_logger.addHandler(panel_handler)

            # Configure stretch ratios
            self.columnconfigure(0, weight=1)
            self.rowconfigure(0, weight=1)
