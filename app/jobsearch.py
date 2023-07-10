
from .utility.sql import SQLConnection

from .utility.types import Job
from .utility.types import COLUMN_INITIAL_WIDTH
from .textwithvar import TextWithVar
from .autocompleteentry import AutocompleteEntry

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


sql = SQLConnection()


class JobSearch(tk.Frame):
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
        #self.search_entry.bind("<KeyRelease>", self.load_entries)
        self.search_entry.bind("<Return>", self.load_entries)

        # New job button
        self.new_job_button = tk.Button(search_frame, text="New Job", command=self.edit_job)
        self.new_job_button.pack(pady=10, padx=20, side=tk.RIGHT)

        # search button
        self.new_job_button = tk.Button(search_frame, text="Search", command=self.load_entries)
        self.new_job_button.pack(pady=10, padx=20, side=tk.RIGHT)

        # Treeview
        self.treeview = ttk.Treeview(self)
        self.treeview.pack(expand=True, fill=tk.BOTH)
        #self.treeview.bind("<<TreeviewSelect>>", self.on_select)
        self.treeview.bind("<Double-1>", self.on_select)

        self.treeview['columns'] = ('id', 'vehicle_id', 'description', 'notes', 'cost', 'mileage_in', 'mileage_out')

        self.treeview.column("#0", width=0, stretch=tk.NO)
        self.treeview.column("id", width=0, stretch=tk.NO)
        self.treeview.column("vehicle_id", anchor=tk.W, width=COLUMN_INITIAL_WIDTH)
        self.treeview.column("description", anchor=tk.W, width=COLUMN_INITIAL_WIDTH)
        self.treeview.column("notes", anchor=tk.W, width=COLUMN_INITIAL_WIDTH)
        self.treeview.column("cost", anchor=tk.W, width=COLUMN_INITIAL_WIDTH)
        self.treeview.column("mileage_in", anchor=tk.W, width=COLUMN_INITIAL_WIDTH)
        self.treeview.column("mileage_out", anchor=tk.W, width=COLUMN_INITIAL_WIDTH)

        self.treeview.heading("id", text="ID")
        self.treeview.heading("vehicle_id", text="Vehicle")
        self.treeview.heading("description", text="Description")
        self.treeview.heading("notes", text="Notes")
        self.treeview.heading("cost", text="Cost")
        self.treeview.heading("mileage_in", text="Mileage In")
        self.treeview.heading("mileage_out", text="Mileage Out")

        self.isLoading = False
        self.load_entries()

    #@debounce(wait_time=1)
    def load_entries(self, *args):
        if self.isLoading == False:
            self.isLoading = True
            search_text = self.search_entry.get()
            self.entries = sql.search_jobs(text=search_text, page=self.page_number, page_size=self.entries_per_page)

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
            self.edit_job(selected_entry)

    def edit_job(self, entry=None):
        new_window = tk.Toplevel(self)
        new_window.title("Job Info")
        ej = EditJob(new_window, entry, self.load_entries).pack(expand=True, fill=tk.BOTH)

