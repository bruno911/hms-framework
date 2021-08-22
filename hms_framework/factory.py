from django.contrib.auth.models import User

from hms_framework.interfaces.patterns.model_factory import ModelFactory
from hms_framework.interfaces.patterns.service_factory import ServiceFactory
from hms_framework.models import Customer, Booking, Room, Invoice, InvoiceItem, InvoicePayment
from hms_framework.services.auth.proxy.django_authentication_proxy import DjangoAuthenticationProxy
from hms_framework.services.auth.authenticator import Authenticator
from hms_framework.services.booking.make_booking import MakeBooking
from hms_framework.services.booking.search_availability import SearchAvailability
from hms_framework.services.financial.build_invoice import BuildInvoice


class CustomerFactory(ModelFactory):
    def create_model(self):
        return Customer


class BookingFactory(ModelFactory):
    def create_model(self):
        return Booking

    def make_booking_service(self):
        booking_model = self.create_model()
        room_model = RoomFactory().create_model()
        customer_model = CustomerFactory().create_model()
        service = MakeBooking(
            booking_model=booking_model,
            room_model=room_model,
            customer_model=customer_model
        )
        return service

    def search_availability_service(self):
        service = SearchAvailability(
            room_model=RoomFactory().create_model()
        )
        return service


class RoomFactory(ModelFactory):
    def create_model(self):
        return Room


class AuthFactory(ServiceFactory):
    def create_service(self) -> Authenticator:
        authentication_service = DjangoAuthenticationProxy()
        service = Authenticator(authentication_service=authentication_service)
        return service


class InvoiceFactory(ModelFactory):
    def build_invoice_service(self):
        booking_model = BookingFactory().create_model()
        invoice_model = self.create_model()
        invoice_item_model = InvoiceItemFactory().create_model()
        user_model = UserFactory().create_model()
        invoice_payment_model = InvoicePaymentFactory().create_model()
        service = BuildInvoice(
            booking_model=booking_model,
            invoice_model=invoice_model,
            invoice_item_model=invoice_item_model,
            user_model=user_model,
            invoice_payment_model=invoice_payment_model
        )

        return service

    def create_model(self):
        return Invoice


class InvoiceItemFactory(ModelFactory):
    def create_model(self):
        return InvoiceItem


class InvoicePaymentFactory(ModelFactory):
    def create_model(self):
        return InvoicePayment


class UserFactory(ModelFactory):
    def create_model(self):
        return User
