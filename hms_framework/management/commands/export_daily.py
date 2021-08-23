import datetime

from django.core.management.base import BaseCommand

from hms_framework.factory import CustomerFactory, InvoiceFactory
from hms_framework.services.exports.export_to_pdf import ExportToPdf
from hms_framework.settings import logger_composite


class Command(BaseCommand):

    def handle(self, *args, **options):

        new_customers = CustomerFactory().create_model().objects.filter(
            created_datetime__gt=datetime.datetime.now() - datetime.timedelta(days=1)
        )

        for new_customer in new_customers:
            new_customer.accept(visitor=ExportToPdf())

        new_invoices = InvoiceFactory().create_model().objects.filter(
            created_datetime__gt=datetime.datetime.now() - datetime.timedelta(days=1)
        )

        for new_invoice in new_invoices:
            new_invoice.accept(visitor=ExportToPdf())

        self.email_files()

        logger_composite.log('INFO', f'Export has successfully exported {len(new_invoices)} invoices'
                                     f' and {len(new_customers)} customers')

    @staticmethod
    def email_files():
        print('Files have been emailed.')
