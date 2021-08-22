from abc import ABC, abstractmethod
from datetime import datetime


class TemplateDebtCollector(ABC):

    customer = None

    def __init__(self, customer):
        self.customer = customer

    def collect(self):
        self.notify_by_email()
        self.notify_by_sms()
        self.notify_by_postal_address()
        self.notify_by_others()
        self.customer.last_has_debts_notified_datetime = datetime.now()
        self.customer.save()

    @staticmethod
    def notify_by_email():
        print('Notify by email')

    @staticmethod
    def notify_by_sms():
        print('Notify by email')

    @staticmethod
    def notify_by_postal_address():
        print('Notify by email')

    @staticmethod
    def notify_by_others():
        print('Notify by others')
