# library imports
import tkinter as tk
from tkinter import ttk

# local imports
from .toolbar import Toolbar
from .customersearch import CustomerSearch

class MainWindow(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.toolbar = Toolbar(parent)
        self.toolbar.pack(side="top", fill="x")

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(pady=10, expand=True)

        #add ttk.notebook here
        self.customersearch = CustomerSearch(self.notebook)
        self.customersearch.pack(expand=True)

        self.notebook.add(self.customersearch, text="Customers")
