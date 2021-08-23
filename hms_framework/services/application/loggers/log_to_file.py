from hms_framework.interfaces.application.logger_service import LoggerService


class LogToFile(LoggerService):

    def log(self, type_name, message):
        print('I am logging to File')
