import tkinter as tk

class ClearableEntry(tk.Frame):
    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        # magic to recreate a tk.entry border
        self.border_frame1 = tk.Frame(self, bg='gray', bd=0)
        self.border_frame1.pack(fill=tk.BOTH, expand=True)
        self.border_frame = tk.Frame(self.border_frame1, bd=0, bg='white')
        self.border_frame.pack(fill=tk.BOTH, expand=True, padx=(1, 0), pady=(1, 0))

        self.entry = tk.Entry(self.border_frame, borderwidth=0, **kwargs)
        self.entry.grid(row=0, column=0, sticky="nsew", padx=(1, 0), pady=0)
        self.clear_button = tk.Label(self.border_frame, text='✕', bg='white', fg='black', cursor='hand2')
        self.clear_button.grid(row=0, column=1, sticky="nsew", padx=(0, 1), pady=(1, 1))
        self.border_frame.grid_columnconfigure(0, weight=1)
        self.border_frame.grid_rowconfigure(0, weight=1)
        self.clear_button.bind('<Button-1>', self._clear_text)
        self.clear_button.bind('<Enter>', self._on_hover)
        self.clear_button.bind('<Leave>', self._on_leave)

        # map bindings from tk.Entry to "self" to behave like an entry
        self.bind = self.entry.bind
        self.get = self.entry.get
        self.delete = self.entry.delete
        self.insert = self.entry.insert
        self.configure = self.entry.configure
        self.cget = self.entry.cget
        self.config = self.entry.config
        self.focus_set = self.entry.focus_set
        self.focus_get = self.entry.focus_get
        self.selection_range = self.entry.selection_range
        self.selection_clear = self.entry.selection_clear


    def _clear_text(self, event=None):
        self.entry.delete(0, tk.END)

    def _on_hover(self, event=None):
        self.clear_button.config(bg='lightgrey')

    def _on_leave(self, event=None):
        self.clear_button.config(bg='white')
