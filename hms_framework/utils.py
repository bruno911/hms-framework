from datetime import datetime


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
