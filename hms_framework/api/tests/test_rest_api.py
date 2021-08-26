import datetime
import json

import pytest
from django.conf import settings
from rest_framework import status

from hms_framework.models import Hotel, Address, Country, City, RoomTypePicture, RoomType, RoomFeatureType, BedType, \
    Room, RoomPricePeriod, Customer, Invoice, InvoiceItem, Booking

BASE_URL = settings.BASE_URL + 'api/v1/'


class TestHotelApi:
    url = BASE_URL + 'hotel/'

    @pytest.mark.django_db(transaction=True)
    def test_auth(self, authorized_api_client, unauthorized_api_client):
        res = authorized_api_client.get(self.url)
        assert res.status_code == 200
        res = unauthorized_api_client.get(self.url)
        assert res.status_code == 403

    @pytest.mark.django_db(transaction=True)
    def test_create(self, authorized_api_client, address, user):
        res = authorized_api_client.post(self.url, {
            'name': 'Hotel Test',
            'address': address.id,
            'currency_code': 'EUR',
            'created_by': user.id
        })

        entity = json.loads(res.content.decode('utf-8'))

        assert res.status_code == status.HTTP_201_CREATED

        # Returns correct entity
        assert entity['name'] == 'Hotel Test'
        assert entity['address'] == address.id
        assert entity['currency_code'] == 'EUR'
        assert entity['created_by'] == user.id

        # Exists in database
        hotel = Hotel.objects.get(pk=entity['id'])
        assert hotel is not None

    @pytest.mark.django_db(transaction=True)
    def test_update(self, authorized_api_client, hotel):
        res = authorized_api_client.put(
            f'{self.url}{hotel.id}/',
            {
                'name': 'Hotel Test 2',
                'address': hotel.address.id,
                'currency_code': 'USD',
                'created_by': hotel.created_by.id
            }
        )

        entity = json.loads(res.content.decode('utf-8'))

        assert res.status_code == status.HTTP_200_OK

        # Returns correct entity
        assert entity['name'] == 'Hotel Test 2'
        assert entity['address'] == hotel.address.id
        assert entity['currency_code'] == 'USD'
        assert entity['created_by'] == hotel.created_by.id

        # Exists in database
        hotel = Hotel.objects.get(pk=entity['id'])
        assert hotel.name == 'Hotel Test 2'
        assert hotel.currency_code == 'USD'

    @pytest.mark.django_db(transaction=True)
    def test_delete(self, authorized_api_client, hotel):
        res = authorized_api_client.delete(
            f'{self.url}',
            data={
                'id': hotel.id
            }
        )
        assert res.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


class TestAddressApi:
    url = BASE_URL + 'address/'

    @pytest.mark.django_db(transaction=True)
    def test_auth(self, authorized_api_client, unauthorized_api_client):
        res = authorized_api_client.get(self.url)
        assert res.status_code == 200
        res = unauthorized_api_client.get(self.url)
        assert res.status_code == 403

    @pytest.mark.django_db(transaction=True)
    def test_create(self, authorized_api_client, country, city, address, user):
        res = authorized_api_client.post(self.url, {
            'house_number': '123',
            'street': 'Street test',
            'postal_code': 'D17 X2E',
            'city': city.id,
            'country': country.id,
            'created_by': user.id
        })

        entity = json.loads(res.content.decode('utf-8'))

        assert res.status_code == status.HTTP_201_CREATED

        # Returns correct entity
        assert entity['id'] is not None
        assert entity['house_number'] == '123'
        assert entity['street'] == 'Street test'
        assert entity['city'] == city.id
        assert entity['country'] == country.id
        assert entity['created_by'] == user.id

        # Exists in database
        address = Address.objects.get(pk=entity['id'])
        assert address is not None

    @pytest.mark.django_db(transaction=True)
    def test_update(self, authorized_api_client, address):
        res = authorized_api_client.put(
            f'{self.url}{address.id}/',
            {
                'house_number': '123 changed',
                'street': 'Street test changed',
                'postal_code': 'changed',
                'city': address.city.id,
                'country': address.country.id,
                'created_by': address.created_by.id
            }
        )

        entity = json.loads(res.content.decode('utf-8'))

        assert res.status_code == status.HTTP_200_OK

        # Returns correct entity
        assert entity['house_number'] == '123 changed'
        assert entity['street'] == 'Street test changed'
        assert entity['postal_code'] == 'changed'

        # Exists in database
        address = Address.objects.get(pk=entity['id'])
        assert address.house_number == '123 changed'
        assert address.street == 'Street test changed'
        assert address.postal_code == 'changed'

    @pytest.mark.django_db(transaction=True)
    def test_delete(self, authorized_api_client, address):
        res = authorized_api_client.delete(
            f'{self.url}',
            data={
                'id': address.id
            }
        )
        assert res.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


