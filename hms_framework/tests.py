import datetime

import pytest
from django.contrib.auth.models import User
from django.test import TestCase

# Create your tests here.
from hms_framework.factory import CustomerFactory, BookingFactory, RoomFactory
from hms_framework.models import Customer, Address, Country, City, Invoice, InvoiceItem, Room, Booking, CustomerMemento
from hms_framework.value_object.booking.create_customer_request import CreateCustomerRequest


class TestModels(TestCase):

    @pytest.mark.django_db(transaction=True)
    def test_customer_model_creates_properly(self):

        country = Country()
        country.name = "Ireland"
        country.save()

        city = City()
        city.name = "Limerick"
        city.country = country
        city.save()

        customer = Customer()
        customer.first_name = "first_name"
        customer.last_name = "last_name"
        customer.telephone = "+123456789"
        customer.email = "test@test.com"

        address = Address()
        address.house_number = "1"
        address.street = "street"
        address.postal_code = "postal_code"
        city_id = "1"
        address.city = City.objects.get(pk=city_id)
        country_id = "1"
        address.country = Country.objects.get(pk=country_id)
        address.created_by_id = 1
        address.save()

        customer.address = address
        customer.created_by_id = 1
        customer.save()

        assert customer.pk > 0
        assert customer.__str__()

        assert country.name == "Ireland"
        assert city.name == "Limerick"

        assert customer.first_name == "first_name"
        assert customer.last_name == "last_name"
        assert customer.telephone == "+123456789"
        assert customer.email == "test@test.com"

        assert address.house_number == "1"
        assert address.street == "street"
        assert address.postal_code == "postal_code"

        assert customer.address == address

        customer.delete()
        address.delete()
        city.delete()
        country.delete()

    @pytest.mark.django_db(transaction=True)
    def test_invoice_model_creates_properly(self):

        # Set up data.
        country = Country()
        country.name = "Ireland"
        country.save()

        city = City()
        city.name = "Limerick"
        city.country = country
        city.save()

        customer = Customer()
        customer.first_name = "first_name"
        customer.last_name = "last_name"
        customer.telephone = "+123456789"
        customer.email = "test@test.com"

        address = Address()
        address.house_number = "1"
        address.street = "street"
        address.postal_code = "postal_code"
        city_id = "1"
        address.city = City.objects.get(pk=city_id)
        country_id = "1"
        address.country = Country.objects.get(pk=country_id)
        address.created_by_id = 1
        address.save()

        customer.address = address
        customer.created_by_id = 1
        customer.save()

        # Actual Test
        invoice = Invoice()
        invoice.customer = customer
        last_now = datetime.datetime.now()
        invoice.due_date = last_now
        invoice.is_deleted = False
        user = User()
        user.username = '123'
        user.save()

        invoice.created_by = user
        invoice.save()

        invoice_item = InvoiceItem()
        invoice_item.amount = 111
        invoice_item.description = "test invoice"
        invoice_item.discount = 4
        invoice_item.invoice = invoice
        invoice_item.created_by_id = 1
        invoice_item.save()

        assert invoice.pk > 0
        assert invoice_item.pk > 0

        assert invoice.customer == customer
        assert invoice.due_date.strftime("%y-%m-%d") == last_now.strftime("%y-%m-%d")

        assert invoice_item.amount == 111
        assert invoice_item.description == "test invoice"
        assert invoice_item.discount == 4
        assert invoice_item.invoice == invoice

        invoice_item.delete()
        invoice.delete()
        customer.delete()
        address.delete()
        city.delete()
        country.delete()


class TestFactory(TestCase):

    @pytest.mark.django_db(transaction=True)
    def test_customer_factory(self):
        model = CustomerFactory().create_model()
        assert type(model) == type(Customer)

    @pytest.mark.django_db(transaction=True)
    def test_booking_factory(self):
        model = BookingFactory().create_model()
        assert type(model) == type(Booking)

    @pytest.mark.django_db(transaction=True)
    def test_room_factory(self):
        model = RoomFactory().create_model()
        assert type(model) == type(Room)


class TestCustomerMemento:

    @pytest.mark.django_db(transaction=True)
    def test_modifying_field_saves_and_undo_properly(self, city, user):
        create_customer_request = CreateCustomerRequest(
            customer_first_name='Test 1',
            customer_last_name='Test 2',
            customer_telephone='123456789',
            customer_email='bruno.quintana@gmail.com',
            address_house_number='27',
            address_street='my street',
            address_postal_code='dublin 1',
            address_city_id=city.id,
            address_country_id=city.country.id,
            created_by_user_id=user.id
        )
        create_customer_service = CustomerFactory().create_customer_service()
        create_customer_response = create_customer_service.execute(
            create_customer_request=create_customer_request
        )

        customer_model = CustomerFactory().create_model()
        customer_id = create_customer_response.customer.id
        customer = customer_model.objects.get(pk=customer_id)
        customer.first_name = 'Test modified first name'
        customer.save()

        customer_model.objects.get(pk=customer.pk)
        # Make sure new name saved properly
        assert customer.first_name == 'Test modified first name'

        customer_memento = CustomerMemento.objects.all().first()
        customer.undo(customer_memento=customer_memento)

        customer = customer_model.objects.get(pk=customer.pk)
        # First name should be rolled back to initial value
        assert customer.first_name == 'Test 1'
