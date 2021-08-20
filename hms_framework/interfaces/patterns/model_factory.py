from abc import ABC, abstractmethod


class ModelFactory(ABC):

    @abstractmethod
    def create_model(self):
        pass
