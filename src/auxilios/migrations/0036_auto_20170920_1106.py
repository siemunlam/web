# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-20 14:06
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auxilios', '0035_auto_20170920_1041'),
    ]

    operations = [
        migrations.RenameField(
            model_name='paciente',
            old_name='motivo_atencion',
            new_name='diagnostico',
        ),
    ]
