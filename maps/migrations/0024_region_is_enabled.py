# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-26 15:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maps', '0023_auto_20170423_1023'),
    ]

    operations = [
        migrations.AddField(
            model_name='region',
            name='is_enabled',
            field=models.BooleanField(default=True),
        ),
    ]