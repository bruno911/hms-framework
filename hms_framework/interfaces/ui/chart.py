

from abc import ABC, abstractmethod
from hms_framework.interfaces.ui.countable_date_resource import CountableDateResource


class Chart(ABC):

    def __init__(self, countable_date_resources: CountableDateResource):
        self.countable_date_resources = countable_date_resources.items()
        self.dates = []
        self.counts = []
        for countable_date_resource in self.countable_date_resources:
            self.dates.append(countable_date_resource.date.strftime('%Y-%m-%d'))
            self.counts.append(countable_date_resource.count)

    @abstractmethod
    def base64_image(self):
        pass