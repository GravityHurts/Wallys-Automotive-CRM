import tkinter as tk
from ..utility import settings
from ..components.scrollableframe import ScrollFrame
from typing import Any

class Settings(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.create_widgets()

    def create_widgets(self):
        self.scrollFrame = ScrollFrame(self)
        
        f = tk.Frame(self.scrollFrame.viewPort)
        save_button = tk.Button(f, text="Save", command=settings.save_settings)
        def l():
            a=0
            for x in settings.config.items():
                a += len(x)
            return a*80
        save_button.pack(side='right', padx=10, pady=(0,l()))
        for section, items in settings.config.items():  # Iterate over sections and their contents
            frame = tk.Frame(f)
            frame.pack()
            section_title = tk.Label(frame, text=section.title(), font=("Helvetica", 12, "bold"))
            section_title.grid(row=0, column=0, sticky='w')
            for idx, (key, value) in enumerate(items.items()):  # Iterate over keys and values within each section
                var = self.create_setting_var(value)
                widget = self.create_widget_for_type(frame, idx, key, var, value)
                if isinstance(widget, tk.Checkbutton):
                    widget.config(command=lambda v=var, sec=section, key=key: self.update_setting(sec, key, v.get()))
                elif isinstance(widget, tk.Entry):
                    widget.bind("<KeyRelease>", lambda e, sec=section, key=key, w=widget: self.update_setting(sec, key, w.get()))
                else:
                    # For non-checkbutton widgets, ensure the command is set correctly if needed in subclasses
                    pass
                widget.grid(row=idx + 1, column=2)
        
        f.pack(side='left')
        self.scrollFrame.pack(expand=True)

    def create_setting_var(self, value: Any):
        if isinstance(value, bool):
            return tk.BooleanVar(value=value)
        elif isinstance(value, (int, float)):
            return tk.IntVar() if isinstance(value, int) else tk.DoubleVar()
        else:  # Assume it's a string
            return tk.StringVar(value=str(value))

    def create_widget_for_type(self, parent, idx, key, var, value):
        if isinstance(value, bool):
            checkbox = tk.Checkbutton(parent, text=key, variable=var)
            label = tk.Label(parent, text=key.title())
            label.grid(row=idx + 1, column=0, sticky='w')  # Position the label next to the entry widget
            return checkbox
        elif isinstance(value, (int, float)):
            entry = tk.Entry(parent, width=10)
            entry.insert(0, str(value))
            label = tk.Label(parent, text=key.title())
            label.grid(row=idx + 1, column=0, sticky='w')  # Position the label next to the entry widget
            return entry
        else:  # Assume it's a string
            entry = tk.Entry(parent, width=20) 
            entry.insert(0, str(value))
            label = tk.Label(parent, text=key.title())
            label.grid(row=idx + 1, column=0, sticky='w')  # Position the label next to the entry widget
            return entry

    def update_setting(self, section, key, value):
        settings.config[section.lower()][key.lower()] = value
