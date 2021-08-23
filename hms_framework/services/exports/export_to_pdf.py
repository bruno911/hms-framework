from hms_framework.interfaces.patterns.visitor import Visitor


class ExportToPdf(Visitor):

    @staticmethod
    def do_it_for_customer(customer):
        print(f'Exporting to PDF for customer: {customer.first_name}')

    @staticmethod
    def do_it_for_invoice(invoice):
        print(f'Exporting to PDF for invoice: {invoice.pk}')
