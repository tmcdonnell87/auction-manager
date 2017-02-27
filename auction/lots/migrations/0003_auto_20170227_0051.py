# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-27 00:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lots', '0002_auto_20170226_0147'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wine',
            name='lot',
        ),
        migrations.AddField(
            model_name='wine',
            name='item',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='lots.Item'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='lot',
            name='cost',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
