# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

FOOD_CHOICES = [
    ("Veg", "Vegetarian"),
    ("Non-Veg", "Non-Vegetarian"),
]


class Merchant(models.Model):
    owner = models.ForeignKey(User, null=True)  # It can be one-to-one or foreignkey relationship based on the usecase
    name = models.CharField(max_length=100)
    description = models.TextField()
    origin = models.CharField(max_length=100)


class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.FloatField()
    food_type = models.CharField(max_length=30, choices=FOOD_CHOICES)


class Store(models.Model):
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    address = models.TextField()
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    lon = models.DecimalField(max_digits=9, decimal_places=6)
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE)
    items = models.ManyToManyField(Item, through='StoreItem')


class StoreItem(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    is_available = models.BooleanField(default=True)






