import datetime

from hms_framework.interfaces.patterns.command import Command
from hms_framework.value_object.financial.build_invoice_request import BuildInvoiceRequest
from hms_framework.value_object.financial.build_invoice_response import BuildInvoiceResponse


class BuildInvoice(Command):

    def __init__(self, booking_model, invoice_model, invoice_item_model, user_model, invoice_payment_model):
        self.booking_model = booking_model
        self.invoice_model = invoice_model
        self.invoice_item_model = invoice_item_model
        self.user_model = user_model
        self.invoice_payment_model = invoice_payment_model

    def execute(self, build_invoice_request: BuildInvoiceRequest):
        booking = self.booking_model.objects.get(pk=build_invoice_request.booking_id)

        try:
            invoice = self.invoice_model.objects.get(customer_id=booking.customer.id)
            invoice_items = self.invoice_item_model.objects.filter(invoice=invoice.id)
        except self.invoice_model.DoesNotExist:
            invoice = self.invoice_model()
            invoice.customer = booking.customer
            invoice.due_date = datetime.datetime.now()
            invoice.is_deleted = False
            invoice.created_by = self.user_model.objects.get(pk=build_invoice_request.created_by_user_id)
            invoice.save()

            invoice_item = self.invoice_item_model()
            invoice_item.amount = booking.total_amount
            invoice_item.description = str(booking.room) + ' (' + booking.date_from.strftime(
                '%d/%m/%Y') + ' to ' + booking.date_to.strftime('%d/%m/%Y') + ')'
            invoice_item.discount = 0
            invoice_item.invoice = invoice
            invoice_item.created_by_id = build_invoice_request.created_by_user_id
            invoice_item.save()
            invoice = self.invoice_model.objects.get(customer_id=booking.customer.id)
            invoice_items = self.invoice_item_model.objects.filter(invoice_id=invoice.id)

        try:
            invoice_payments = self.invoice_payment_model.objects.filter(invoice=invoice)
        except self.invoice_payment_model.DoesNotExist:
            invoice_payments = None

        return BuildInvoiceResponse(
            booking=booking,
            invoice=invoice,
            invoice_items=invoice_items,
            invoice_payments=invoice_payments
        )