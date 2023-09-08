# library imports
import tkinter as tk
from tkinter import ttk

# local imports
from .toolbar import Toolbar
from .searchtemplate import Search

class MainWindow(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.toolbar = Toolbar(self)
        self.toolbar.pack(side="top", fill="x")

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(padx=4, pady=4, expand=True, fill='both')
        self.notebook.parent = self

        #Customers tab
        self.customersearch = Search(self.notebook, {
            "name": "Customer",
            "dbname": "customers"
        })
        self.customersearch.pack(expand=True, fill='both')
        self.notebook.add(self.customersearch, text="Customers")

        #Vehicles tab
        self.vehiclesearch = Search(self.notebook, {
            "name": "Vehicle",
            "dbname": "vehicles"
        })
        self.vehiclesearch.pack(expand=True, fill='both')
        self.notebook.add(self.vehiclesearch, text="Vehicles")

        #Jobs tab
        self.jobsearch = Search(self.notebook, {
            "name": "Job",
            "dbname": "jobs"
        })
        self.jobsearch.pack(expand=True, fill='both')
        self.notebook.add(self.jobsearch, text="Jobs")

