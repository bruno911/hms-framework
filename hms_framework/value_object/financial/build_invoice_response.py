

class BuildInvoiceResponse:
    booking = None
    invoice = None
    invoice_items = None
    invoice_payments = None

    def __init__(self, booking, invoice, invoice_items, invoice_payments):
        self.booking = booking
        self.invoice = invoice
        self.invoice_items = invoice_items
        self.invoice_payments = invoice_payments
