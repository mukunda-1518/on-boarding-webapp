from food_app.models import *
from django.contrib.auth.models import User
import pytest


@pytest.fixture
def merchant_data(db):
    user = User.objects.create_user(username = "Merchant", password = "password@123", is_staff=True, email="merchant@gmail.com")
    CustomUser.objects.create(user = user, name = "Merchant", role = "Merchant")
    return user


@pytest.fixture
def store_post_data():
    store_post_data = {
        "name": "First Store",
        "city": "First City",
        "address": "First Address",
        "lat": 2.345,
        "lon": 45.678
    }
    return store_post_data