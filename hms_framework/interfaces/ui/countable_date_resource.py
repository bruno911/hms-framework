from abc import ABC, abstractmethod
from typing import List

from hms_framework.interfaces.ui.countable_date_resource_item import CountableDateResourceItem


class CountableDateResource(ABC):

    @abstractmethod
    def items(self) -> List[CountableDateResourceItem]:
        pass


