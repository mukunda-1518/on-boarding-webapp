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
def custom_consumer_data(db):
    user = User.objects.create_user(username = "Consumer", password = "password@123", is_staff=True, email="consumer@gmail.com")
    custom_user = CustomUser.objects.create(user = user, name = "Consumer", role = "Consumer")
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
def store_get_data(db, store_post_data, custom_user):
    store_obj = Store.objects.create(merchant=custom_user, **store_post_data)
    return store_obj


@pytest.fixture
def stores_get_data(db, stores_post_data, custom_user):
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
    
  
@pytest.fixture
def prepare_items_data():
    items = [
        {
            "name": "new item1",
            "description": "Description",
            "price": 200,
            "food_type": "Vegetarian"
        },
        {
            "name": "new item2",
            "description": "Description",
            "price": 100,
            "food_type": "Vegetarian"
        },
        {
            "name": "new item3",
            "description": "Description",
            "price": 300,
            "food_type": "Vegetarian"
        }   
    ] 
    return items
  
@pytest.fixture
def populate_items(db, prepare_items_data):
    item_objs = [ Item.objects.create(**item) for item in prepare_items_data]
    return item_objs
    

@pytest.fixture
def create_store_items(db, store_get_data, populate_items):
    store_items = [StoreItem.objects.create(item=item, store=store_get_data) for item in populate_items] 
    return store_items
    
@pytest.fixture
def populate_order(db, store_get_data, custom_user, custom_consumer_data, populate_items):
    order_obj = Order.objects.create(store=store_get_data, merchant=custom_user, user=custom_consumer_data)
    order_items_objs = [OrderItem.objects.create(order=order_obj, item=item) for item in populate_items]
    return order_obj
        
    

@pytest.fixture(scope="session")
def celery_worker_parameters(django_db_setup):
    assert settings.DATABASES["TEST"]["NAME"].startswith("test_")
    return {}
