import datetime

from django.db.models import Sum

from hms_framework.interfaces.patterns.command import Command
from hms_framework.models import Room


# service = SearchAvailability(
#     1,
#     2,
#     '2020-10-12',
#     '2020-10-24',
# )
#
# rooms = service.execute() # 1s
# print(...)
# rooms = service.execute() # 1ms

class SearchAvailability(Command):

    room_type = None
    number_of_guests = None
    date_from = None
    date_to = None
    rooms_available = None

    def __init__(self,
                 room_type,
                 number_of_guests,
                 date_from,
                 date_to):
        self.room_type = room_type
        self.number_of_guests = number_of_guests
        self.date_from = datetime.datetime.strptime(date_from, '%Y-%m-%d')
        self.date_to = datetime.datetime.strptime(date_to, '%Y-%m-%d')

    def execute(self) -> Room:

        if self.rooms_available is not None:
            return self.rooms_available

        model = Room

        # ORM
        self.rooms_available = model.objects.filter(
            room_type_id=self.room_type
        ).annotate(
            total_beds_capacity=Sum('room_beds__people_capacity')
        ).filter(
            total_beds_capacity__gte=self.number_of_guests
        ).exclude(
            booking__date_from__range=(self.date_from, self.date_to),
            booking__date_to__range=(self.date_from, self.date_to)
        )

        return self.rooms_available
