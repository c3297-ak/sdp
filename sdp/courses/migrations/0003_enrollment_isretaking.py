# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-03 06:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_auto_20161202_2210'),
    ]

    operations = [
        migrations.AddField(
            model_name='enrollment',
            name='isRetaking',
            field=models.BooleanField(default=False),
        ),
    ]