class TestCountryApi:
    url = BASE_URL + 'country/'

    @pytest.mark.django_db(transaction=True)
    def test_auth(self, authorized_api_client, unauthorized_api_client):
        res = authorized_api_client.get(self.url)
        assert res.status_code == 200
        res = unauthorized_api_client.get(self.url)
        assert res.status_code == 403

    @pytest.mark.django_db(transaction=True)
    def test_create(self, authorized_api_client, country, city, address, user):
        res = authorized_api_client.post(self.url, {
            'name': 'Spain',
            'phone_prefix': '+34',
        })

        entity = json.loads(res.content.decode('utf-8'))

        assert res.status_code == status.HTTP_201_CREATED

        # Returns correct entity
        assert entity['id'] is not None
        assert entity['name'] == 'Spain'
        assert entity['phone_prefix'] == '+34'

        # Exists in database
        country = Country.objects.get(pk=entity['id'])
        assert country is not None

    @pytest.mark.django_db(transaction=True)
    def test_update(self, authorized_api_client, country):
        res = authorized_api_client.put(
            f'{self.url}{country.id}/',
            {
                'name': 'Spain changed',
                'phone_prefix': '+123',
            }
        )

        entity = json.loads(res.content.decode('utf-8'))

        assert res.status_code == status.HTTP_200_OK

        # Returns correct entity
        assert entity['name'] == 'Spain changed'
        assert entity['phone_prefix'] == '+123'

        # Exists in database
        country = Country.objects.get(pk=entity['id'])
        assert country.name == 'Spain changed'
        assert country.phone_prefix == '+123'

    @pytest.mark.django_db(transaction=True)
    def test_delete(self, authorized_api_client, country):
        res = authorized_api_client.delete(
            f'{self.url}',
            data={
                'id': country.id
            }
        )
        assert res.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


class TestCityApi:
    url = BASE_URL + 'city/'

    @pytest.mark.django_db(transaction=True)
    def test_auth(self, authorized_api_client, unauthorized_api_client):
        res = authorized_api_client.get(self.url)
        assert res.status_code == 200
        res = unauthorized_api_client.get(self.url)
        assert res.status_code == 403

    @pytest.mark.django_db(transaction=True)
    def test_create(self, authorized_api_client, country):
        res = authorized_api_client.post(self.url, {
            'name': 'Limerick',
            'country': country.id
        })

        entity = json.loads(res.content.decode('utf-8'))

        assert res.status_code == status.HTTP_201_CREATED

        # Returns correct entity
        assert entity['id'] is not None
        assert entity['name'] == 'Limerick'
        assert entity['country'] == country.id

        # Exists in database
        city = City.objects.get(pk=entity['id'])
        assert city is not None

    @pytest.mark.django_db(transaction=True)
    def test_update(self, authorized_api_client, city):
        res = authorized_api_client.put(
            f'{self.url}{city.id}/',
            {
                'name': 'Madrid Changed',
                'country': city.country.id,
            }
        )

        entity = json.loads(res.content.decode('utf-8'))

        assert res.status_code == status.HTTP_200_OK

        # Returns correct entity
        assert entity['name'] == 'Madrid Changed'

        # Exists in database
        city = City.objects.get(pk=entity['id'])
        assert city.name == 'Madrid Changed'

    @pytest.mark.django_db(transaction=True)
    def test_delete(self, authorized_api_client, city):
        res = authorized_api_client.delete(
            f'{self.url}',
            data={
                'id': city.id
            }
        )
        assert res.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


class TestRoomTypePictureApi:

    url = BASE_URL + 'room-type-picture/'

    @pytest.mark.django_db(transaction=True)
    def test_auth(self, authorized_api_client, unauthorized_api_client):
        res = authorized_api_client.get(self.url)
        assert res.status_code == 200
        res = unauthorized_api_client.get(self.url)
        assert res.status_code == 403

    @pytest.mark.django_db(transaction=True)
    def test_create(self, authorized_api_client, dummy_image_file):
        res = authorized_api_client.post(self.url, {
            'image': dummy_image_file
        })

        entity = json.loads(res.content.decode('utf-8'))

        assert res.status_code == status.HTTP_201_CREATED

        # Returns correct entity
        assert entity['id'] is not None

        # Exists in database
        room_type_picture = RoomTypePicture.objects.get(pk=entity['id'])
        assert room_type_picture is not None

    @pytest.mark.django_db(transaction=True)
    def test_delete(self, authorized_api_client, room_type_picture):
        res = authorized_api_client.delete(
            f'{self.url}',
            data={
                'id': room_type_picture.id
            }
        )
        assert res.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


