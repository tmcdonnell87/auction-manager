# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2017-10-24 04:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auction', '0010_auto_20171023_2146'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donation',
            name='inactive_reason',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
