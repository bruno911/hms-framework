from hms_framework.interfaces.patterns.template_debt_collector import TemplateDebtCollector


class DebtCollector(TemplateDebtCollector):

    @staticmethod
    def notify_by_sms():
        print('Disabled sms notification')

    @staticmethod
    def notify_by_others():
        print('Notify by Whatsapp')
