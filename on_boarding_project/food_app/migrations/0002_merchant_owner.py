# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2022-11-25 11:06
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('food_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='merchant',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
