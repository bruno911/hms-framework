from abc import ABC, abstractmethod


class Visitor(ABC):


    @staticmethod
    @abstractmethod
    def do_it_for_customer(customer):
        pass


    @staticmethod
    @abstractmethod
    def do_it_for_invoice(customer):
        pass