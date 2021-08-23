from hms_framework.interfaces.patterns.command import Command
from hms_framework.services.application.interceptors.measure_loading_time_interceptor import \
    measure_loading_time_interceptor


class MarkPayment(Command):

    def __init__(self, invoice_model, user_model, invoice_payment_model):
        self.invoice_model = invoice_model
        self.user_model = user_model
        self.invoice_payment_model = invoice_payment_model

    @measure_loading_time_interceptor
    def execute(self, invoice_id, payment_type, created_by_user_id):
        invoice_payment = self.invoice_payment_model()
        invoice_payment.invoice = self.invoice_model.objects.get(pk=int(invoice_id))
        invoice_payment.amount = invoice_payment.invoice.invoice_items_total()
        invoice_payment.payment_type = payment_type
        invoice_payment.created_by = self.user_model.objects.get(pk=created_by_user_id)
        invoice_payment.save()
