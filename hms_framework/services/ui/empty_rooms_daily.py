import datetime
import random
from typing import List

from django.db.models.base import ModelBase

from hms_framework.interfaces.ui.countable_date_resource import CountableDateResource
from hms_framework.interfaces.ui.countable_date_resource_item import CountableDateResourceItem
from hms_framework.utils import date_range


class EmptyRoomsDaily(CountableDateResource):

    def __init__(self, room_model: ModelBase):
        self.room_model = room_model

    def items(self) -> List[CountableDateResourceItem]:

        list_countable_date_resource = []
        today = datetime.datetime.now()

        for single_date in date_range(start_date=today - datetime.timedelta(days=7), end_date=today):
            empty_rooms = random.randint(1, 30)
            list_countable_date_resource.append(
                CountableDateResourceItem(
                    date=single_date,
                    count=empty_rooms
                )
            )

        return list_countable_date_resource
