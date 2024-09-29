import tkinter as tk
from tkcalendar import DateEntry
from datetime import datetime

datepicker_format = '%Y-%m-%d'
dp_format = 'yyyy-mm-dd'
workorder_date_format = '%y%m%d'

class DateEntryWithInlineCalendar(tk.Frame):
    def __init__(self, master=None, initial_date=None, **kwargs):
        self.var = kwargs.pop('textvariable', None)
        noclear = kwargs.pop('noclear', False)
        super().__init__(master, **kwargs)
        self.master = master
        
        # # Create an Entry widget
        # self.date_entry = tk.Entry(self, width=20)
        # self.date_entry.pack(side=tk.LEFT, padx=(0, 5))
        # self.date_entry.config(state='disabled')

        # Create the DateEntry widget and set it to be hidden initially
        self.cal = DateEntry(self, textvariable=self.var, width=12,
                             background='darkblue', foreground='white', borderwidth=2, date_pattern=dp_format)
        self.cal.pack(padx=10, pady=10, side=tk.LEFT)

        # Create a button to show the calendar
        self.calendar_button = tk.Button(self, text="Today", command=self.today)
        self.calendar_button.pack(side=tk.LEFT, padx=5)

        if not noclear:
            # Create a button to clear the date
            self.calendar_button = tk.Button(self, text="Clear", command=self.clear)
            self.calendar_button.pack(side=tk.LEFT)

        # Set the initial date if provided
        if initial_date:
            self.cal.set_date(initial_date)

    def set_callback(self, cb):
        def c(event):
            cb(self.get_date())
        self.cal.bind("<<DateEntrySelected>>", c)

    def clear(self):
        self.var.set('')

    def today(self):
        self.cal.set_date(datetime.today())

    def get_wo_date(self):
        return self.cal.get_date().strftime(workorder_date_format)
    
    def get_date(self):
        return self.cal.get_date().strftime(datepicker_format)

    def set_date(self, date):
        self.cal.set_date(date)

if __name__ == '__main__':
    root = tk.Tk()
    # Initialize with a specific date, e.g., September 29, 2023
    initial_date = datetime.strptime("2021-09-29", "%Y-%m-%d")
    date_frame = DateEntryWithInlineCalendar(root, initial_date=initial_date)
    date_frame.pack(padx=10, pady=10)

    root.mainloop()
