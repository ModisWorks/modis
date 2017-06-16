class Pipe:
    def __init__(self):
        """Utility to void calls to pipes when the pipe doesnt exist"""

        import tkinter as tk
        import tkinter as ttk

        self.void = None

    def insert(self, *args, **kwargs):
        """For ttk.Treeview"""

        return self.void

    def set(self, *args, **kwargs):
        """For ttk.Label"""

        return self.void

    def add(self, *args, **kwargs):
        """For ttk.Notebook"""

        return self.void

    def forget(self, *args, **kwargs):
        """For ttk.Norebook"""

        return self.void