class TestRoomTypeApi:

    url = BASE_URL + 'room-type/'

    @pytest.mark.django_db(transaction=True)
    def test_auth(self, authorized_api_client, unauthorized_api_client):
        res = authorized_api_client.get(self.url)
        assert res.status_code == 200
        res = unauthorized_api_client.get(self.url)
        assert res.status_code == 403

    @pytest.mark.django_db(transaction=True)
    def test_create(self, authorized_api_client, room_type_picture):
        res = authorized_api_client.post(self.url, {
            'name': 'Twin Room',
            'pictures': [
                room_type_picture.id
            ]
        })

        entity = json.loads(res.content.decode('utf-8'))

        assert res.status_code == status.HTTP_201_CREATED

        # Returns correct entity
        assert entity['id'] is not None
        assert entity['name'] == 'Twin Room'
        assert entity['pictures'][0] == room_type_picture.id

        # Exists in database
        room_type = RoomType.objects.get(pk=entity['id'])
        assert room_type is not None
        assert room_type.name == 'Twin Room'

    @pytest.mark.django_db(transaction=True)
    def test_update(self, authorized_api_client, room_type, room_type_picture):
        res = authorized_api_client.put(
            f'{self.url}{room_type.id}/',
            {
                'name': 'Twin Room Changed',
                'pictures': [
                    room_type_picture.id
                ]
            }
        )

        entity = json.loads(res.content.decode('utf-8'))

        assert res.status_code == status.HTTP_200_OK

        # Returns correct entity
        assert entity['name'] == 'Twin Room Changed'

        # Exists in database
        room_type = RoomType.objects.get(pk=entity['id'])
        assert room_type.name == 'Twin Room Changed'
        assert room_type.pictures[0] == room_type_picture.id

    @pytest.mark.django_db(transaction=True)
    def test_delete(self, authorized_api_client, room_type):
        res = authorized_api_client.delete(
            f'{self.url}',
            data={
                'id': room_type.id
            }
        )
        assert res.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


class TestRoomFeatureTypeApi:

    url = BASE_URL + 'room-feature-type/'

    @pytest.mark.django_db(transaction=True)
    def test_auth(self, authorized_api_client, unauthorized_api_client):
        res = authorized_api_client.get(self.url)
        assert res.status_code == 200
        res = unauthorized_api_client.get(self.url)
        assert res.status_code == 403

    @pytest.mark.django_db(transaction=True)
    def test_create(self, authorized_api_client, room_type_picture, user):
        res = authorized_api_client.post(self.url, {
            'name': 'Air Condition',
            'is_everywhere': True,
            'is_active': True,
            'created_by': user.id
        })

        entity = json.loads(res.content.decode('utf-8'))

        assert res.status_code == status.HTTP_201_CREATED

        # Returns correct entity
        assert entity['id'] is not None
        assert entity['name'] == 'Air Condition'
        assert entity['is_everywhere'] is True
        assert entity['is_active'] is True
        assert entity['created_by'] == user.id

        # Exists in database
        room_feature_type = RoomFeatureType.objects.get(pk=entity['id'])
        assert room_feature_type is not None
        assert room_feature_type.name == 'Air Condition'
        assert room_feature_type.is_everywhere is True
        assert room_feature_type.is_active is True
        assert room_feature_type.created_by.id == user.id

    @pytest.mark.django_db(transaction=True)
    def test_update(self, authorized_api_client, room_feature_type, user):
        res = authorized_api_client.put(
            f'{self.url}{room_feature_type.id}/',
            {
                'name': 'Air Condition Changed',
                'is_everywhere': False,
                'is_active': False,
                'created_by': user.id
            }
        )

        entity = json.loads(res.content.decode('utf-8'))

        assert res.status_code == status.HTTP_200_OK

        # Returns correct entity
        assert entity['name'] == 'Air Condition Changed'

        # Exists in database
        room_feature_type = RoomFeatureType.objects.get(pk=entity['id'])
        assert room_feature_type.name == 'Air Condition Changed'
        assert room_feature_type.is_everywhere is False
        assert room_feature_type.is_active is False

    @pytest.mark.django_db(transaction=True)
    def test_delete(self, authorized_api_client, room_feature_type):
        res = authorized_api_client.delete(
            f'{self.url}',
            data={
                'id': room_feature_type.id
            }
        )
        assert res.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


