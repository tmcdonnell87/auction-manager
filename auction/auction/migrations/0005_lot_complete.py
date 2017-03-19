# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-13 22:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auction', '0004_auto_20170307_0728'),
    ]

    operations = [
        migrations.AddField(
            model_name='lot',
            name='complete',
            field=models.BooleanField(default=False, help_text='The lot description and items are complete based on donation form'),
        ),
    ]
