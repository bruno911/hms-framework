from hms_framework.interfaces.application.logger_service import LoggerService


class LogToSlack(LoggerService):

    def log(self, type_name, message):
        print('I am logging to Slack')
