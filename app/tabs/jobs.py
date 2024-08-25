from ..components.searchtemplate import *

class JobSearch(SearchTemplate):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, {"name": "Job","dbname": "jobs"}, *args, **kwargs)
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
            customer.edit_item(cx, callback=self.load_entries)

    def show_vehicle(self):
        selected_entry = self.get_selected_item()
        if selected_entry is not None:
            vehicle = self.parent.parent.vehiclesearch
            vx = sql.id_vehicle(selected_entry.vehicle_id)
            vehicle.edit_item(vx, callback=self.load_entries)
            