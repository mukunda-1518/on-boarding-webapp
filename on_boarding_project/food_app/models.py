# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import uuid

from django.db import models
from django.contrib.auth.models import User

FOOD_CHOICES = [
    ("Veg", "Vegetarian"),
    ("Non-Veg", "Non-Vegetarian"),
]

ROLES = [
    ("Merchant", "Merchant"),
    ("Consumer", "Consumer")
]


class CustomUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, unique=True)
    role = models.CharField(max_length=100, choices=ROLES)
    profile_pic = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.name


class Store(models.Model):
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    address = models.TextField()
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    lon = models.DecimalField(max_digits=9, decimal_places=6)
    merchant = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.FloatField()
    food_type = models.CharField(max_length=30, choices=FOOD_CHOICES)
    store = models.ManyToManyField(Store, through='StoreItem', related_name="items")

    def __str__(self):
        return self.name


class StoreItem(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return "{} - {}".format(self.store, self.item)


class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="order_user")
    merchant = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="order_merchant")
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    items = models.ManyToManyField(Item, through="OrderItem", related_name="orders")

    def __str__(self):
        return "order - {}".format(self.id)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)

    def __str__(self):
        return "order:{} - item:{}".format(self.order.id, self.item.id)
