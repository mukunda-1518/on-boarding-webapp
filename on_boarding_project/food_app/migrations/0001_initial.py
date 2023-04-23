# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2022-11-24 10:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('price', models.FloatField()),
                ('food_type', models.CharField(choices=[('Veg', 'Vegetarian'), ('Non-Veg', 'Non-Vegetarian')], max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Merchant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('origin', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('address', models.TextField()),
                ('lat', models.DecimalField(decimal_places=6, max_digits=9)),
                ('lon', models.DecimalField(decimal_places=6, max_digits=9)),
            ],
        ),
        migrations.CreateModel(
            name='StoreItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_available', models.BooleanField(default=True)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='food_app.Item')),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='food_app.Store')),
            ],
        ),
        migrations.AddField(
            model_name='store',
            name='items',
            field=models.ManyToManyField(through='food_app.StoreItem', to='food_app.Item'),
        ),
        migrations.AddField(
            model_name='store',
            name='merchant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='food_app.Merchant'),
        ),
    ]