class TestBedTypeApi:
    url = BASE_URL + 'bed-type/'

    @pytest.mark.django_db(transaction=True)
    def test_auth(self, authorized_api_client, unauthorized_api_client):
        res = authorized_api_client.get(self.url)
        assert res.status_code == 200
        res = unauthorized_api_client.get(self.url)
        assert res.status_code == 403

    @pytest.mark.django_db(transaction=True)
    def test_create(self, authorized_api_client):
        res = authorized_api_client.post(self.url, {
            'name': 'Double King',
            'people_capacity': 2
        })

        entity = json.loads(res.content.decode('utf-8'))

        assert res.status_code == status.HTTP_201_CREATED

        # Returns correct entity
        assert entity['id'] is not None
        assert entity['name'] == 'Double King'
        assert entity['people_capacity'] == 2

        # Exists in database
        bed_type = BedType.objects.get(pk=entity['id'])
        assert bed_type is not None
        assert bed_type.name == 'Double King'
        assert bed_type.people_capacity == 2

    @pytest.mark.django_db(transaction=True)
    def test_update(self, authorized_api_client, bed_type):
        res = authorized_api_client.put(
            f'{self.url}{bed_type.id}/',
            {
                'name': 'Single Room Changed',
                'people_capacity': 2
            }
        )

        entity = json.loads(res.content.decode('utf-8'))

        assert res.status_code == status.HTTP_200_OK

        # Returns correct entity
        assert entity['name'] == 'Single Room Changed'
        assert entity['people_capacity'] == 2

        # Exists in database
        bed_type = BedType.objects.get(pk=entity['id'])
        assert bed_type.name == 'Single Room Changed'
        assert bed_type.people_capacity == 2

    @pytest.mark.django_db(transaction=True)
    def test_delete(self, authorized_api_client, bed_type):
        res = authorized_api_client.delete(
            f'{self.url}',
            data={
                'id': bed_type.id
            }
        )
        assert res.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


class TestRoomApi:

    url = BASE_URL + 'room/'

    @pytest.mark.django_db(transaction=True)
    def test_auth(self, authorized_api_client, unauthorized_api_client):
        res = authorized_api_client.get(self.url)
        assert res.status_code == 200
        res = unauthorized_api_client.get(self.url)
        assert res.status_code == 403

    @pytest.mark.django_db(transaction=True)
    def test_create(self, authorized_api_client, hotel, room_type, room_feature_type, bed_type, user):
        res = authorized_api_client.post(self.url, {
            'hotel': hotel.id,
            'price_night': 100,
            'price_week': 600,
            'price_month': 2400,
            'room_type': room_type.id,
            'description': 'This is a description',
            'room_number': 1,
            'floor': 1,
            'square_meters': 45,
            'room_features': [
                room_feature_type.id
            ],
            'room_beds': [
                bed_type.id
            ],
            'created_by': user.id
        })

        entity = json.loads(res.content.decode('utf-8'))

        assert res.status_code == status.HTTP_201_CREATED

        # Returns correct entity
        assert entity['id'] is not None
        assert entity['hotel'] == hotel.id
        assert entity['price_night'] == 100
        assert entity['price_week'] == 600
        assert entity['price_month'] == 2400
        assert entity['room_type'] == room_type.id
        assert entity['description'] == 'This is a description'
        assert entity['room_number'] == 1
        assert entity['floor'] == 1
        assert entity['square_meters'] == 45
        assert entity['room_features'][0] == room_feature_type.id
        assert entity['room_beds'][0] == bed_type.id
        assert entity['created_by'] == user.id

        # Exists in database
        room = Room.objects.get(pk=entity['id'])
        assert room is not None
        assert room.hotel.id == hotel.id
        assert room.price_night == 100
        assert room.price_week == 600
        assert room.price_month == 2400
        assert room.room_type.id == room_type.id
        assert room.description == 'This is a description'
        assert room.room_number == 1
        assert room.floor == 1
        assert room.square_meters == 45
        assert room.room_features.first().id == room_feature_type.id
        assert room.room_beds.first().id == bed_type.id
        assert room.created_by.id == user.id

    @pytest.mark.django_db(transaction=True)
    def test_update(self, authorized_api_client, room):
        res = authorized_api_client.put(
            f'{self.url}{room.id}/',
            {
                'hotel': room.hotel.id,
                'room_type': room.room_type.id,
                'price_night': 101,
                'price_week': 601,
                'price_month': 2401,
                'description': 'This is a description changed',
                'room_number': 2,
                'floor': 2,
                'square_meters': 46,
                'room_features': [
                    room.room_features.first().id
                ],
                'room_beds': [
                    room.room_beds.first().id
                ],
                'created_by': room.created_by.id
            }
        )

        entity = json.loads(res.content.decode('utf-8'))

        assert res.status_code == status.HTTP_200_OK

        # Returns correct entity
        assert entity['price_night'] == 101
        assert entity['price_week'] == 601
        assert entity['price_month'] == 2401
        assert entity['description'] == 'This is a description changed'
        assert entity['room_number'] == 2
        assert entity['floor'] == 2
        assert entity['square_meters'] == 46
        assert entity['room_features'] == []
        assert entity['room_beds'] == []
        assert entity['created_by'] == room.user.id

        # Exists in database
        room = Room.objects.get(pk=entity['id'])
        assert room.price_night == 101
        assert room.price_week == 601
        assert room.price_month == 2401
        assert room.description == 'This is a description changed'
        assert room.room_number == 2
        assert room.floor == 2
        assert room.square_meters == 46
        assert room.room_features == []
        assert room.room_beds == []
        assert room.created_by == room.user.id

    @pytest.mark.django_db(transaction=True)
    def test_delete(self, authorized_api_client, room):
        res = authorized_api_client.delete(
            f'{self.url}',
            data={
                'id': room.id
            }
        )
        assert res.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


