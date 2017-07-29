# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-29 17:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auxilios', '0010_auto_20170727_1526'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='auxilio',
            options={'ordering': ['-categoria', 'prioridad'], 'verbose_name': 'Auxilio'},
        ),
        migrations.AddField(
            model_name='auxilio',
            name='prioridad',
            field=models.PositiveSmallIntegerField(default=25),
            preserve_default=False,
        ),
    ]
