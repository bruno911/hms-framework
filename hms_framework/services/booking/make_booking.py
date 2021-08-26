from hms_framework.interfaces.patterns.command import Command
from hms_framework.models import Booking, Room, Customer


class MakeBooking(Command):

    def __init__(self, booking_model, room_model, customer_model, user_model):
        self.booking_model = booking_model
        self.room_model = room_model
        self.customer_model = customer_model
        self.user_model = user_model

    def execute(self, room_id, customer_id, date_from, date_to, created_by_user_id):
        booking = self.booking_model()
        booking.room = self.room_model.objects.get(pk=room_id)
        booking.customer = self.customer_model.objects.get(pk=customer_id)
        booking.date_from = date_from
        booking.date_to = date_to
        booking.created_by = self.user_model.objects.get(pk=created_by_user_id)
        booking.save()
        return booking