class TestRoomPricePeriodApi:
    url = BASE_URL + 'room-price-period/'

    @pytest.mark.django_db(transaction=True)
    def test_auth(self, authorized_api_client, unauthorized_api_client):
        res = authorized_api_client.get(self.url)
        assert res.status_code == 200
        res = unauthorized_api_client.get(self.url)
        assert res.status_code == 403

    @pytest.mark.django_db(transaction=True)
    def test_create(self, authorized_api_client, room, user):
        res = authorized_api_client.post(self.url, {
            'room': room.id,
            'price_night': 100,
            'price_week': 600,
            'price_month': 2400,
            'valid_date_from': '2021-08-25',
            'valid_date_to': '2021-09-25',
            'valid_type': 'BOOKING_DATE',
            'created_by': user.id
        })

        entity = json.loads(res.content.decode('utf-8'))

        assert res.status_code == status.HTTP_201_CREATED

        # Returns correct entity
        assert entity['id'] is not None
        assert entity['room'] == room.id
        assert entity['price_night'] == 100
        assert entity['price_week'] == 600
        assert entity['price_month'] == 2400
        assert entity['valid_date_from'] == '2021-08-25'
        assert entity['valid_date_to'] == '2021-09-25'
        assert entity['valid_type'] == 'BOOKING_DATE'

        # Exists in database
        room_price_period = RoomPricePeriod.objects.get(pk=entity['id'])
        assert room_price_period is not None
        assert room_price_period.room.id == room.id
        assert room_price_period.price_night == 100
        assert room_price_period.price_week == 600
        assert room_price_period.price_month == 2400
        assert room_price_period.valid_date_from == datetime.date(2021, 8, 25)
        assert room_price_period.valid_date_to == datetime.date(2021, 9, 25)
        assert room_price_period.valid_type == 'BOOKING_DATE'
        assert room.created_by.id == user.id

    @pytest.mark.django_db(transaction=True)
    def test_update(self, authorized_api_client, room_price_period):
        res = authorized_api_client.put(
            f'{self.url}{room_price_period.id}/',
            {
                'room': room_price_period.room.id,
                'price_night': 101,
                'price_week': 601,
                'price_month': 2401,
                'valid_date_from': '2021-08-26',
                'valid_date_to': '2021-09-26',
                'valid_type': 'STAY_DATE',
                'created_by': room_price_period.created_by.id
            }
        )

        entity = json.loads(res.content.decode('utf-8'))

        assert res.status_code == status.HTTP_200_OK

        # Returns correct entity
        assert entity['room'] == room_price_period.room.id
        assert entity['price_night'] == 101
        assert entity['price_week'] == 601
        assert entity['price_month'] == 2401
        assert entity['valid_date_from'] == '2021-08-26'
        assert entity['valid_date_to'] == '2021-09-26'
        assert entity['valid_type'] == 'STAY_DATE'
        assert entity['created_by'] == room_price_period.created_by.id

        # Exists in database
        room_price_period = RoomPricePeriod.objects.get(pk=entity['id'])
        assert room_price_period.price_night == 101
        assert room_price_period.price_week == 601
        assert room_price_period.price_month == 2401
        assert room_price_period.valid_date_from == datetime.date(2021, 8, 26)
        assert room_price_period.valid_date_to == datetime.date(2021, 9, 26)
        assert room_price_period.valid_type == 'STAY_DATE'
        assert room_price_period.created_by.id == room_price_period.created_by.id

    @pytest.mark.django_db(transaction=True)
    def test_delete(self, authorized_api_client, room):
        res = authorized_api_client.delete(
            f'{self.url}',
            data={
                'id': room.id
            }
        )
        assert res.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


