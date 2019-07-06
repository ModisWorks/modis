import logging
import tkinter as tk
import tkinter.ttk as ttk
import threading

from modis.tools import data

from github import Github

logger = logging.getLogger(__name__)

githubapi = Github(data.cache["keys"]["github_token"])

# TODO pip requirements listing, installation and uninstallation
# TODO live module refresh

# import subprocess
# import sys
#
# def install(package):
#     subprocess.call([sys.executable, "-m", "pip", "install", package])


class Frame(ttk.Frame):
    """A tab containing tools to install and manage modules."""

    def __init__(self, parent):
        """Create the frame.

        Args:
            parent: A tk or ttk object.
        """

        super(Frame, self).__init__(parent, padding=8)

        # Add elements
        find = self.Find(self)
        info = self.Info(self)
        installed = self.Installed(self)

        # Grid elements
        find.grid(column=0, row=0, padx=8, pady=8, sticky="W E N S")
        info.grid(column=1, row=0, padx=8, pady=8, sticky="W E N S")
        installed.grid(column=2, row=0, padx=8, pady=8, sticky="W E N S")

        # Configure stretch ratios
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(0, weight=1)

    class Find(ttk.LabelFrame):
        """A panel with tools to find modules on GitHub."""

        def __init__(self, parent):
            """Create the frame.

            Args:
                parent: A tk or ttk object.
            """

            super(Frame.Find, self).__init__(parent, padding=8, text="Find new modules")

            # Variables
            self.repo = tk.StringVar(value="Enter or select a GitHub user/organisation")

            # Add elements
            self.name_entry = ttk.Combobox(self, textvariable=self.repo, values=["modisworks", "infraxion"])
            self.scan_button = ttk.Button(self, command=self.scan, text="Scan user/org")
            self.loadingbar = ttk.Progressbar(self)

            self.panel_listing = self.PanelListing(self)

            self.install_button = ttk.Button(self, command=self.install, text="Install")

            # Grid elements
            self.name_entry.grid(column=0, row=0, padx=4, pady=4, sticky="W E N")
            self.scan_button.grid(column=1, row=0, padx=4, pady=4, sticky="E N")
            self.loadingbar.grid(column=0, columnspan=2, row=1, padx=4, pady=4, sticky="W E")

            self.panel_listing.grid(column=0, columnspan=2, row=2, padx=4, pady=4, sticky="W E N S")

            self.install_button.grid(column=1, row=3, padx=4, pady=4, sticky="E S")

            # Configure stretch ratios
            self.columnconfigure(0, weight=1)
            self.columnconfigure(1, weight=0)
            self.rowconfigure(0, weight=0)
            self.rowconfigure(1, weight=0)
            self.rowconfigure(2, weight=1)
            self.rowconfigure(3, weight=0)

        def scan(self):
            """Initiate a GitHub search for the entered user/organisation's repositories."""
            self.loadingbar.start(50)

            self.name_entry.state(statespec=["disabled"])
            self.scan_button.state(statespec=["disabled"])
            self.panel_listing.grid_remove()

            repo_scanner = self.RepoScanner(self.name_entry.get(), self.scan_done)
            repo_scanner.run()

        def scan_done(self, repos):
            """Pass found repos to the repo listing panel.

            Args:
                repos (list): Repos to give to the listing panel.
            """
            self.panel_listing.tree.delete(*self.panel_listing.tree.get_children())
            for repo in repos:
                self.panel_listing.tree.insert("", "end", text=repo.name)

            self.panel_listing.grid()

            self.loadingbar.stop()
            self.loadingbar.configure(value=100)
            self.scan_button.state(statespec=["!disabled"])
            self.name_entry.state(statespec=["!disabled"])

        def install(self):
            """Install the selected module."""
            pass

        class PanelListing(ttk.Frame):
            """Panel listing found repositories for the selected user/organisation."""

            def __init__(self, parent):
                """Create the frame.

                Args:
                    parent: A tk or ttk object.
                """

                super(Frame.Find.PanelListing, self).__init__(parent)

                # Add elements
                self.tree = ttk.Treeview(self, show="tree")
                self.tree.column("#0", width=100)
                yscrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
                self.tree['yscrollcommand'] = yscrollbar.set

                # Grid elements
                self.tree.grid(column=0, row=0, padx=(4, 0), pady=4, sticky="W E N S")
                yscrollbar.grid(column=1, row=0, padx=(0, 4), pady=4, sticky="N S")

                # Configure stretch ratios
                self.columnconfigure(0, weight=1)
                self.columnconfigure(1, weight=0)
                self.rowconfigure(0, weight=1)

        class PanelLoading(ttk.Frame):
            """Panel shown when fetching repos from GitHub"""

            def __init__(self, parent):
                """Create the frame.

                Args:
                    parent: A tk or ttk object.
                """

                super(Frame.Find.PanelLoading, self).__init__(parent)

                # Add elements
                self.spinner = ttk.Progressbar(self)

                # Grid elements
                self.spinner.grid(column=0, row=1, padx=4, pady=4, sticky="W E N S")

                # Configure stretch ratios
                self.columnconfigure(0, weight=1)
                self.rowconfigure(0, weight=1)
                self.rowconfigure(1, weight=0)
                self.rowconfigure(2, weight=1)

        class PanelText(ttk.Frame):
            """Panel shown when """

        class RepoScanner(threading.Thread):
            """Find module repos belonging to the specified user/organisation."""

            def __init__(self, query, after):
                """Create the thread.

                Args:
                    query (str): The user or organisation to search for modules in.
                    after (func): The function to call after completing the search.
                """

                threading.Thread.__init__(self)
                self.query = query
                self.after = after

            def run(self):
                """Start the thread."""

                try:
                    repos = githubapi.get_organization(self.query).get_repos()
                    self.after(repos)
                except:
                    try:
                        repos = githubapi.get_user(self.query).get_repos()
                        self.after(repos)
                    except:
                        # TODO Bad user indicator
                        print("Bad user")

    class Info(ttk.LabelFrame):
        """A panel displaying info about the currently selected module."""

        def __init__(self, parent):
            """Create the frame.

            Args:
                parent: A tk or ttk object.
            """

            super(Frame.Info, self).__init__(parent, padding=8, text="Module info")

    class Installed(ttk.LabelFrame):
        """A panel displaying a list of installed modules along with management controls."""

        def __init__(self, parent):
            """Create the frame.

            Args:
                parent: A tk or ttk object.
            """

            super(Frame.Installed, self).__init__(parent, padding=8, text="Installed modules")
