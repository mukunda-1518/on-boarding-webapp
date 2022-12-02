# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import *

admin.site.register(CustomUser)
admin.site.register(Store)
admin.site.register(Item)
admin.site.register(StoreItem)
admin.site.register(Order)
admin.site.register(OrderItem)
