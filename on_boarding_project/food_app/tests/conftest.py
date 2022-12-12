from food_app.models import *
from django.contrib.auth.models import User
import pytest
from django.contrib.auth import settings


@pytest.fixture
def merchant_data(db):
    user = User.objects.create_user(username = "Merchant", password = "password@123", is_staff=True, email="merchant@gmail.com")
    CustomUser.objects.create(user = user, name = "Merchant", role = "Merchant")
    return user


@pytest.fixture
def consumer_data(db):
    user = User.objects.create_user(username = "Consumer", password = "password@123", is_staff=True, email="consumer@gmail.com")
    CustomUser.objects.create(user = user, name = "Consumer", role = "Consumer")
    return user

@pytest.fixture
def custom_user(db):
    user = User.objects.create_user(username = "Merchant", password = "password@123", is_staff=True, email="merchant@gmail.com")
    custom_user = CustomUser.objects.create(user = user, name = "Merchant", role = "Merchant")
    return custom_user


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


@pytest.fixture
def stores_post_data():
    stores_post_data = [
        {
            "name": "First Store",
            "city": "First City",
            "address": "First Address",
            "lat": 2.345,
            "lon": 45.678
        },
        {
            "name": "Second Store",
            "city": "Second City",
            "address": "Second Address",
            "lat": 2.345,
            "lon": 45.678
        },
        {
            "name": "Third Store",
            "city": "Third City",
            "address": "Third Address",
            "lat": 2.345,
            "lon": 45.678
        },
        
    ]
    return stores_post_data



@pytest.fixture
def store_get_data(store_post_data, custom_user):
    store_obj = Store.objects.create(merchant=custom_user, **store_post_data)
    return store_obj


@pytest.fixture
def stores_get_data(stores_post_data, custom_user):
    store_obj1 = Store.objects.create(merchant=custom_user, **stores_post_data[0])
    store_obj2 = Store.objects.create(merchant=custom_user, **stores_post_data[1])
    store_obj3 = Store.objects.create(merchant=custom_user, **stores_post_data[2])
    return [store_obj1, store_obj2, store_obj3]
    

@pytest.fixture
def stores_put_data():
    update_store_data =  {
            "name": "Updated Store",
            "city": "Updated City",
            "address": "Updated Address",
            "lat": 2.345,
            "lon": 45.678
        }
    return update_store_data
    
    
    

@pytest.fixture(scope="session")
def celery_worker_parameters(django_db_setup):
    assert settings.DATABASES["TEST"]["NAME"].startswith("test_")
    return {}
