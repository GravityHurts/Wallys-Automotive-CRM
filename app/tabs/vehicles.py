from ..components.searchtemplate import *

class VehicleSearch(SearchTemplate):
    def __init__(self, parent):
        super().__init__(parent, {"name": "Vehicle","dbname": "vehicles"})
        self.init_context_menu({
            "Customer details": self.show_customer,
            "Show all Jobs for this Vehicle": self.show_all_jobs
        })

    def show_all_jobs(self):
        selected_entry = self.get_selected_item()
        if selected_entry is not None:
            vehicle_id = selected_entry.id
            job = self.parent.parent.jobsearch
            job.search_entry.delete(0, tk.END)
            job.search_entry.insert(0, f'<<vehicle:{vehicle_id}>>')
            self.parent.select(2)
            job.load_entries()

    def show_customer(self):
        selected_entry = self.get_selected_item()
        if selected_entry is not None:
            customer = self.parent.parent.customersearch
            cx = sql.id_customer(selected_entry.customer_id)
            customer.edit_item(cx)