# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2024-01-25 19:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expenses', '0022_auto_20240125_1843'),
    ]

    operations = [
        migrations.AddField(
            model_name='expense',
            name='is_digital',
            field=models.NullBooleanField(),
        ),
    ]
