from typing import List

from hms_framework.interfaces.application.logger_service import LoggerService


class LoggerComposite(LoggerService):

    def __init__(self) -> None:
        self._children: List[LoggerService] = []

    def add(self, logger_service: LoggerService) -> None:
        self._children.append(logger_service)
        logger_service.parent = self

    def remove(self, logger_service: LoggerService) -> None:
        self._children.remove(logger_service)
        logger_service.parent = None

    @staticmethod
    def is_composite() -> bool:
        return True

    def log(self, type_name, message):
        results = []
        for child in self._children:
            results.append(child.log(type_name, message))
