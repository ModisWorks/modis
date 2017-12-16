import logging
import tkinter as tk
import tkinter.ttk as ttk

from modis.tools import help, config, moduledb

logger = logging.getLogger(__name__)


class Frame(ttk.Frame):
    """A tab containing UI pages for all the modules"""

    def __init__(self, parent):
        """Create the frame.

        Args:
            parent: A tk or ttk object.
        """

        super(Frame, self).__init__(parent)

        # Configure styles
        s = ttk.Style()
        s.configure(
            "modis2.TNotebook",
            tabmargins=[0, 0, -1, 0],
            tabposition="wn"
        )
        s.configure(
            "modis2.TNotebook.Tab",
            padding=4,
            width=15
        )
        s.map(
            "modis2.TNotebook.Tab",
            expand=[
                ("selected", [0, 0, 1, 0]),
                ("active", [0, 0, 1, 0])
            ]
        )

        # Add elements
        self.nav = ttk.Notebook(self, style="modis2.TNotebook")

        # Grid elements
        self.nav.grid(column=0, row=0, padx=0, pady=0, sticky="W E N S")

        # Configure stretch ratios
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.scan()

    def scan(self):
        modules = moduledb.get_imports(["__ui"])

        for module_name in modules.keys():
            if "__ui" not in modules[module_name].keys():
                logger.debug("No module UI for " + module_name)
                module_ui = None
            else:
                logger.debug("Module UI found for " + module_name)
                module_ui = modules[module_name]["__ui"].ModuleUIFrame
            module_frame = self.ModuleFrame(self.nav, module_name, module_ui)
            self.nav.add(module_frame, text=module_name)

    class ModuleFrame(ttk.Frame):
        """The base frame for a module's UI."""

        def __init__(self, parent, module_name, module_ui):
            """Create the frame.

            Args:
                parent: A tk or ttk object.
                module_name (str): The name of the module.
                module_frame (import): The __ui.py file to add for the module.
            """

            super(Frame.ModuleFrame, self).__init__(parent, padding=8)

            # Add elements
            if module_ui:
                module_frame = module_ui(self)
            else:
                module_frame = ttk.Frame(self)

            nav = ttk.Notebook(self)
            help_frame = self.HelpFrame(self, module_name)
            log_frame = self.LogFrame(self, module_name)
            nav.add(help_frame, text="Help")
            nav.add(log_frame, text="Log")

            # Grid elements
            module_frame.grid(row=0, column=0, sticky="W E N S")
            nav.grid(row=1, column=0, padx=8, pady=8, sticky="W E N S")

            # Configure stretch ratios
            self.columnconfigure(0, weight=1)
            self.rowconfigure(0, weight=0)
            self.rowconfigure(1, weight=1)

        class HelpFrame(ttk.Frame):
            def __init__(self, parent, module_name):

                super(Frame.ModuleFrame.HelpFrame, self).__init__(parent, padding=8)

                # Add elements
                help_panel = tk.Text(self)

                help_panel.configure(background="#202020", wrap="word")
                help_panel.tag_config("title", font="TkHeadingFont 20 bold", justify="center", foreground="#AAAAAA")
                help_panel.tag_config("heading", font="TkHeadingFont 14 bold italic", foreground="#AAAAAA")
                help_panel.tag_config("command", font="TkFixedFont", foreground="#FFAA00")
                help_panel.tag_config("param", font="TkFixedFont", foreground="#00AAFF")
                help_panel.tag_config("description", font="TkTextFont", foreground="#AAAAAA")

                yscrollbar = ttk.Scrollbar(self, orient="vertical", command=help_panel.yview)
                xscrollbar = ttk.Scrollbar(self, orient="horizontal", command=help_panel.xview)
                help_panel['yscrollcommand'] = yscrollbar.set
                help_panel['xscrollcommand'] = xscrollbar.set

                # Grid elements
                help_panel.grid(column=0, row=0, sticky="W E N S")
                yscrollbar.grid(column=1, row=0, sticky="N S")
                xscrollbar.grid(column=0, row=1, sticky="W E")

                # Configure stretch ratios
                self.columnconfigure(0, weight=1)
                self.rowconfigure(0, weight=1)

                help_contents = help.get_raw(module_name)
                help_panel.insert("end", "\n{}\n".format(module_name), "title")
                for d in help_contents:
                    help_panel.insert("end", "\n\n    {}\n\n".format(d), "heading")

                    if "commands" not in d.lower():
                        help_panel.insert("end", help_contents[d] + "\n\n", "desc")
                        continue

                    for c in help_contents[d]:
                        if "name" not in c:
                            continue

                        command = "!" + c["name"]
                        help_panel.insert("end", command, ("command", "desc"))
                        if "params" in c:
                            for param in c["params"]:
                                help_panel.insert("end", " -" + param, ("param", "desc"))
                        help_panel.insert('end', " - ", "description")
                        if "description" in c:
                            help_panel.insert("end", c["description"], "description")

                        help_panel.insert("end", "\n")

                help_panel.config(state=tk.DISABLED)

        class LogFrame(ttk.Frame):
            """The text box showing the logging output"""

            def __init__(self, parent, module_name):
                """Create the frame.

                Args:
                    parent: A tk or ttk object.
                """

                super(Frame.ModuleFrame.LogFrame, self).__init__(parent, padding=8)

                # Add elements
                log_panel = tk.Text(self, wrap="none")

                formatter = logging.Formatter(
                    "{levelname:8} {name} - {message}", style="{")
                handler = self.PanelHandler(log_panel)
                handler.setFormatter(formatter)

                root_logger = logging.getLogger("modis.modules." + module_name)
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
                    msg_level = logging.Formatter("{levelname}",
                                                  style="{").format(record)
                    # Remove '.modis' from start of logs
                    msg = msg[:9] + msg[23:]
                    # Exceptions
                    if msg_level.startswith("ERROR"):
                        msg_level = "ERROR"

                    self.text_widget.config(state=tk.NORMAL)
                    self.text_widget.insert("end", msg + "\n", msg_level)
                    self.text_widget.config(state=tk.DISABLED)
                    self.text_widget.see("end")
