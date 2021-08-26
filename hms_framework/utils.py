import importlib
from datetime import datetime, timedelta


class TimeDiff:

    def __init__(self):
        self.start = datetime.now()
        self._step = self.start
        self.end = self.start

    @property
    def stop(self, ):
        self.end = datetime.now()
        diff = self.end - self.start
        return diff

    @property
    def step(self):
        old_step = self._step
        self._step = datetime.now()
        diff = self._step - old_step
        return diff

    def print_stop(self):
        print(self.stop)

    def print_step(self):
        print(self.step)


def date_range(start_date, end_date):
    for n in range(0, int((end_date - start_date).days) + 1):
        yield start_date + timedelta(n)


def class_for_name(module_name, class_name):
    m = importlib.import_module(module_name)
    c = getattr(m, class_name)
    return c
