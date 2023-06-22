
from .utility.sql import SQLConnection

from .utility.types import Vehicle
from .textwithvar import TextWithVar
from .autocompleteentry import AutocompleteEntry

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


sql = SQLConnection()



class VehicleSearch(tk.Frame):
    def __init__(self, parent, entries_per_page=20):
        super().__init__(parent)
        self.parent = parent

        self.entries_per_page = entries_per_page
        self.page_number = 1
        self.entries = []

        search_frame = tk.Frame(self)
        search_frame.pack(fill=tk.X, pady=10)

        search_label = tk.Label(search_frame, text="Search:")
        search_label.pack(pady=10, padx=10, side=tk.LEFT)

        # Search Entry
        self.search_entry = tk.Entry(search_frame)
        self.search_entry.size()
        self.search_entry.pack(pady=10, padx=20, side=tk.LEFT, expand=True, fill=tk.X)
        # self.search_entry.bind("<KeyRelease>", self.load_entries)
        self.search_entry.bind("<Return>", self.load_entries)

        # New vehicle button
        self.new_vehicle_button = tk.Button(search_frame, text="New Vehicle", command=self.edit_vehicle)
        self.new_vehicle_button.pack(pady=10, padx=20, side=tk.RIGHT)

        # search button
        self.new_vehicle_button = tk.Button(search_frame, text="Search", command=self.load_entries)
        self.new_vehicle_button.pack(pady=10, padx=20, side=tk.RIGHT)

        # Treeview
        self.treeview = ttk.Treeview(self)
        self.treeview.pack(expand=True, fill=tk.BOTH)
        # self.treeview.bind("<<TreeviewSelect>>", self.on_select)
        self.treeview.bind("<Double-1>", self.on_select)

        self.treeview['columns'] = ('id', 'customer_id', 'year', 'make', 'model', 'vin', 'notes')

        self.treeview.column("#0", width=0, stretch=tk.NO)
        self.treeview.column("id", width=0, stretch=tk.NO)
        self.treeview.column("customer_id", anchor=tk.W)
        self.treeview.column("year", anchor=tk.W)
        self.treeview.column("make", anchor=tk.W)
        self.treeview.column("model", anchor=tk.W)
        self.treeview.column("vin", anchor=tk.W)
        self.treeview.column("notes", anchor=tk.W)

        self.treeview.heading("id", text="ID")
        self.treeview.heading("customer_id", text="Customer")
        self.treeview.heading("year", text="Year")
        self.treeview.heading("make", text="Make")
        self.treeview.heading("model", text="Model")
        self.treeview.heading("vin", text="VIN")
        self.treeview.heading("notes", text="Notes")

        self.isLoading = False
        self.load_entries()

    #@debounce(wait_time=1)
    def load_entries(self, *args):
        if self.isLoading == False:
            self.isLoading = True
            search_text = self.search_entry.get()
            self.entries = sql.search_vehicles(text=search_text, page=self.page_number, page_size=self.entries_per_page)

            self.update_treeview()

            self.isLoading = False

    def update_treeview(self):
        self.treeview.delete(*self.treeview.get_children())

        counter = 0
        for entry in self.entries:
            self.treeview.insert("", tk.END, values=entry.to_tuple(), iid=counter)
            counter += 1

    def on_select(self, event):
        selected_item = self.treeview.focus()

        if selected_item:
            selected_index = int(selected_item)
            selected_entry = self.entries[selected_index]
            self.edit_vehicle(selected_entry)

    def edit_vehicle(self, entry=None):
        new_window = tk.Toplevel(self)
        new_window.title("Vehicle Info")
        ev = EditVehicle(new_window, entry, self.load_entries).pack(expand=True, fill=tk.BOTH)

