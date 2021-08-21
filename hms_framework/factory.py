from hms_framework.interfaces.patterns.model_factory import ModelFactory
from hms_framework.interfaces.patterns.service_factory import ServiceFactory
from hms_framework.models import Customer, Booking, Room
from hms_framework.services.auth.proxy.django_authentication_proxy import DjangoAuthenticationProxy
from hms_framework.services.auth.authenticator import Authenticator
from hms_framework.services.booking.make_booking import MakeBooking


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


class RoomFactory(ModelFactory):
    def create_model(self):
        return Room


class AuthFactory(ServiceFactory):
    def create_service(self) -> Authenticator:
        authentication_service = DjangoAuthenticationProxy()
        service = Authenticator(authentication_service=authentication_service)
        return service