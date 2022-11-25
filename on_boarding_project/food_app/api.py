from tastypie import fields
from tastypie.authentication import BasicAuthentication, ApiKeyAuthentication
from tastypie.authorization import Authorization
from tastypie.resources import ModelResource, ALL
from .models import *
from django.contrib.auth import get_user_model
from django.conf.urls import url, include
from tastypie.utils import trailing_slash

User = get_user_model()


class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = "user"
        fields = ["username", "first_name", "last_name", "last_login", "email"]
        allowed_methods = ["get", "post", "put", "delete"]
        authorization = Authorization()


class MerchantAuthorization(Authorization):

    def read_list(self, object_list, bundle):
        return object_list.filter(owner=bundle.request.user)

    def read_detail(self, object_list, bundle):
        obj = object_list[0]
        return obj.owner == bundle.request.user


class MerchantResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'owner')

    class Meta:
        queryset = Merchant.objects.all()
        resource_name = "merchant"
        filtering = {
            'name': ALL,
        }
        allowed_methods = ['get', 'post', 'put', 'patch', 'delete']
        authorization = MerchantAuthorization()
        authentication = ApiKeyAuthentication()

    def hydrate(self, bundle):
        bundle.obj.user = bundle.request.user
        return bundle



    def override_urls(self):  # prepend_urls in 0.9.12
        return [
            url(r'^(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)/store%s$' % (
                self._meta.resource_name, trailing_slash()),
                self.wrap_view('dispatch_child'),
                name='api_parent_child'),
        ]

    def dispatch_child(self, request, **kwargs):
        return StoreResource().dispatch('list', request, **kwargs)


class ItemResource(ModelResource):
    class Meta:
        queryset = Item.objects.all()
        resource_name = "item"


class StoreResource(ModelResource):
    merchant = fields.ForeignKey(MerchantResource, 'merchant', full=True)
    items = fields.ToManyField(ItemResource, 'items', full=True)

    class Meta:
        queryset = Store.objects.all()
        resource_name = "store"


class StoreItemResource(ModelResource):

    store = fields.ForeignKey(StoreResource, "store")
    item = fields.ForeignKey(ItemResource, "item")

    class Meta:
        queryset = StoreItem.objects.all()
        resource_name = "storeitem"