class TestCustomerApi:

    url = BASE_URL + 'customer/'

    @pytest.mark.django_db(transaction=True)
    def test_auth(self, authorized_api_client, unauthorized_api_client):
        res = authorized_api_client.get(self.url)
        assert res.status_code == 200
        res = unauthorized_api_client.get(self.url)
        assert res.status_code == 403

    @pytest.mark.django_db(transaction=True)
    def test_create(self, authorized_api_client, address, user):
        res = authorized_api_client.post(self.url, {
            'first_name': 'Bruno',
            'last_name': 'Quintana',
            'telephone': '+353123456789',
            'email': 'public.bq@gmail.com',
            'address': address.id,
            'has_debts': False,
            'last_has_debts_notified_datetime': '',
            'created_by': user.id
        })

        entity = json.loads(res.content.decode('utf-8'))

        assert res.status_code == status.HTTP_201_CREATED

        # Returns correct entity
        assert entity['id'] is not None
        assert entity['first_name'] == 'Bruno'
        assert entity['last_name'] == 'Quintana'
        assert entity['telephone'] == '+353123456789'
        assert entity['email'] == 'public.bq@gmail.com'
        assert entity['address'] == address.id
        assert entity['has_debts'] is False
        assert entity['last_has_debts_notified_datetime'] is None
        assert entity['created_by'] == user.id

        # Exists in database
        customer = Customer.objects.get(pk=entity['id'])
        assert customer is not None
        assert customer.first_name == 'Bruno'
        assert customer.last_name == 'Quintana'
        assert customer.telephone == '+353123456789'
        assert customer.email == 'public.bq@gmail.com'
        assert customer.address.id == address.id
        assert customer.has_debts is False
        assert customer.last_has_debts_notified_datetime is None
        assert customer.created_by.id == user.id

    @pytest.mark.django_db(transaction=True)
    def test_update(self, authorized_api_client, customer):
        res = authorized_api_client.put(
            f'{self.url}{customer.id}/',
            {
                'first_name': '1Bruno',
                'last_name': '1Quintana',
                'telephone': '1+353123456789',
                'email': '1public.bq@gmail.com',
                'address': customer.address.id,
                'has_debts': True,
                'last_has_debts_notified_datetime': '',
                'created_by': customer.created_by.id
            }
        )

        entity = json.loads(res.content.decode('utf-8'))

        assert res.status_code == status.HTTP_200_OK

        # Returns correct entity
        assert entity['first_name'] == '1Bruno'
        assert entity['last_name'] == '1Quintana'
        assert entity['telephone'] == '1+353123456789'
        assert entity['email'] == '1public.bq@gmail.com'
        assert entity['address'] == customer.address.id
        assert entity['has_debts'] is True
        assert entity['last_has_debts_notified_datetime'] is None
        assert entity['created_by'] == customer.created_by.id

        # Exists in database
        customer = Customer.objects.get(pk=entity['id'])
        assert customer.first_name == '1Bruno'
        assert customer.last_name == '1Quintana'
        assert customer.telephone == '1+353123456789'
        assert customer.email == '1public.bq@gmail.com'
        assert customer.address == customer.address
        assert customer.has_debts is True
        assert customer.last_has_debts_notified_datetime is None
        assert customer.created_by == customer.created_by

    @pytest.mark.django_db(transaction=True)
    def test_delete(self, authorized_api_client, customer):
        res = authorized_api_client.delete(
            f'{self.url}',
            data={
                'id': customer.id
            }
        )
        assert res.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


