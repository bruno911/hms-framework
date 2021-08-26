import datetime
import io

import pytest
from PIL import Image
from django.core.files.base import ContentFile
from rest_framework.test import APIClient

from hms_framework.factory import UserFactory
from hms_framework.models import City, Country, Address, Hotel, RoomTypePicture, RoomFeatureType, BedType, RoomType, \
    Room, RoomPricePeriod, Customer, Invoice, InvoiceItem, Booking
from rest_framework.authtoken.models import Token


@pytest.fixture()
def address(country, city, user):
    address = Address.objects.get_or_create(
        house_number='house number 1',
        street='street 1',
        postal_code='D19 X1',
        city=city,
        country=country,
        created_by=user
    )[0]
    return address


@pytest.fixture()
def country():
    country = Country.objects.get_or_create(name='Ireland', phone_prefix='353')[0]
    return country


@pytest.fixture()
def city(country):
    city = City.objects.get_or_create(name='Dublin', country=country)[0]
    return city


@pytest.fixture()
def hotel(address, user):
    hotel = Hotel.objects.get_or_create(
        name='Hotel Test',
        address=address,
        currency_code='EUR',
        created_by=user
    )[0]
    return hotel


@pytest.fixture()
def room_feature_type(user):
    room_feature_type = RoomFeatureType.objects.get_or_create(
        name='Air Condition',
        is_everywhere=True,
        is_active=True,
        created_by=user
    )[0]
    return room_feature_type


@pytest.fixture()
def room_type(user, room_type_picture):
    room_type = RoomType.objects.get_or_create(
        name='Twin Room',
    )[0]
    return room_type


@pytest.fixture()
def room(hotel, room_type, room_feature_type, bed_type, user):
    room = Room.objects.get_or_create(
            hotel=hotel,
            price_night=100,
            price_week=600,
            price_month=2400,
            room_type=room_type,
            description='This is a description',
            room_number=1,
            floor=1,
            square_meters=45,
            created_by=user
        )[0]
    room.room_features.add(room_feature_type)
    room.room_beds.add(bed_type)
    return room


@pytest.fixture()
def bed_type(user):
    bed_type = BedType.objects.get_or_create(
        name='Single Bed',
        people_capacity=1
    )[0]
    return bed_type


@pytest.fixture()
def room_price_period(user, room):
    room_price_period = RoomPricePeriod.objects.get_or_create(
        room=room,
        price_night=100,
        price_week=600,
        price_month=2400,
        valid_date_from=datetime.date(2021, 8, 25),
        valid_date_to=datetime.date(2021, 9, 25),
        valid_type='BOOKING_DATE',
        created_by=user
    )[0]
    return room_price_period


@pytest.fixture()
def customer(user, address):
    customer = Customer.objects.get_or_create(
        first_name='Bruno',
        last_name='Quintana',
        telephone='+353123456789',
        email='public.bq@gmail.com',
        address=address,
        has_debts=False,
        last_has_debts_notified_datetime=None,
        created_by=user
    )[0]
    return customer


@pytest.fixture()
def invoice(user, customer):
    invoice = Invoice.objects.get_or_create(
        customer=customer,
        is_deleted=False,
        created_by=user
    )[0]
    return invoice


@pytest.fixture()
def invoice_item(user, invoice):
    invoice_item = InvoiceItem.objects.get_or_create(
        invoice=invoice,
        description='Double Room - 4 nights',
        amount=200,
        discount=0,
        created_by=user
    )[0]
    return invoice_item


@pytest.fixture()
def booking(room, customer, user, invoice):
    booking = Booking.objects.get_or_create(
        room=room,
        customer=customer,
        date_from=datetime.date(2022, 1, 1),
        date_to=datetime.date(2022, 1, 10),
        created_by=user
    )[0]
    return booking


@pytest.fixture()
def user(country):
    user_model = UserFactory().create_model()

    user = user_model.objects.filter(username='Bruno')
    if user.exists():
        return user.first()

    user = user_model.objects.get_or_create(username='Bruno', is_superuser=True, is_staff=True)[0]
    Token.objects.create(user=user)

    return user


@pytest.fixture()
@pytest.mark.django_db(transaction=True)
def authorized_api_client(user) -> APIClient:
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Token ' + user.auth_token.key)
    return client


@pytest.fixture()
@pytest.mark.django_db(transaction=True)
def unauthorized_api_client(user) -> APIClient:
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Token 123456789')
    return client


@pytest.fixture()
@pytest.mark.django_db(transaction=True)
def dummy_image_file():
    file = io.BytesIO()
    image = Image.new('RGBA', size=(100, 100), color=(155, 0, 0))
    image.save(file, 'png')
    file.name = 'test.png'
    file.seek(0)
    return file


@pytest.fixture()
def room_type_picture(dummy_image_file):
    image_content = ContentFile(dummy_image_file.read())
    room_type_picture = RoomTypePicture.objects.get_or_create(
        image=image_content
    )[0]

    return room_type_picture
