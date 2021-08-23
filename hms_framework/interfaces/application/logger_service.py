from abc import ABC, abstractmethod


class LoggerService(ABC):

    @abstractmethod
    def log(self, type_name, message):
        pass
