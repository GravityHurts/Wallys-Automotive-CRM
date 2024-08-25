import tkinter as tk
from tkinter import ttk
from tkinter import font


import time

# local imports
from .toolbar import Toolbar
from .tabs.customers import CustomerSearch
from .tabs.vehicles import VehicleSearch
from .tabs.jobs import JobSearch
from .tabs.settings import Settings

class MainWindow(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        win_font = font.nametofont("TkDefaultFont")  # Get default font value into Font object
        line_height = win_font.metrics()['linespace']  # returns an integer
        # self.toolbar = Toolbar(self)
        # self.toolbar.pack(side="top", fill="x")

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(padx=4, pady=4, expand=True, fill='both')
        self.notebook.parent = self
        style = ttk.Style(self.notebook)
        style.configure('Treeview', font=win_font, rowheight=line_height)
        
        # Create loading overlay
        self.create_loading_overlay()

        # Customers tab
        self.customersearch = CustomerSearch(self.notebook, line_height=line_height)
        self.customersearch.pack(expand=True, fill='both')
        self.notebook.add(self.customersearch, text="Customers")

        # Vehicles tab
        self.vehiclesearch = VehicleSearch(self.notebook, line_height=line_height)
        self.vehiclesearch.pack(expand=True, fill='both')
        self.notebook.add(self.vehiclesearch, text="Vehicles")

        # Jobs tab
        self.jobsearch = JobSearch(self.notebook, line_height=line_height)
        self.jobsearch.pack(expand=True, fill='both')
        self.notebook.add(self.jobsearch, text="Jobs")

        # Settings tab
        self.settingstab = Settings(self.notebook)
        self.settingstab.pack(expand=True, fill='both')
        self.notebook.add(self.settingstab, text="Settings")

        self.notebook.bind("<<NotebookTabChanged>>", self.changed)


    def create_loading_overlay(self):
        """Creates the loading overlay with a spinning progress bar."""
        # Set the background color to simulate transparency
        self.loading_overlay = tk.Frame(self, background='')  # Using a semi-transparent color
        self.loading_overlay.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.progress_bar = ttk.Progressbar(self.loading_overlay, mode='indeterminate')
        self.progress_bar.pack(expand=True)

        # Hide overlay initially
        self.hide_loading_overlay()

    def show_loading_overlay(self):
        """Shows the loading overlay."""
        self.loading_overlay.lift()
        self.progress_bar.start(10)  # Start the spinning effect

    def hide_loading_overlay(self):
        """Hides the loading overlay."""
        self.loading_overlay.lower()
        self.progress_bar.stop()

    def changed(self, event):
        """Handles tab changes."""
        a = self.notebook.select()
        if 'settings' not in a:
            self.notebook.nametowidget(self.notebook.select()).search_entry.focus_set()

# Create and start the main application
if __name__ == "__main__":
    root = tk.Tk()
    MainWindow(root).pack(expand=True, fill='both')
    root.mainloop()
