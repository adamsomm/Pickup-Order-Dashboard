class PickupOrder:
    def __init__(self, unique_id, contact, company, details, pickup_date, titan_number, is_picked_up=False):
        self.unique_id = unique_id
        self.contact = contact
        self.company = company
        self.details = details
        self.pickup_date = pickup_date
        self.titan_number = titan_number
        self.is_picked_up = is_picked_up

    # Getters
    def get_unique_id(self):
        return self.unique_id

    def get_details(self):
        return self.details

    def get_pickup_date(self):
        if not self.pickup_date:
            return "N/A"
        return self.pickup_date.strftime("%d/%b/%Y, %H:%M:%S")

    def get_status(self):
        return self.is_picked_up

    def get_company(self):
        return self.company

    def get_contact(self):
        return self.contact

    def get_titan_number(self):
        return self.titan_number

    # Setters
    def mark_picked_up(self):
        self.is_picked_up = True

    def mark_not_picked_up(self):
        self.is_picked_up = False
