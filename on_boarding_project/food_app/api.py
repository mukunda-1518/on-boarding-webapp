import json

from tastypie import fields
from tastypie.authentication import ApiKeyAuthentication, BasicAuthentication, Authentication
from tastypie.authorization import Authorization
from tastypie.http import HttpUnauthorized, HttpCreated, HttpNotFound
from tastypie.models import ApiKey
from tastypie.resources import ModelResource, ALL

from .mixins import CommonMethods
from .models import *
from django.contrib.auth import get_user_model
from django.conf.urls import url, include
from django.core import serializers
from tastypie.utils import trailing_slash
from django.contrib.auth import authenticate
from django.db.models import *

User = get_user_model()


class UserResource(ModelResource):

    class Meta:
        queryset = User.objects.all()
        resource_name = "user"
        # fields = ["username", "email", "password", "is_staff"]
        allowed_methods = ["get", "post", "put", "delete"]
        authentication = Authentication()
        authorization = Authorization()

    def obj_create(self, bundle, request=None, **kwargs):
        username = bundle.data.pop('username')
        password = bundle.data.pop('password')
        role = bundle.data.pop('role')
        email = bundle.data.pop('email')
        is_staff = bundle.data.pop('is_staff')
        user = User.objects.create(username=username, password=password, email=email, is_staff=is_staff)
        user.set_password(password)
        user.save()
        CustomUser.objects.create(
            user=user,
            name=username,
            role=role
        )

    def prepend_urls(self):

        return [
            url(r"^user/signup/$", self.wrap_view('signup'), name='user_signup'),
            url(r"^user/login/$", self.wrap_view('login'), name='api_login'),
        ]

    def signup(self, request, **kwargs):
        """"
        """
        data = self.deserialize(request, request.body, format=request.META.get(
            'CONTENT_TYPE', 'application/json'))  # Got json data convert to dict
        username = data['username']
        password = data['password']
        role = data['role']
        email = data['email']
        is_staff = data['is_staff']

        user = User.objects.create(username=username, password=password, email=email, is_staff=is_staff)
        user.set_password(password)
        user.save()
        CustomUser.objects.create(
            user=user,
            name=username,
            role=role
        )
        api_key = ApiKey.objects.get(user=user)
        custom_user_obj = CustomUser.objects.get(user__username=user)
        role = custom_user_obj.role
        return self.create_response(request, {
            'api_key': api_key.key,
            'username': username,
            'role': role,
            'success': True
        })

    def login(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        data = self.deserialize(request, request.body, format=request.META.get(
            'CONTENT_TYPE', 'application/json'))  # Got json data convert to dict
        username = data['username']
        password = data['password']
        user = authenticate(username=username, password=password)
        if user:
            try:
                api_key = ApiKey.objects.get(user=user)
            except ApiKey.DoesNotExist:
                api_key = ApiKey.objects.create(user=user)
            custom_user_obj = CustomUser.objects.get(user__username=user)
            role = custom_user_obj.role
            return self.create_response(request, {
                'api_key': api_key.key,
                'username': username,
                'role': role,
                'success': True
            })
        else:
            return self.create_response(
                request,
                {'success': False, 'message': 'User is not registered or user is inactive state'},
                HttpUnauthorized
            )


class CustomUserResource(ModelResource):
    user = fields.OneToOneField(UserResource, 'user', full=True)

    class Meta:
        queryset = CustomUser.objects.all()
        resource_name = 'customuser'
        include_resource_uri = False
        authentication = Authentication()
        authorization = Authorization()


class StoreResource(ModelResource, CommonMethods):
    merchant = fields.ForeignKey(CustomUserResource, 'merchant', full=True)

    class Meta:
        queryset = Store.objects.all()
        resource_name = "store"
        allowed_methods = ['get', 'post', 'put', 'patch', 'delete']
        authentication = ApiKeyAuthentication()
        authorization = Authorization()

    def prepend_urls(self):

        return [
            url(r"^create_store/$", self.wrap_view('create_store'), name='create_store'),
            url(r"^get_stores/$", self.wrap_view('get_stores'), name='get_stores'),
            url(r"^update_store/(?P<pk>.*?)/$", self.wrap_view('update_store'), name='update_store'),
            url(r"^delete_store/(?P<pk>.*?)/$", self.wrap_view('delete_store'), name='delete_store'),
            url(r"^get_stores/(?P<pk>.*?)/$", self.wrap_view('get_store'), name='get_store'),
        ]

    def create_store(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        self.is_authenticated(request)
        data = self.deserialize(request, request.body, format=request.META.get(
            'CONTENT_TYPE', 'application/json'))
        username = request.user
        custom_user_obj = self.get_custom_user(username)
        if custom_user_obj.role == "Merchant":
            store = Store(merchant=custom_user_obj, **data)
            store.save()
            return self.create_response(request, {
                "name": store.name,
                "city": store.city,
                "Address": store.address,
                "lat": store.lat,
                "log": store.lon,
                'success': True
                },
                HttpCreated
            )
        else:
            return self.create_response(
                request,
                {'success': False, 'message': 'User do not have access'},
                HttpUnauthorized
            )

    def get_store(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        self.is_authenticated(request)
        store_id = kwargs['pk']
        username = request.user
        custom_user_obj = self.get_custom_user(username)
        if custom_user_obj.role == "Merchant":
            try:
                obj = Store.objects.get(id=store_id)
                store_details = {
                    "id": obj.id,
                    "name": obj.name,
                    "city": obj.city,
                    "Address": obj.address,
                    "lat": obj.lat,
                    "log": obj.lon
                }
                return self.create_response(request, {
                    'success': True,
                    'store_details': store_details
                })

            except Store.DoesNotExist:
                return self.create_response(request, {
                    'message': "Resource not found"
                }, HttpNotFound)

        else:
            return self.create_response(
                request,
                {'success': False, 'message': 'User do not have access'},
                HttpUnauthorized
            )

    def get_stores(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        self.is_authenticated(request)
        username = request.user
        custom_user_obj = self.get_custom_user(username)
        if custom_user_obj.role == "Merchant":
            store_objs = Store.objects.filter(merchant=custom_user_obj)
            store_details = []
            for obj in store_objs:
                store = {
                    "id": obj.id,
                    "name": obj.name,
                    "city": obj.city,
                    "Address": obj.address,
                    "lat": obj.lat,
                    "log": obj.lon,
                }
                store_details.append(store)
            return self.create_response(
                request,
                {'stores': store_details, 'success': True}
            )

        else:
            return self.create_response(
                request,
                {'success': False, 'message': 'User do not have access'},
                HttpUnauthorized
            )

    def update_store(self, request, **kwargs):
        self.method_check(request, allowed=['put'])
        self.is_authenticated(request)
        data = self.deserialize(request, request.body, format=request.META.get(
            'CONTENT_TYPE', 'application/json'))
        store_id = kwargs['pk']
        username = request.user
        custom_user_obj = self.get_custom_user(username)
        if custom_user_obj.role == "Merchant":
            try:
                obj = Store.objects.get(id=store_id)
                obj.name = data['name']
                obj.city = data['city']
                obj.address = data['address']
                obj.lat = data['lat']
                obj.lon = data['lon']
                obj.save()
                return self.create_response(request, {
                    'success': True
                })

            except Store.DoesNotExist:
                Store.objects.create(
                    name=data['name'],
                    city=data['city'],
                    address=data['address'],
                    lat=data['lat'],
                    lon=data['lon'],
                    merchant=custom_user_obj
                )

                return self.create_response(request, {
                    'success': "True"
                }, HttpCreated)
        else:
            return self.create_response(
                request,
                {'success': False, 'message': 'User do not have access'},
                HttpUnauthorized
            )

    def delete_store(self, request, **kwargs):
        self.method_check(request, allowed=['delete'])
        self.is_authenticated(request)
        store_id = kwargs['pk']
        username = request.user
        custom_user_obj = self.get_custom_user(username)
        if custom_user_obj.role == "Merchant":
            try:
                obj = Store.objects.get(id=store_id)
                obj.delete()
                return self.create_response(request, {
                    'success': True
                })
            except Store.DoesNotExist:
                return self.create_response(request, {
                    'message': "Resource not found"
                    }, HttpNotFound
                )
        else:
            return self.create_response(
                request,
                {'success': False, 'message': 'User do not have access'},
                HttpUnauthorized
            )


class ItemResource(ModelResource, CommonMethods):

    store = fields.ToManyField(StoreResource, 'store', full=True)

    class Meta:
        queryset = Item.objects.all()
        resource_name = "item"
        allowed_methods = ['get', 'post', 'put', 'patch', 'delete']
        authentication = ApiKeyAuthentication()
        authorization = Authorization()

    def prepend_urls(self):

        return [
            url(r"^get_stores/(?P<store_pk>.*)/create_item/$", self.wrap_view('create_item'), name='create_store'),
            url(r"^get_stores/(?P<store_pk>.*)/get_items/(?P<item_pk>.*?)/$", self.wrap_view('get_item'), name='get_item'),
            url(r"^get_stores/(?P<store_pk>.*?)/update_item/(?P<item_pk>.*?)/$", self.wrap_view('update_item'), name='update_item'),
            url(r"^get_stores/(?P<store_pk>.*?)/delete_item/(?P<item_pk>.*?)/$", self.wrap_view('delete_item'), name='delete_item'),
            url(r"^get_stores/(?P<store_pk>.*?)/get_items/$", self.wrap_view('get_items'), name='get_items'),
        ]

    def create_item(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        self.is_authenticated(request)
        data = self.deserialize(request, request.body, format=request.META.get(
            'CONTENT_TYPE', 'application/json'))
        username = request.user
        custom_user_obj = self.get_custom_user(username)
        store_id = kwargs['store_pk']
        if custom_user_obj.role == "Merchant":
            item_obj = Item(**data)
            item_obj.save()
            StoreItem.objects.create(store_id=store_id, item=item_obj)
            return self.create_response(request, {
                'success': True
                },
                HttpCreated
            )
        else:
            return self.create_response(
                request,
                {'success': False, 'message': 'User do not have access'},
                HttpUnauthorized
            )

    def get_item(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        self.is_authenticated(request)
        store_id = kwargs['store_pk']
        item_id = kwargs['item_pk']
        try:
            store_item_obj = StoreItem.objects.get(item_id=item_id, store_id=store_id)
            item_obj = Item.objects.get(id=item_id)
            item_details = {
                "id": item_obj.id,
                "name": item_obj.name,
                "description": item_obj.description,
                "price": item_obj.price,
                "food_type": item_obj.food_type,
                "store_id": store_item_obj.store_id
            }
            return self.create_response(request, {
                'success': True,
                'item_details': item_details
            })
        except StoreItem.DoesNotExist:
            return self.create_response(request, {
                'message': "Item not found in the store"
            }, HttpNotFound)

    def get_items(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        self.is_authenticated(request)
        store_id = kwargs['store_pk']
        try:
            store_obj = Store.objects.prefetch_related('items').get(id=store_id)
            store_details = {
                "id": store_obj.id,
                "name": store_obj.name,
                "city": store_obj.city,
                "address": store_obj.address,
                "lat": store_obj.lat,
                "lon": store_obj.lon
            }
            items = []
            for item_obj in store_obj.items.all():
                item = {
                    "id": item_obj.id,
                    "name": item_obj.name,
                    "description": item_obj.description,
                    "price": item_obj.price,
                    "food_type": item_obj.food_type,
                }
                items.append(item)
            return self.create_response(request, {
                'items': items,
                'store_details': store_details,
                'success': "True"
            })
        except Store.DoesNotExist:
            return self.create_response(request, {
                'message': "Store not found"
            }, HttpNotFound)

    def update_item(self, request, **kwargs):
        store_id = kwargs['store_pk']
        item_id = kwargs['item_pk']
        self.method_check(request, allowed=['put'])
        self.is_authenticated(request)
        data = self.deserialize(request, request.body, format=request.META.get(
            'CONTENT_TYPE', 'application/json'))
        username = request.user
        custom_user_obj = self.get_custom_user(username)
        if custom_user_obj.role == "Merchant":
            try:
                store_item_obj = StoreItem.objects.get(store_id=store_id, item_id=item_id)
                item_obj = Item.objects.get(id=item_id)
                if data['new_store_id']:
                    store_item_obj.store_id = data["new_store_id"]
                    store_item_obj.save()
                item_obj.name = data['name']
                item_obj.description = data["description"]
                item_obj.price = data["price"]
                item_obj.food_type = data["food_type"]
                item_obj.save()
                return self.create_response(
                    request,
                    {'success': True}
                )
            except StoreItem.DoesNotExist:
                return self.create_response(
                    request,
                    {'success': False, 'message': 'Item not found in store'},
                    HttpNotFound
                )
        else:
            return self.create_response(
                request,
                {'success': False, 'message': 'User do not have access'},
                HttpUnauthorized
            )

    def delete_item(self, request, **kwargs):
        store_id = kwargs['store_pk']
        item_id = kwargs['item_pk']
        self.method_check(request, allowed=['delete'])
        self.is_authenticated(request)
        username = request.user
        custom_user_obj = self.get_custom_user(username)
        if custom_user_obj.role == "Merchant":
            try:
                StoreItem.objects.get(store_id=store_id, item_id=item_id)
                Item.objects.get(id=item_id).delete()
                return self.create_response(
                    request,
                    {'success': True}
                )
            except StoreItem.DoesNotExist:
                return self.create_response(
                    request,
                    {'success': False, 'message': 'Item not found in store'},
                    HttpNotFound
                )
        else:
            return self.create_response(
                request,
                {'success': False, 'message': 'User do not have access'},
                HttpUnauthorized
            )


class OrderResource(ModelResource, CommonMethods):

    user = fields.ToOneField(CustomUserResource, 'user', full=True)
    merchant = fields.ToOneField(CustomUserResource, 'merchant', full=True)
    store = fields.ToOneField(StoreResource, 'store', full=True)
    items = fields.ToManyField(ItemResource, 'items', full=True)

    class Meta:
        queryset = Order.objects.all()
        resource_name = "order"
        allowed_methods = ['post', 'get']
        authentication = ApiKeyAuthentication()
        authorization = Authorization()

    def prepend_urls(self):

        return [
            url(r"^create_order/$", self.wrap_view('create_order'), name='create_order'),
            url(r"^get_orders/(?P<pk>.*?)/$", self.wrap_view('get_order'), name='get_order'),
            url(r"^get_orders/$", self.wrap_view('get_orders'), name='get_orders'),
            url(r"^all_orders/$", self.wrap_view('all_orders'), name='all_orders'),
        ]

    def create_order(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        self.is_authenticated(request)
        data = self.deserialize(request, request.body, format=request.META.get(
            'CONTENT_TYPE', 'application/json'))
        username = request.user
        custom_user_obj = self.get_custom_user(username)
        item_ids = data['item_ids']  # Assuming all the items are in db
        store_id = data['store_id']  # Assuming store is in db
        store_obj = Store.objects.get(id=store_id)
        merchant_obj = store_obj.merchant

        order_obj = Order.objects.create(store=store_obj, merchant=merchant_obj, user=custom_user_obj)
        orders_list = []
        for item_id in item_ids:
            OrderItem(order=order_obj, item_id=item_id)
        OrderItem.objects.bulk_create(orders_list)

        return self.create_response(
                    request,
                    {'order_id': order_obj.id, 'success': True}
                )










