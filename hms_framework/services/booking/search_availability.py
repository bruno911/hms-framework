import datetime

from django.db.models import Sum

from hms_framework.interfaces.patterns.command import Command
from hms_framework.models import Room

class SearchAvailability(Command):

    rooms_available = None

    def __init__(self, room_model):
        self.room_model = room_model

    def execute(self,
                room_type,
                number_of_guests,
                date_from,
                date_to) -> Room:

        if self.rooms_available is not None:
            return self.rooms_available

        model = self.room_model

        date_from_obj = datetime.datetime.strptime(date_from, '%Y-%m-%d')
        date_to_obj = datetime.datetime.strptime(date_to, '%Y-%m-%d')

        # ORM
        self.rooms_available = model.objects.filter(
            room_type_id=room_type
        ).annotate(
            total_beds_capacity=Sum('room_beds__people_capacity')
        ).filter(
            total_beds_capacity__gte=number_of_guests
        ).exclude(
            booking__date_from__range=(date_from_obj, date_to_obj),
            booking__date_to__range=(date_from_obj, date_to_obj)
        )

        return self.rooms_available
