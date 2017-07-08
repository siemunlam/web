# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-08 15:48
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auxilios', '0004_auto_20170708_1038'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='solicituddeauxilio',
            name='contacto_solicitante',
        ),
        migrations.AddField(
            model_name='solicituddeauxilio',
            name='cantidad_pacientes',
            field=models.SmallIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AddField(
            model_name='solicituddeauxilio',
            name='contacto',
            field=models.CharField(blank=True, max_length=120, verbose_name='contacto'),
        ),
        migrations.AddField(
            model_name='solicituddeauxilio',
            name='nombre',
            field=models.CharField(blank=True, max_length=120),
        ),
        migrations.AddField(
            model_name='solicituddeauxilio',
            name='sexo',
            field=models.CharField(blank=True, choices=[('F', 'F'), ('M', 'M')], max_length=1),
        ),
        migrations.AddField(
            model_name='solicituddeauxilio',
            name='ubicacion_coordenadas',
            field=models.CharField(blank=True, max_length=120, verbose_name='ubicación coordenadas'),
        ),
        migrations.AddField(
            model_name='solicituddeauxilio',
            name='ubicacion_especifica',
            field=models.CharField(blank=True, max_length=120, verbose_name='ubicación especifica'),
        ),
    ]
