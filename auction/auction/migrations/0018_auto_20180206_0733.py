# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-02-06 15:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auction', '0017_auto_20180120_0858'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='location',
            field=models.CharField(choices=[('OFFICE', 'Guardsmen Office'), ('SFWC', 'SF Wine Center'), ('OTHER', 'Other'), ('PICKUP', 'Pickup Required')], default='OTHER', help_text='Where the item is currently located', max_length=40),
        ),
        migrations.AlterField(
            model_name='lot',
            name='lot_number',
            field=models.PositiveSmallIntegerField(db_index=True),
        ),
    ]
