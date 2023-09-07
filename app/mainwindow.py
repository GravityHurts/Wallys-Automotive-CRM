# library imports
import tkinter as tk
from tkinter import ttk

# local imports
from .toolbar import Toolbar
from .customersearch import CustomerSearch
from .vehiclesearch import VehicleSearch
from .jobsearch import JobSearch

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
        self.customersearch = CustomerSearch(self.notebook)
        self.customersearch.pack(expand=True, fill='both')
        self.notebook.add(self.customersearch, text="Customers")

        #Vehicles tab
        self.vehiclesearch = VehicleSearch(self.notebook)
        self.vehiclesearch.pack(expand=True, fill='both')
        self.notebook.add(self.vehiclesearch, text="Vehicles")

        #Jobs tab
        self.jobsearch = JobSearch(self.notebook)
        self.jobsearch.pack(expand=True, fill='both')
        self.notebook.add(self.jobsearch, text="Jobs")