class EditJob(tk.Frame):
    def __init__(self, parent, entry=None, update_list=None):
        super().__init__(parent)
        self.parent = parent
        self.entry = entry
        self.update_list = update_list
        if self.update_list is None:
            self.update_list = lambda: None

        self.newentry = False
        if self.entry is None:
            self.entry = Job()
            self.newentry = True

        self.create_widgets()
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(5, weight=1)
        self.parent.minsize(300, 300)

        self.parent.protocol("WM_DELETE_WINDOW", self.close_window)

    def create_widgets(self):
        if self.entry.id != '':
            # Delete Button in Menu
            self.menu_bar = tk.Menu(self.parent)
            self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
            self.menu_bar.add_cascade(label="File", menu=self.file_menu)

            self.file_menu.add_command(label="X Delete Job X", command=self.delete_entry)
            self.parent.config(menu=self.menu_bar)

        # Vehicle ID
        self.vehicle_id_label = tk.Label(self, text="Vehicle ID:")
        self.vehicle_id_label.grid(row=0, column=0, sticky="e")
        self.vehicle_id_var = tk.StringVar()
        #self.vehicle_id_entry = tk.Entry(self, textvariable=self.vehicle_id_var)
        self.vehicle_id_entry = VehicleIDSuggestEntry(self, textvariable=self.vehicle_id_var)
        self.vehicle_id_entry.grid(row=0, column=1, sticky="ew", columnspan=2)

        # Description
        self.description_label = tk.Label(self, text="Description:")
        self.description_label.grid(row=1, column=0, sticky="e")
        self.description_var = tk.StringVar()
        self.description_entry = tk.Entry(self, textvariable=self.description_var)
        self.description_entry.grid(row=1, column=1, sticky="ew", columnspan=2)

        # Notes
        self.sb = tk.Scrollbar(self, orient=tk.VERTICAL)
        self.sb.grid(row=2, column=3, sticky="nse")

        self.notes_label = tk.Label(self, text="Notes:")
        self.notes_label.grid(row=2, column=0, sticky="ne")
        self.notes_var = tk.StringVar()
        self.notes_entry = TextWithVar(self, textvariable=self.notes_var, yscrollcommand=self.sb.set)
        self.sb.config(command=self.notes_entry.yview)
        self.notes_entry.grid(row=2, column=1, sticky="nsew", columnspan=2)

        # Cost
        self.cost_label = tk.Label(self, text="Cost:")
        self.cost_label.grid(row=3, column=0, sticky="e")
        self.cost_var = tk.StringVar()
        self.cost_entry = tk.Entry(self, textvariable=self.cost_var)
        self.cost_entry.grid(row=3, column=1, sticky="ew", columnspan=2)

        # Mileage In
        self.mileage_in_label = tk.Label(self, text="Mileage In:")
        self.mileage_in_label.grid(row=4, column=0, sticky="e")
        self.mileage_in_var = tk.StringVar()
        self.mileage_in_entry = tk.Entry(self, textvariable=self.mileage_in_var)
        self.mileage_in_entry.grid(row=4, column=1, sticky="ew", columnspan=2)

        # Mileage Out
        self.mileage_out_label = tk.Label(self, text="Mileage Out:")
        self.mileage_out_label.grid(row=5, column=0, sticky="e")
        self.mileage_out_var = tk.StringVar()
        self.mileage_out_entry = tk.Entry(self, textvariable=self.mileage_out_var)
        self.mileage_out_entry.grid(row=5, column=1, sticky="ew", columnspan=2)

        # Save Button
        self.save_button = tk.Button(self, text="Save", command=self.save_info)
        self.save_button.grid(row=6, column=1, pady=10, padx=10)

        # Cancel Button
        self.cancel_button = tk.Button(self, text="Cancel", command=self.close_window)
        self.cancel_button.grid(row=6, column=2, pady=10, padx=10)

        self.fill_entries()
        
        if self.newentry:
            self.vehicle_id_entry.focus()

    def save_info(self):
        #self.entry.vehicle_id = self.vehicle_id_var.get()
        self.entry.vehicle_id = ''

        if self.vehicle_id_entry.selected is not None:
            link = sql.id_vehicle(self.vehicle_id_entry.selected.id)
            if link is not None:
                self.entry.vehicle_id = link.id

        self.entry.description = self.description_var.get()
        self.entry.notes = self.notes_var.get()
        self.entry.cost = self.cost_var.get()
        self.entry.mileage_in = self.mileage_in_var.get()
        self.entry.mileage_out = self.mileage_out_var.get()

        self.entry.save()

        self.close_window(force=True)

    def vx_id_changed(self):
        if hasattr(self, 'vehicle_link'):
            return self.vehicle_link.__str__() != self.vehicle_id_var.get()
        else:
            return self.vehicle_id_var.get() != ''
        
    def has_changed(self):
        if (
            #self.entry.vehicle_id != self.vehicle_id_var.get() or
            self.vx_id_changed() or
            self.entry.description != self.description_var.get() or
            self.entry.notes != self.notes_var.get() or
            str(self.entry.cost) != self.cost_var.get() or
            self.entry.mileage_in != self.mileage_in_var.get() or
            self.entry.mileage_out != self.mileage_out_var.get()
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
        result = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this Job?")

        if result:
            self.entry.delete()
            self.close_window()
        else:
            self.focus()
            pass

    def fill_entries(self):
        self.vehicle_id_var.set(self.entry.vehicle_id)

        if self.entry.vehicle_id != '':
            #update vehicle field if vehicle_id is present
            link = sql.id_vehicle(self.entry.vehicle_id)
            if link is not None:
                self.vehicle_id_var.set(link.__str__())
                self.vehicle_id_entry.selected = link
                self.vehicle_link = link

        self.description_var.set(self.entry.description)
        self.notes_var.set(self.entry.notes)
        self.cost_var.set(self.entry.cost)
        self.mileage_in_var.set(self.entry.mileage_in)
        self.mileage_out_var.set(self.entry.mileage_out)
        self.notes_entry.update_textvariable()


class VehicleIDSuggestEntry(AutocompleteEntry):
    def __init__(self, *args, **kwargs):
        super().__init__([], *args, **kwargs)

    def comparison(self): 
        search_text = self.var.get()
        return sql.search_vehicles(search_text, 1, 8)
    
