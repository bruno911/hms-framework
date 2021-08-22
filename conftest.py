import random
from typing import List

import pytest

from hms_framework.factory import UserFactory
from hms_framework.models import City, Country


@pytest.fixture()
def country():
    country = Country.objects.get_or_create(name='Ireland', phone_prefix='353')[0]
    return country


@pytest.fixture()
def city(country):
    city = City.objects.get_or_create(name='Dublin', country=country)[0]
    return city


@pytest.fixture()
def user(country):
    user_model = UserFactory().create_model()
    user = user_model.objects.get_or_create(username='Bruno', is_superuser=True, is_staff=True)[0]
    return user

