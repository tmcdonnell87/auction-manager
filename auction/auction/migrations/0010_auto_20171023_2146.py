# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2017-10-24 04:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auction', '0009_auto_20171023_2116'),
    ]

    operations = [
        migrations.AddField(
            model_name='donation',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='donation',
            name='delivery_method',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='donation',
            name='inactive_reason',
            field=models.TextField(blank=True, max_length=255, null=True),
        ),
    ]
