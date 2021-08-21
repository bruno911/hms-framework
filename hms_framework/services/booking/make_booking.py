from django.db.models import Model

from hms_framework.interfaces.patterns.command import Command


class MakeBooking(Command):

    def __init__(self, booking_model: Model, room_model: Model, customer_model: Model):
        self.booking_model = booking_model
        self.room_model = room_model
        self.customer_model = customer_model

    def execute(self, room_id, customer_id, date_from, date_to, created_by_user_id):
        booking = self.booking_model
        booking.room = self.room_model.objects.get(pk=room_id)
        booking.customer = self.customer_model.objects.get(pk=customer_id)
        booking.date_from = date_from
        booking.date_to = date_to
        booking.created_by_id = created_by_user_id
        booking.save()
