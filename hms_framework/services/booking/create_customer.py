from hms_framework.interfaces.patterns.command import Command
from hms_framework.value_object.booking.create_customer_request import CreateCustomerRequest
from hms_framework.value_object.booking.create_customer_response import CreateCustomerResponse


class CreateCustomer(Command):

    def __init__(self, customer_model, address_model, country_model, city_model):
        self.customer_model = customer_model
        self.address_model = address_model
        self.country_model = country_model
        self.city_model = city_model

    def execute(self, create_customer_request: CreateCustomerRequest):
        customer = self.customer_model()
        customer.first_name = create_customer_request.customer_first_name
        customer.last_name = create_customer_request.customer_last_name
        customer.telephone = create_customer_request.customer_telephone
        customer.email = create_customer_request.customer_email

        address = self.address_model()
        address.house_number = create_customer_request.address_house_number
        address.street = create_customer_request.address_street
        address.postal_code = create_customer_request.address_postal_code
        city_id = create_customer_request.address_city_id
        address.city = self.city_model.objects.get(pk=city_id)
        country_id = create_customer_request.address_country_id
        address.country = self.country_model.objects.get(pk=country_id)
        address.created_by_id = create_customer_request.created_by_user_id
        address.save()

        customer.address = address
        customer.created_by_id = create_customer_request.created_by_user_id
        customer.save()

        return CreateCustomerResponse(
            customer=customer
        )
