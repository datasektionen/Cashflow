# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2024-09-24 21:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expenses', '0024_auto_20240516_1926'),
    ]

    operations = [
        migrations.CreateModel(
            name='FortnoxAuthToken',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('access_token', models.TextField()),
                ('refresh_token', models.TextField()),
                ('expires_at', models.DateTimeField()),
            ],
        ),
    ]