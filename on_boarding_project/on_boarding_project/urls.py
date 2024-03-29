"""on_boarding_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from tastypie.api import Api
from django.contrib.auth.models import User
from django.db import models
from tastypie.models import create_api_key
# from food_app.api import MerchantResource, StoreItemResource, StoreResource, ItemResource, UserResource
from food_app.api import UserResource, StoreResource, ItemResource, OrderResource

v1_api = Api(api_name='v1')
v1_api.register(ItemResource())
v1_api.register(UserResource())
v1_api.register(StoreResource())
v1_api.register(OrderResource())

models.signals.post_save.connect(create_api_key, sender=User)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include(v1_api.urls))
]
