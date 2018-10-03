import logging
import tkinter as tk
import tkinter.ttk as ttk

from modis.tools import help, config, moduledb

logger = logging.getLogger(__name__)


class Frame(ttk.Frame):
    """A tab containing tools to install and manage modules"""

    def __init__(self, parent):
        """Create the frame.

        Args:
            parent: A tk or ttk object.
        """

        super(Frame, self).__init__(parent, padding=8)

        # Add elements
        installed = self.Installed(self)
        find = self.Find(self)

        # Grid elements
        installed.grid(column=0, row=0, padx=8, pady=8, sticky="W E N S")
        find.grid(column=1, row=0, padx=8, pady=8, sticky="E N S")

        # Configure stretch ratios
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=0)
        self.rowconfigure(0, weight=1)

    class Installed(ttk.LabelFrame):
        """List of installed modules"""

        def __init__(self, parent):
            """Create the frame.

            Args:
                parent: A tk or ttk object.
            """

            super(Frame.Installed, self).__init__(parent, padding=8, text="Manage module")

            # Variables
            self.moduledb = {}
            self.module_ui_cache = {}

            # Add elements
            self.module_list = ttk.Treeview(self, show="tree")
            self.module_list.bind("<<TreeviewSelect>>", self.module_select)
            self.module_list.column("#0", width=100)
            yscrollbar = ttk.Scrollbar(self, orient="vertical", command=self.module_list.yview)
            self.module_list['yscrollcommand'] = yscrollbar.set

            self.module_ui_container = ttk.Frame(self)
            self.module_ui_container.columnconfigure(0, weight=1)
            self.module_ui_container.rowconfigure(0, weight=1)

            # Grid elements
            self.module_list.grid(column=0, row=0, padx=(4, 0), pady=4, sticky="W N S")
            yscrollbar.grid(column=1, row=0, padx=(0, 4), pady=4, sticky="W N S")
            self.module_ui_container.grid(column=2, row=0, sticky="W E N S")

            # Configure stretch ratios
            self.columnconfigure(0, weight=0)
            self.columnconfigure(1, weight=0)
            self.columnconfigure(2, weight=1)
            self.rowconfigure(0, weight=1)

            # Import module UIs
            self.moduledb = moduledb.get_imports(["__ui"])

            for module_name in self.moduledb.keys():
                # Register module into module list
                self.module_list.insert('', 'end', module_name, text=module_name)

                # Create module frame
                self.module_ui_cache[module_name] = ttk.Frame(self.module_ui_container)
                self.module_ui_cache[module_name].grid(row=0, column=0, sticky="W E N S")
                self.module_ui_cache[module_name].lower()

                # Scan module database for module ui
                if "__ui" not in self.moduledb[module_name].keys():
                    logger.debug("No module UI for " + module_name)
                else:
                    logger.debug("Module UI found for " + module_name)

                    # Add elements
                    module_ui = self.moduledb[module_name]["__ui"].ModuleUIFrame(self.module_ui_cache[module_name])

                    # Grid elements
                    module_ui.grid(row=0, column=0, sticky="W E N S")

                # Add elements
                nav = ttk.Notebook(self.module_ui_cache[module_name])
                help_frame = self.HelpFrame(nav, module_name)
                log_frame = self.LogFrame(nav, module_name)
                nav.add(help_frame, text="Help")
                nav.add(log_frame, text="Log")

                # Grid elements
                nav.grid(row=1, column=0, padx=4, pady=4, sticky="W E N S")

                # Configure stretch ratios
                self.module_ui_cache[module_name].columnconfigure(0, weight=1)
                self.module_ui_cache[module_name].rowconfigure(0, weight=0)
                self.module_ui_cache[module_name].rowconfigure(1, weight=1)

        def module_select(self, event):
            selected = self.module_list.focus()
            self.module_ui_cache[selected].lift()

        class HelpFrame(ttk.Frame):
            def __init__(self, parent, module_name):

                super(Frame.Installed.HelpFrame, self).__init__(parent, padding=8)

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
                self.columnconfigure(1, weight=0)
                self.rowconfigure(0, weight=1)
                self.rowconfigure(1, weight=0)

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

                super(Frame.Installed.LogFrame, self).__init__(parent, padding=8)

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
                self.columnconfigure(1, weight=0)
                self.rowconfigure(0, weight=1)
                self.rowconfigure(1, weight=0)

            class PanelHandler(logging.Handler):
                def __init__(self, text_widget):
                    logging.Handler.__init__(self)

                    self.text_widget = text_widget
                    self.text_widget.config(state=tk.DISABLED)

                def emit(self, record):
                    msg = self.format(record)
                    msg_level = logging.Formatter("{levelname}", style="{").format(record)

                    # Remove '.modis' from start of logs
                    msg = msg[:9] + msg[23:]

                    # Exceptions
                    if msg_level.startswith("ERROR"):
                        msg_level = "ERROR"

                    self.text_widget.config(state=tk.NORMAL)
                    self.text_widget.insert("end", msg + "\n", msg_level)
                    self.text_widget.config(state=tk.DISABLED)
                    self.text_widget.see("end")

    class Find(ttk.LabelFrame):
        """Find modules off GitHub"""

        def __init__(self, parent):
            """Create the frame.

            Args:
                parent: A tk or ttk object.
            """

            super(Frame.Find, self).__init__(parent, padding=8, text="Module downloader")

            # Variables
            self.repo = tk.StringVar(value="modisworks")

            # Add elements
            repo_entry = ttk.Entry(self, textvariable=self.repo)
            repo_scan = ttk.Button(self, command=self.scan, text="Scan repo")

            self.module_list = ttk.Treeview(self, show="tree")
            self.module_list.column("#0", width=100)
            yscrollbar = ttk.Scrollbar(self, orient="vertical", command=self.module_list.yview)
            self.module_list['yscrollcommand'] = yscrollbar.set

            install_button = ttk.Button(self, command=self.install, text="Install")

            # Grid elements
            repo_entry.grid(column=0, columnspan=2, row=0, padx=4, pady=4, sticky="W E N")
            repo_scan.grid(column=0, columnspan=2, row=1, padx=4, pady=4, sticky="E N")
            self.module_list.grid(column=0, row=2, padx=(4, 0), pady=4, sticky="W E N S")
            yscrollbar.grid(column=1, row=2, padx=(0, 4), pady=4, sticky="N S")
            install_button.grid(column=0, columnspan=2, row=3, padx=4, pady=4, sticky="E S")

            # Configure stretch ratios
            self.columnconfigure(0, weight=1)
            self.columnconfigure(1, weight=0)
            self.rowconfigure(0, weight=0)
            self.rowconfigure(1, weight=0)
            self.rowconfigure(2, weight=1)
            self.rowconfigure(3, weight=0)

        def scan(self):
            pass

        def install(self):
            pass
