

class CreateCustomerRequest:

    customer_first_name = ''
    customer_last_name = ''
    customer_telephone = None
    customer_email = ''

    address_house_number = None
    address_street = None
    address_postal_code = None
    address_city_id = None
    address_country_id = None

    created_by_user_id = None

    def __init__(self,
                 customer_first_name,
                 customer_last_name,
                 customer_telephone,
                 customer_email,
                 address_house_number,
                 address_street,
                 address_postal_code,
                 address_city_id,
                 address_country_id,
                 created_by_user_id
                 ):
        self.customer_first_name = customer_first_name
        self.customer_last_name = customer_last_name
        self.customer_telephone = customer_telephone
        self.customer_email = customer_email

        self.address_house_number = address_house_number
        self.address_street = address_street
        self.address_postal_code = address_postal_code
        self.address_city_id = address_city_id
        self.address_country_id = address_country_id

        self.created_by_user_id = created_by_user_id
