from ..components.searchtemplate import *

class CustomerSearch(SearchTemplate):
    def __init__(self, parent):
        super().__init__(parent, {"name": "Customer","dbname": "customers"})
        self.init_context_menu({
            "Show all Vehicles for this Customer": self.show_all_vehicles,
            "Show all Jobs for this Customer": self.show_all_jobs
        })

    def show_all_vehicles(self):
        selected_entry = self.get_selected_item()
        if selected_entry is not None:
            customer_id = selected_entry.id
            vehicle = self.parent.parent.vehiclesearch
            vehicle.search_entry.delete(0, tk.END)
            vehicle.search_entry.insert(0, f'<<customer:{customer_id}>>')
            self.parent.select(1)
            vehicle.load_entries()

    def show_all_jobs(self):
        selected_entry = self.get_selected_item()
        if selected_entry is not None:
            customer_id = selected_entry.id
            job = self.parent.parent.jobsearch
            job.search_entry.delete(0, tk.END)
            job.search_entry.insert(0, f'<<customer:{customer_id}>>')
            self.parent.select(2)
            job.load_entries()