class TestInvoiceApi:

    url = BASE_URL + 'invoice/'

    @pytest.mark.django_db(transaction=True)
    def test_auth(self, authorized_api_client, unauthorized_api_client):
        res = authorized_api_client.get(self.url)
        assert res.status_code == 200
        res = unauthorized_api_client.get(self.url)
        assert res.status_code == 403

    @pytest.mark.django_db(transaction=True)
    def test_create(self, authorized_api_client, customer, user):
        res = authorized_api_client.post(self.url, {
            'customer': customer.id,
            'is_deleted': False,
            'created_by': user.id
        })

        entity = json.loads(res.content.decode('utf-8'))

        assert res.status_code == status.HTTP_201_CREATED

        # Returns correct entity
        assert entity['id'] is not None
        assert entity['customer'] == customer.id
        assert entity['is_deleted'] is False
        assert entity['created_by'] == user.id

        # Exists in database
        invoice = Invoice.objects.get(pk=entity['id'])
        assert invoice is not None
        assert invoice.customer.id == customer.id
        assert invoice.is_deleted is False
        assert invoice.created_by.id == user.id

    @pytest.mark.django_db(transaction=True)
    def test_update(self, authorized_api_client, invoice, customer, user):
        res = authorized_api_client.put(
            f'{self.url}{customer.id}/',
            {
                'customer': customer.id,
                'is_deleted': False,
                'created_by': user.id,
            }
        )

        entity = json.loads(res.content.decode('utf-8'))

        assert res.status_code == status.HTTP_200_OK

        # Returns correct entity
        assert entity['customer'] == customer.id
        assert entity['is_deleted'] is False
        assert entity['created_by'] == customer.created_by.id

        # Exists in database
        invoice = Invoice.objects.get(pk=entity['id'])
        assert invoice.due_date is not None
        assert invoice.customer.id == customer.id
        assert invoice.is_deleted is False
        assert invoice.created_by.id == user.id

    @pytest.mark.django_db(transaction=True)
    def test_delete(self, authorized_api_client, invoice):
        res = authorized_api_client.delete(
            f'{self.url}',
            data={
                'id': invoice.id
            }
        )
        assert res.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


class TestInvoiceItemApi:
    url = BASE_URL + 'invoice-item/'

    @pytest.mark.django_db(transaction=True)
    def test_auth(self, authorized_api_client, unauthorized_api_client):
        res = authorized_api_client.get(self.url)
        assert res.status_code == 200
        res = unauthorized_api_client.get(self.url)
        assert res.status_code == 403

    @pytest.mark.django_db(transaction=True)
    def test_create(self, authorized_api_client, invoice, user):
        res = authorized_api_client.post(self.url, {
            'invoice': invoice.id,
            'description': 'Twin Room - 3 nights',
            'amount': 100,
            'discount': 0,
            'created_by': user.id
        })

        entity = json.loads(res.content.decode('utf-8'))

        assert res.status_code == status.HTTP_201_CREATED

        # Returns correct entity
        assert entity['id'] is not None
        assert entity['invoice'] == invoice.id
        assert entity['description'] == 'Twin Room - 3 nights'
        assert entity['amount'] == 100
        assert entity['discount'] == 0
        assert entity['created_by'] == user.id

        # Exists in database
        invoice_item = InvoiceItem.objects.get(pk=entity['id'])
        assert invoice_item is not None
        assert invoice_item.invoice.id == invoice.id
        assert invoice_item.description == 'Twin Room - 3 nights'
        assert invoice_item.amount == 100
        assert invoice_item.discount == 0
        assert invoice_item.created_by.id == user.id

    @pytest.mark.django_db(transaction=True)
    def test_update(self, authorized_api_client, invoice_item, user):
        res = authorized_api_client.put(
            f'{self.url}{invoice_item.id}/',
            {
                'invoice': invoice_item.invoice.id,
                'description': '1Twin Room - 3 nights',
                'amount': 101,
                'discount': 1,
                'created_by': user.id
            }
        )

        entity = json.loads(res.content.decode('utf-8'))

        assert res.status_code == status.HTTP_200_OK

        # Returns correct entity
        assert entity['invoice'] == invoice_item.invoice.id
        assert entity['description'] == '1Twin Room - 3 nights'
        assert entity['amount'] == 101
        assert entity['discount'] == 1
        assert entity['created_by'] == user.id

        # Exists in database
        invoice_item = InvoiceItem.objects.get(pk=entity['id'])
        assert invoice_item.invoice.id == invoice_item.invoice.id
        assert invoice_item.description == '1Twin Room - 3 nights'
        assert invoice_item.amount == 101
        assert invoice_item.discount == 1
        assert invoice_item.created_by.id == user.id

    @pytest.mark.django_db(transaction=True)
    def test_delete(self, authorized_api_client, invoice_item):
        res = authorized_api_client.delete(
            f'{self.url}',
            data={
                'id': invoice_item.id
            }
        )
        assert res.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