class EditVehicle(tk.Frame):
    def __init__(self, parent, entry=None, update_list=None):
        super().__init__(parent)
        self.parent = parent
        self.entry = entry
        self.update_list = update_list
        if self.update_list is None:
            self.update_list = lambda: None

        self.newentry = False
        if self.entry is None:
            self.entry = Vehicle()
            self.newentry = True

        self.create_widgets()
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(6, weight=1)
        self.parent.minsize(300, 300)

        self.parent.protocol("WM_DELETE_WINDOW", self.close_window)

    def create_widgets(self):
        if self.entry.id != '':
            # Delete Button in Menu
            self.menu_bar = tk.Menu(self.parent)
            self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
            self.menu_bar.add_cascade(label="File", menu=self.file_menu)

            self.file_menu.add_command(label="X Delete Vehicle X", command=self.delete_entry)
            self.parent.config(menu=self.menu_bar)

        # Customer ID
        self.customer_id_label = tk.Label(self, text="Customer:")
        self.customer_id_label.grid(row=0, column=0, sticky="e")
        self.customer_id_var = tk.StringVar()
        #self.customer_id_entry = tk.Entry(self, textvariable=self.customer_id_var)
        self.customer_id_entry = CustomerIDSuggestEntry(self, textvariable=self.customer_id_var)
        self.customer_id_entry.grid(row=0, column=1, sticky="ew", columnspan=2)

        # Year
        self.year_label = tk.Label(self, text="Year:")
        self.year_label.grid(row=1, column=0, sticky="e")
        self.year_var = tk.StringVar()
        self.year_entry = tk.Entry(self, textvariable=self.year_var)
        self.year_entry.grid(row=1, column=1, sticky="ew", columnspan=2)

        # Make
        self.make_label = tk.Label(self, text="Make:")
        self.make_label.grid(row=2, column=0, sticky="e")
        self.make_var = tk.StringVar()
        self.make_entry = tk.Entry(self, textvariable=self.make_var)
        self.make_entry.grid(row=2, column=1, sticky="ew", columnspan=2)

        # Model
        self.model_label = tk.Label(self, text="Model:")
        self.model_label.grid(row=3, column=0, sticky="e")
        self.model_var = tk.StringVar()
        self.model_entry = tk.Entry(self, textvariable=self.model_var)
        self.model_entry.grid(row=3, column=1, sticky="ew", columnspan=2)

        # VIN
        self.vin_label = tk.Label(self, text="VIN:")
        self.vin_label.grid(row=4, column=0, sticky="e")
        self.vin_var = tk.StringVar()
        self.vin_entry = tk.Entry(self, textvariable=self.vin_var)
        self.vin_entry.grid(row=4, column=1, sticky="ew", columnspan=2)

        # Notes
        self.sb = tk.Scrollbar(self, orient=tk.VERTICAL)
        self.sb.grid(row=5, column=3, sticky="nse")

        self.notes_label = tk.Label(self, text="Notes:")
        self.notes_label.grid(row=5, column=0, sticky="ne")
        self.notes_var = tk.StringVar()
        self.notes_entry = TextWithVar(self, textvariable=self.notes_var, yscrollcommand=self.sb.set)
        self.sb.config(command=self.notes_entry.yview)
        self.notes_entry.grid(row=5, column=1, sticky="nsew", columnspan=2)

        # Save Button
        self.save_button = tk.Button(self, text="Save", command=self.save_info)
        self.save_button.grid(row=6, column=1, pady=10, padx=10)

        # Cancel Button
        self.cancel_button = tk.Button(self, text="Cancel", command=self.close_window)
        self.cancel_button.grid(row=6, column=2, pady=10, padx=10)

        self.fill_entries()
        
        if self.newentry:
            self.customer_id_entry.focus()

    def save_info(self):
        self.entry.customer_id = ''

        if self.customer_id_entry.selected is not None:
            link = sql.id_customer(self.customer_id_entry.selected.id)
            if link is not None and len(link) > 0:
                link = link[0]
                self.entry.customer_id = link.id

        self.entry.year = self.year_var.get()
        self.entry.make = self.make_var.get()
        self.entry.model = self.model_var.get()
        self.entry.vin = self.vin_var.get()
        self.entry.notes = self.notes_var.get()

        self.entry.save()

        self.close_window(force=True)

    def has_changed(self):
        if (
            #self.entry.customer_id != self.customer_id_var.get()
            str(self.entry.year) != self.year_var.get()
            or self.entry.make != self.make_var.get()
            or self.entry.model != self.model_var.get()
            or self.entry.vin != self.vin_var.get()
            or self.entry.notes != self.notes_var.get()
        ):
            return True
        else:
            return False

    def close_window(self, force=False):
        if self.has_changed() and force == False:
            result = messagebox.askyesno("Discard Changes", "You have unsaved changes. YES = Close without saving")
            
            if result:
                #self.entry.delete()
                self.close()
            else:
                self.focus()
        else:
            self.close()

    def close(self):
        self.parent.destroy()
        self.update_list()

    def delete_entry(self):
        result = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this Vehicle?")

        if result:
            self.entry.delete()
            self.close_window()
        else:
            self.focus()
            pass

    def fill_entries(self):
        self.customer_id_var.set(self.entry.customer_id)

        if self.entry.customer_id != '':
            #update customer field if customer_id is present
            link = sql.id_customer(self.entry.customer_id)
            if link is not None and len(link) > 0:
                link = link[0]
                self.customer_id_var.set(link.__str__())
                self.customer_id_entry.selected = link

        self.year_var.set(self.entry.year)
        self.make_var.set(self.entry.make)
        self.model_var.set(self.entry.model)
        self.vin_var.set(self.entry.vin)
        self.notes_var.set(self.entry.notes)
        self.notes_entry.update_textvariable()


class CustomerIDSuggestEntry(AutocompleteEntry):
    def __init__(self, *args, **kwargs):
        super().__init__([], *args, **kwargs)

    def comparison(self): 
        search_text = self.var.get()
        return sql.search_customers(search_text, 1, 8)
    
