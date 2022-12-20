# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.test import TestCase
from tastypie.test import ResourceTestCaseMixin
from .models import *
import json

# Create your tests here.


class StoreResourceTest(ResourceTestCaseMixin, TestCase):

    def setUp(self):
        super(StoreResourceTest, self).setUp()

        # Create a user
        self.username = "Merchantxyz"
        self.password = "admin1234"
        self.user = User.objects.create_user(username=self.username, email='merchant1@gmail.com', password=self.password)
        self.customuser = CustomUser.objects.create(user=self.user, name=self.username, role="Merchant")


        # Create Stores 
        Store.objects.create(
            name="Second Store", city="Second City", address="Second Address", 
            merchant=self.customuser, lat=23.456, lon=34.567)


        # User post data
        self.user_login_data = {
            'username': self.username,
            'password': self.password
        }

        # Store post data
        self.store_post_data = {
            "name": "First Store",
            "city": "First City",
            "address": "First Address",
            "lat": 2.345,
            "lon": 45.678
        }


    def get_credentials(self):
        resp = self.api_client.post('/api/v1/user/login/', data=self.user_login_data)
        # self.assertValidJSONResponse(resp)
        resp = self.deserialize(resp)
        return "Bearer {}".format(resp['access_token'])

    def test_create_store_unauthenticated(self):
        self.assertHttpUnauthorized(self.api_client.post('/api/v1/create_store/', format='json', data=self.store_post_data))

    def test_create_store(self):
        self.assertHttpCreated(self.api_client.post('/api/v1/create_store/', data=self.store_post_data, authentication=self.get_credentials()))

    def test_get_list_stores(self):
        self.api_client.get('/api/v1/get_stores/', format='json', authentication=self.get_credentials())
        self.assertEqual(Store.objects.all().count(), 1)



class OrderresourceTest(ResourceTestCaseMixin, TestCase):

    def setUp(self):
        super(OrderresourceTest, self).setUp()
    
         # Create a user
        self.username = "Consumerxyz"
        self.password = "admin123"
        self.user = User.objects.create_user(username=self.username, email='merchant1@gmail.com', password=self.password)
        self.customuser = CustomUser.objects.create(user=self.user, name=self.username, role="Consumer")

    
        # Create Stores 
        self.store_obj = Store.objects.create(
            name="Order Store", city="Order City", address="Order Address", 
            merchant=self.customuser, lat=23.456, lon=34.567
        )

        # Create Items
        self.item1_obj = Item.objects.create(
            name="item1", description="description1", price=100, food_type="Vegetarian"
        )
        self.item2_obj = Item.objects.create(
            name="item2", description="description2", price=200, food_type="Vegetarian"
        )
        self.item3_obj = Item.objects.create(
            name="item3", description="description3", price=300, food_type="Vegetarian"
        )
        self.item4_obj = Item.objects.create(
            name="item4", description="description4", price=400, food_type="Vegetarian"
        )
        self.item5_obj = Item.objects.create(
            name="item5", description="description5", price=500, food_type="Vegetarian"
        )

        # Create store items relatationship
        StoreItem.objects.create(item=self.item1_obj, store=self.store_obj)
        StoreItem.objects.create(item=self.item2_obj, store=self.store_obj)
        StoreItem.objects.create(item=self.item3_obj, store=self.store_obj)
        StoreItem.objects.create(item=self.item4_obj, store=self.store_obj)
        StoreItem.objects.create(item=self.item5_obj, store=self.store_obj)


         # User login data
        self.user_login_data = {
            'username': self.username,
            'password': self.password
        }

        # Create order data
        self.order_create_data = {
            "item_ids": [self.item1_obj.pk, self.item2_obj.pk, self.item3_obj.pk, self.item4_obj.pk, self.item5_obj.pk],
            "store_id": self.store_obj.pk
        }

    def get_credentials(self):
        resp = self.api_client.post('/api/v1/user/login/', data=self.user_login_data)
        # self.assertValidJSONResponse(resp)
        resp = self.deserialize(resp)
        return "Bearer {}".format(resp['access_token'])

    def test_create_order(self):
        self.assertHttpCreated(self.api_client.post('/api/v1/create_order/', data=self.order_create_data, authentication=self.get_credentials()))
        self.assertEqual(Order.objects.all().count(), 1)

    def test_get_all_order_details(self):
        self.assertHttpOK(self.api_client.get('/api/v1/get_orders/', authentication=self.get_credentials()))