class TestBookingApi:

    url = BASE_URL + 'booking/'

    @pytest.mark.django_db(transaction=True)
    def test_auth(self, authorized_api_client, unauthorized_api_client):
        res = authorized_api_client.get(self.url)
        assert res.status_code == 200
        res = unauthorized_api_client.get(self.url)
        assert res.status_code == 403

    @pytest.mark.django_db(transaction=True)
    def test_create(self, authorized_api_client, room, customer, user):
        res = authorized_api_client.post(self.url, {
            'room': room.id,
            'customer': customer.id,
            'date_from': '2022-01-01',
            'date_to': '2022-01-10',
            'created_by': user.id
        })

        entity = json.loads(res.content.decode('utf-8'))

        assert res.status_code == status.HTTP_201_CREATED

        # Returns correct entity
        assert entity['id'] is not None
        assert entity['room'] == room.id
        assert entity['customer'] == customer.id
        assert entity['date_from'] == '2022-01-01'
        assert entity['date_to'] == '2022-01-10'
        assert entity['created_by'] == user.id

        # Exists in database
        booking = Booking.objects.get(pk=entity['id'])
        assert booking is not None
        assert booking.room.id == room.id
        assert booking.customer.id == customer.id
        assert booking.date_from == datetime.date(2022, 1, 1)
        assert booking.date_to == datetime.date(2022, 1, 10)

    @pytest.mark.django_db(transaction=True)
    def test_create_calls_service(self, authorized_api_client, room, customer, user, mocker):
        class Trigger:
            triggered = False

        def trigger(room_id, customer_id, date_from, date_to, created_by_user_id):
            Trigger.triggered = True
            assert room_id is not None
            assert customer_id is not None
            assert date_from is not None
            assert date_to is not None
            assert created_by_user_id is not None

        mocker.patch('hms_framework.services.booking.make_booking.MakeBooking.execute', side_effect=trigger)

        authorized_api_client.post(self.url, {
            'room': room.id,
            'customer': customer.id,
            'date_from': '2022-01-01',
            'date_to': '2022-01-10',
            'created_by': user.id
        })

        assert Trigger.triggered is True

    @pytest.mark.django_db(transaction=True)
    def test_update(self, authorized_api_client, booking):
        res = authorized_api_client.put(
            f'{self.url}{booking.id}/',
            {
                'room': booking.room.id,
                'customer': booking.customer.id,
                'date_from': '2021-12-15',
                'date_to': '2021-12-31',
                'created_by': booking.created_by.id
            }
        )

        entity = json.loads(res.content.decode('utf-8'))

        assert res.status_code == status.HTTP_200_OK

        # Returns correct entity
        assert entity['room'] == booking.room.id
        assert entity['customer'] == booking.customer.id
        assert entity['date_from'] == '2021-12-15'
        assert entity['date_to'] == '2021-12-31'
        assert entity['created_by'] == booking.created_by.id

        # Exists in database
        booking = Booking.objects.get(pk=entity['id'])
        assert booking.date_from == datetime.date(2021, 12, 15)
        assert booking.date_to == datetime.date(2021, 12, 31)

    @pytest.mark.django_db(transaction=True)
    def test_delete(self, authorized_api_client, booking):
        res = authorized_api_client.delete(
            f'{self.url}',
            data={
                'id': booking.id
            }
        )
        assert res.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


class TestSearchAvailabilityServiceApi:

    url = BASE_URL + 'search-availability-service/'

    @pytest.mark.django_db(transaction=True)
    def test_auth(self, authorized_api_client, unauthorized_api_client):
        res = authorized_api_client.get(self.url)
        # Because we don't accept gets requests.
        assert res.status_code == 405
        res = unauthorized_api_client.get(self.url)
        assert res.status_code == 403

    @pytest.mark.django_db(transaction=True)
    def test_create(self, authorized_api_client, room_type, mocker):
        class Trigger:
            triggered = False

        def trigger(room_type, number_of_guests, date_from, date_to):
            Trigger.triggered = True
            assert room_type is not None
            assert number_of_guests is not None
            assert date_from is not None
            assert date_to is not None

        mocker.patch('hms_framework.services.booking.search_availability.SearchAvailability.execute',
                     side_effect=trigger)

        res = authorized_api_client.post(self.url, {
            'room_type': room_type.id,
            'number_of_guests': 1,
            'date_from': '2022-01-01',
            'date_to': '2022-01-10',
        })

        assert res.status_code == status.HTTP_200_OK

        # Make sure it calls the right service
        assert Trigger.triggered is True

    @pytest.mark.django_db(transaction=True)
    def test_update(self, authorized_api_client):
        res = authorized_api_client.put(
            f'{self.url}',
            data={
                'id': 1
            }
        )
        assert res.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    @pytest.mark.django_db(transaction=True)
    def test_delete(self, authorized_api_client):
        res = authorized_api_client.delete(
            f'{self.url}',
            data={
                'id': 1
            }
        )
        assert res.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
