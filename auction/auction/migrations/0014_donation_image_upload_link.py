# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2017-11-12 23:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auction', '0013_auto_20171112_1305'),
    ]

    operations = [
        migrations.AddField(
            model_name='donation',
            name='image_upload_link',
            field=models.URLField(blank=True, null=True),
        ),
    ]
