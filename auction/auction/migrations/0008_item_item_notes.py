# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2017-10-23 15:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auction', '0007_auto_20171023_0822'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='item_notes',
            field=models.TextField(blank=True, null=True),
        ),
    ]
