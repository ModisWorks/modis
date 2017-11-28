import importlib
import logging
import os
import tkinter as tk
import tkinter.ttk as ttk

from modis.tools import help, config

logger = logging.getLogger(__name__)


class Frame(tk.Frame):
    """A tab containing UI pages for all the modules"""

    def __init__(self, parent):
        """Create the frame.

        Args:
            parent: A tk or ttk object.
        """

        super(Frame, self).__init__(parent)

        # Setup styles
        style = ttk.Style()
        style.configure("Module.TFrame", background="white")

        self.module_buttons = {}
        self.current_button = None

        # Add elements
        self.module_list = ttk.Frame(self, width=150, style="Module.TFrame")
        self.header = tk.Label(self.module_list, text="Modules", bg="white", fg="#484848")
        self.module_selection = ttk.Frame(self.module_list, style="Module.TFrame")
        self.module_ui = ttk.Frame(self)

        # Grid elements
        self.module_list.grid(column=0, row=0, padx=0, pady=0, sticky="W E N S")
        self.header.grid(column=0, row=0, padx=0, pady=0, sticky="W E N")
        self.module_selection.grid(column=0, row=1, padx=0, pady=0, sticky="W E N S")
        self.module_ui.grid(column=1, row=0, padx=0, pady=0, sticky="W E N S")

        # Configure stretch ratios
        self.module_list.columnconfigure(0, weight=1)
        self.module_list.rowconfigure(0, weight=0)
        self.module_list.rowconfigure(1, weight=1)
        self.module_selection.columnconfigure(0, weight=1)
        self.module_ui.columnconfigure(0, weight=1)
        self.module_ui.rowconfigure(0, weight=1)

        self.columnconfigure(0, minsize=150)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        self.scan()

    def add(self, module_name, module_ui):
        """Adds a module to the list.

        Args:
            module_name (str): The name of the module.
            module_ui (import): The function to call to create the module's UI.
        """

        m_button = tk.Label(self.module_selection, text=module_name, bg="white", anchor="w")
        m_button.grid(column=0, row=len(self.module_selection.winfo_children()), padx=0, pady=0, sticky="W E N S")

        self.module_buttons[module_name] = m_button
        m_button.bind("<Button-1>", lambda e: self.select(module_name, module_ui))

    def scan(self):
        # Iterate through modules
        for module_name in os.listdir(config.MODULES_DIR):
            module_dir = "{}/{}".format(config.MODULES_DIR, module_name)

            if not os.path.isdir(module_dir):
                continue
            if module_name.startswith("_"):
                continue

            files = os.listdir(module_dir)
            if "_ui.py" in files:
                logger.debug("Importing UI for {} module".format(module_name))
                import_name = ".modules.{}.{}".format(module_name, "_ui")
                self.add(module_name, importlib.import_module(import_name, "modis"))
            else:
                logger.debug("No UI for {} module".format(module_name))
                self.add(module_name, None)

    def select(self, module_name, module_ui):
        """Called when a module is selected.

        Args:
            module_name (str): The name of the module
            module_ui (import): The function to call to create the module's UI
        """

        if self.current_button == self.module_buttons[module_name]:
            return

        self.module_buttons[module_name].config(bg="#cacaca")
        if self.current_button is not None:
            self.current_button.config(bg="white")
        self.current_button = self.module_buttons[module_name]

        self.destroy()

        try:
            # Create the UI
            module_ui_frame = self.ModuleFrame(self.module_ui, module_name, module_ui)
            module_ui_frame.grid(column=0, row=0, sticky="W E N S")
        except Exception as e:
            logger.error("Could not load UI for {}".format(module_name))
            logger.exception(e)
            # Create a error UI
            tk.Label(self.module_ui, text="Could not load UI for {}".format(module_name)).grid(
                column=0, row=0, padx=0, pady=0, sticky="W E N S")

    def clear(self):
        """Clears all modules from the list."""

        for child in self.module_selection.winfo_children():
            child.destroy()

        self.destroy()

        tk.Label(self.module_ui, text="Start Modis and select a module").grid(
            column=0, row=0, padx=0, pady=0, sticky="W E N S")

        if self.current_button is not None:
            self.current_button.config(bg="white")

        self.module_buttons = {}
        self.current_button = None

    def destroy(self):
        """Clears everything in the UI."""

        for child in self.module_ui.winfo_children():
            child.destroy()

    class ModuleFrame(ttk.Frame):
        """The base frame for a module's UI."""

        def __init__(self, parent, module_name, module_ui):
            """Create the frame.

            Args:
                parent: A tk or ttk object.
                module_name (str): The name of the module.
                module_ui (import): The _ui.py file to add for the module.
            """

            super(Frame.ModuleFrame, self).__init__(parent, padding=8)

            # Add elements
            help_frame = ttk.LabelFrame(self, padding=8, text="Help")
            self.add_help_text(help_frame, module_name)

            # Grid elements
            if module_ui is not None:
                module_ui.ModuleUIFrame(self).grid(row=0, column=0, sticky="W E N S")
            help_frame.grid(row=1, column=0, sticky="W E N S")

            # Configure stretch ratios
            help_frame.columnconfigure(0, weight=1)
            help_frame.rowconfigure(0, weight=1)

            self.columnconfigure(0, weight=1)
            self.rowconfigure(1, weight=1)

        def add_help_text(self, parent, module_name, prefix="!"):
            """Load help text from a file and add it to the parent.

            Args:
                parent: A tk or ttk object.
                module_name (str): The module to load help text from.
                prefix (str): The prefix to use for commands.
            """

            import tkinter as tk
            import tkinter.ttk as ttk

            # Add elements
            text = tk.Text(parent, wrap='word', font=("Helvetica", 10))
            text.tag_config("heading", font=("Helvetica", 14))
            text.tag_config("command", font=("Courier", 10))
            text.tag_config("param", font=("Courier", 10))
            text.tag_config("desc")
            help_contents = help.get_help_data(module_name)
            for d in help_contents:
                text.insert('end', d + '\n', "heading")

                if "commands" not in d.lower():
                    text.insert('end', help_contents[d] + '\n\n', "desc")
                    continue

                for c in help_contents[d]:
                    if "name" not in c:
                        continue

                    command = prefix + c["name"]
                    text.insert('end', command, ("command", "desc"))
                    if "params" in c:
                        for param in c["params"]:
                            text.insert('end', " [{}]".format(param), ("param", "desc"))
                    text.insert('end', ": ")
                    if "desc" in c:
                        text.insert('end', c["desc"], "desc")

                    text.insert('end', '\n')

                text.insert('end', '\n')

            yscrollbar = ttk.Scrollbar(parent, orient="vertical", command=text.yview)
            text['yscrollcommand'] = yscrollbar.set

            # Grid elements
            text.grid(row=0, column=0, sticky="W E N S")
            yscrollbar.grid(column=1, row=0, sticky="N S")

            text.config(state=tk.DISABLED)
