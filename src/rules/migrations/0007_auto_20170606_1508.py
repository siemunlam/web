# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-06 18:08
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rules', '0006_remove_ajuste_fue_anulado'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ajuste',
            options={'ordering': ['-valor'], 'verbose_name_plural': 'ajustes'},
        ),
    ]
