# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-03 16:02
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rules', '0012_auto_20170611_1531'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='categoria',
            name='fue_anulado',
        ),
        migrations.RemoveField(
            model_name='factordeajuste',
            name='fue_anulado',
        ),
        migrations.RemoveField(
            model_name='factordeprecategorizacion',
            name='fue_anulado',
        ),
        migrations.RemoveField(
            model_name='regladeajuste',
            name='fue_anulado',
        ),
        migrations.RemoveField(
            model_name='regladeprecategorizacion',
            name='fue_anulado',
        ),
        migrations.RemoveField(
            model_name='valordefactordeajuste',
            name='fue_anulado',
        ),
        migrations.RemoveField(
            model_name='valordefactordeprecategorizacion',
            name='fue_anulado',
        ),
    ]
