# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-23 16:29
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auxilios', '0020_auto_20170823_1323'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='estadoauxilio',
            name='generador',
        ),
    ]
