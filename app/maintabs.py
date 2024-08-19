from .components.searchtemplate import *

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

class JobSearch(SearchTemplate):
    def __init__(self, parent):
        super().__init__(parent, {"name": "Job","dbname": "jobs"})
        self.init_context_menu({
            "Customer details": self.show_customer,
            "Vehicle details": self.show_vehicle
        })

    def show_customer(self):
        selected_entry = self.get_selected_item()
        if selected_entry is not None:
            customer = self.parent.parent.customersearch
            vx = sql.id_vehicle(selected_entry.vehicle_id)
            cx = sql.id_customer(vx.customer_id)
            customer.edit_item(cx)

    def show_vehicle(self):
        selected_entry = self.get_selected_item()
        if selected_entry is not None:
            vehicle = self.parent.parent.vehiclesearch
            vx = sql.id_vehicle(selected_entry.vehicle_id)
            vehicle.edit_item(vx)
            