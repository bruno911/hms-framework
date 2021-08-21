from abc import ABC, abstractmethod


class ServiceFactory(ABC):

    @abstractmethod
    def create_service(self):
        pass
