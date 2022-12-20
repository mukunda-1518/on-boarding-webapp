import pytest
from django.contrib.auth.models import User
from food_app.models import *
import json
from django.test import Client
import time

client = Client()


@pytest.mark.django_db
def test_user_with_valid_details(client, merchant_data):
    # Arrange 
    data = {
        "username": merchant_data.username,
        "password": "password@123"
    }

    # Act
    response = client.post('/api/v1/user/login/', data=json.dumps(data),
                content_type="application/json")
    # import pdb;
    # pdb.set_trace();
    
    # Assert
    assert response.status_code == 200



@pytest.mark.django_db
def test_user_with_invalid_username(client, merchant_data):
    # Arrange 
    data = {'username': "Consumer", 'password': "password@123"}

    # Act
    response = client.post('/api/v1/user/login/', data=json.dumps(data),
                content_type="application/json")

    # Assert
    assert response.status_code == 401

@pytest.mark.django_db
def test_user_with_invalid_password(client, merchant_data):
    # Arrange 
    data = {'username': merchant_data.username, 'password': "pass"}

    # Act
    response = client.post('/api/v1/user/login/', data=json.dumps(data),
                content_type="application/json")

    # Assert
    assert response.status_code == 401


@pytest.mark.django_db
def test_create_store_with_valid_data(client, merchant_data, store_post_data):
    # Arrange
    data = {
        "username": merchant_data.username,
        "password": "password@123"
    }

    response = client.post('/api/v1/user/login/', data=json.dumps(data),
                content_type="application/json")
    response = response.json()
    access_token = response['access_token']

    # Act
    response = client.post(
        '/api/v1/create_store/', data=json.dumps(store_post_data), content_type="application/json",
        **{'HTTP_AUTHORIZATION': 'Bearer' + " " + access_token}
    )

    # import pdb
    # pdb.set_trace()

    # Assert
    from django.contrib.auth import settings
    # import ipdb;
    # ipdb.set_trace()
    print(settings.DATABASES)
    assert response.status_code == 201
    assert Store.objects.all().count() == 1
    