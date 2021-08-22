

class BuildInvoiceRequest:
    booking_id = None
    created_by_user_id = None

    def __init__(self, booking_id, created_by_user_id):
        self.booking_id = booking_id
        self.created_by_user_id = created_by_user_id
