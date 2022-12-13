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
    print(settings.DATABASES)
    assert response.status_code == 201
    # assert Store.objects.all().count() == 1
    

    
class TestStoreResource:
    
    @pytest.mark.django_db
    def test_create_store_with_valid_data(self, client, merchant_data, store_post_data):
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
        print(settings.DATABASES)
        assert response.status_code == 201
        # assert Store.objects.all().count() == 1
        
    def test_create_store_by_consumer_raise_unauthorised(self, client, consumer_data, store_post_data):
        # Arrange
        data = {
            "username": consumer_data.username,
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

        # Assert
        assert response.status_code == 401
        
    @pytest.mark.django_db
    def test_get_store_details(self, client, custom_user, store_get_data):
        # Arrange
        data = {
            "username": custom_user.name,
            "password": "password@123"
        }

        response = client.post('/api/v1/user/login/', data=json.dumps(data),
                    content_type="application/json")
        response = response.json()
        access_token = response['access_token']

        # Act
        response = client.get(
            '/api/v1/get_stores/1/', content_type="application/json",
            **{'HTTP_AUTHORIZATION': 'Bearer' + " " + access_token}
        )
        response = response.json()
        store_details = response['store_details']
        
        # Assert
        assert store_details['Address'] == store_get_data.address
        assert store_details['id'] == store_get_data.id
        assert store_details['city'] == store_get_data.city


    @pytest.mark.django_db
    def test_get_stores_details(self, client, custom_user, stores_get_data):
        # Arrange
        data = {
            "username": custom_user.name,
            "password": "password@123"
        }

        response = client.post('/api/v1/user/login/', data=json.dumps(data),
                    content_type="application/json")
        response = response.json()
        access_token = response['access_token']

        # Act
        response = client.get(
            '/api/v1/get_stores/', content_type="application/json",
            **{'HTTP_AUTHORIZATION': 'Bearer' + " " + access_token}
        )
        response = response.json()
        stores = response['stores']
        
        # Assert
        assert len(stores) == len(stores_get_data)
        for i in range(len(stores)):
            assert stores[i]['id'] == stores_get_data[i].id
            
    
    @pytest.mark.django_db
    def test_update_existing_store_details(self, client, custom_user, stores_put_data, store_get_data):
        # Arrange
        data = {
            "username": custom_user.name,
            "password": "password@123"
        }

        response = client.post('/api/v1/user/login/', data=json.dumps(data),
                    content_type="application/json")
        response = response.json()
        access_token = response['access_token']

        # Act
        response = client.put(
            '/api/v1/update_store/{}/'.format(store_get_data.id), data=json.dumps(stores_put_data), content_type="application/json",
            **{'HTTP_AUTHORIZATION': 'Bearer' + " " + access_token}
        )
        
        # Assert
        assert response.status_code == 200
        
    @pytest.mark.django_db
    def test_update_store_details_creates_one_if_store_does_not_exists(self, client, custom_user, stores_put_data, store_get_data):
        # Arrange
        data = {
            "username": custom_user.name,
            "password": "password@123"
        }

        response = client.post('/api/v1/user/login/', data=json.dumps(data),
                    content_type="application/json")
        response = response.json()
        access_token = response['access_token']

        # Act
        response = client.put(
            '/api/v1/update_store/10/', data=json.dumps(stores_put_data), content_type="application/json",
            **{'HTTP_AUTHORIZATION': 'Bearer' + " " + access_token}
        )
        
        # Assert
        assert response.status_code == 201
        
    @pytest.mark.django_db
    def test_delete_store(self, client, custom_user, stores_put_data, store_get_data):
        # Arrange
        data = {
            "username": custom_user.name,
            "password": "password@123"
        }

        response = client.post('/api/v1/user/login/', data=json.dumps(data),
                    content_type="application/json")
        response = response.json()
        access_token = response['access_token']

        # Act
        response = client.delete(
            '/api/v1/delete_store/{}/'.format(store_get_data.id), data=json.dumps(stores_put_data), content_type="application/json",
            **{'HTTP_AUTHORIZATION': 'Bearer' + " " + access_token}
        )
        
        # Assert
        assert response.status_code == 200
 
 
 
@pytest.mark.django_db       
class TestOrderResource:
    
    def test_create_order(self, client, create_store_items, consumer_data, store_get_data, populate_items):
        # Arrange
        data = {
            "username": consumer_data.username,
            "password": "password@123"
        }
        response = client.post('/api/v1/user/login/', data=json.dumps(data),
                    content_type="application/json")
        response = response.json()
        access_token = response['access_token']
        
        body = {
            'item_ids': [item.id for item in populate_items],
            'store_id': store_get_data.id
        }
        
        # Act
        response = client.post(
            '/api/v1/order/', data=json.dumps(body), content_type="application/json",
            **{'HTTP_AUTHORIZATION': 'Bearer' + " " + access_token}
        )
        
        
        # Assert
        assert response.status_code == 201
        
    
    
    def test_get_order_deatails(self, client, populate_order, custom_consumer_data):
        # Arrange
        data = {
            "username": custom_consumer_data.name,
            "password": "password@123"
        }
        response = client.post('/api/v1/user/login/', data=json.dumps(data),
                    content_type="application/json")
        response = response.json()
        access_token = response['access_token']
        
        
        # Act
        response = client.get(
            '/api/v1/order/{}/'.format(populate_order.id), content_type="application/json",
            **{'HTTP_AUTHORIZATION': 'Bearer' + " " + access_token}
        )
        
        
        # Assert
        assert response.status_code == 200
        assert response.json()['id'] == populate_order.id
    
    def test_get_orders_details(self, client, populate_order, custom_consumer_data):
        
        # Arrange
        data = {
            "username": custom_consumer_data.name,
            "password": "password@123"
        }
        response = client.post('/api/v1/user/login/', data=json.dumps(data),
                    content_type="application/json")
        response = response.json()
        access_token = response['access_token']
        
        
        # Act
        response = client.get(
            '/api/v1/order/', content_type="application/json",
            **{'HTTP_AUTHORIZATION': 'Bearer' + " " + access_token}
        )
        
        
        # Assert
        assert response.status_code == 200
        response = response.json()
        assert response['objects'][0]['id'] == populate_order.id