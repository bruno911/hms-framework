from django.contrib.auth.models import User

from hms_framework.interfaces.patterns.model_factory import ModelFactory
from hms_framework.interfaces.patterns.service_factory import ServiceFactory
from hms_framework.interfaces.ui.chart import Chart
from hms_framework.models import Customer, Booking, Room, Invoice, InvoiceItem, InvoicePayment, Address, Country, City, \
    RoomType
from hms_framework.services.auth.proxy.django_authentication_proxy import DjangoAuthenticationProxy
from hms_framework.services.auth.authenticator import Authenticator
from hms_framework.services.booking.create_customer import CreateCustomer
from hms_framework.services.booking.make_booking import MakeBooking
from hms_framework.services.booking.search_availability import SearchAvailability
from hms_framework.services.financial.build_invoice import BuildInvoice
from hms_framework.services.financial.debt_collector import DebtCollector
from hms_framework.services.financial.mark_payment import MarkPayment
from hms_framework.services.ui.bar_horizontal import BarHorizontal
from hms_framework.services.ui.bar_vertical import BarVertical
from hms_framework.services.ui.empty_rooms_daily import EmptyRoomsDaily
from hms_framework.services.ui.guests_daily import GuestsDaily


class CustomerFactory(ModelFactory):
    def create_model(self):
        return Customer

    def create_customer_service(self):
        service = CreateCustomer(
            customer_model=self.create_model(),
            address_model=AddressFactory().create_model(),
            country_model=CountryFactory().create_model(),
            city_model=CityFactory().create_model()
        )

        return service


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


class RoomTypeFactory(ModelFactory):
    def create_model(self):
        return RoomType


class AddressFactory(ModelFactory):
    def create_model(self):
        return Address


class CountryFactory(ModelFactory):
    def create_model(self):
        return Country


class CityFactory(ModelFactory):
    def create_model(self):
        return City


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

    def mark_payment_service(self):
        invoice_model = self.create_model()
        user_model = UserFactory().create_model()
        invoice_payment_model = InvoicePaymentFactory().create_model()
        service = MarkPayment(
            invoice_model=invoice_model,
            user_model=user_model,
            invoice_payment_model=invoice_payment_model
        )
        return service


class FinancialFactory:
    def debt_collector_service(self, customer):
        service = DebtCollector(customer=customer)
        return service


class UserFactory(ModelFactory):
    def create_model(self):
        return User


class ChartFactory:
    @staticmethod
    def empty_rooms_daily() -> Chart:
        return BarHorizontal(countable_date_resources=EmptyRoomsDaily(
            room_model=RoomFactory().create_model()
        ))

    @staticmethod
    def guests_daily() -> Chart:
        return BarVertical(countable_date_resources=GuestsDaily(
            customer_model=CustomerFactory().create_model()
        ))
