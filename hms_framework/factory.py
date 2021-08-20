from hms_framework.interfaces.patterns.model_factory import ModelFactory
from hms_framework.models import Customer, Booking, Room


class CustomerFactory(ModelFactory):
    def create_model(self):
        return Customer


class BookingFactory(ModelFactory):
    def create_model(self):

        return Booking


class RoomFactory(ModelFactory):
    def create_model(self):
        return Room
