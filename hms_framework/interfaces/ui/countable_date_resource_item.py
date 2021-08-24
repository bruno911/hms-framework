from abc import ABC, abstractmethod
from datetime import datetime


class CountableDateResourceItem(ABC):
    date: datetime
    count: int

    def __init__(self, date, count):
        self.date = date
        self.count = count
