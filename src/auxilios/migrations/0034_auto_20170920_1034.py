# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-20 13:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auxilios', '0033_auto_20170920_1027'),
    ]

    operations = [
        migrations.AlterField(
            model_name='formulariofinalizacion',
            name='categorizacion',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(1, 'Sub-categorizado'), (0, 'Apropiadamente categorizado'), (2, 'Sobre-categorizado')], default=0, help_text='¿Cuál es su opinión acerca de la categorización del auxilio?', null=True, verbose_name='categorización'),
        ),
        migrations.AlterField(
            model_name='formulariofinalizacion',
            name='motivo_inasistencia',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(1, 'Ubicación incorrecta'), (2, 'No responde'), (3, 'Ya fue trasladado'), (0, 'Otro')], default=0, help_text='¿Por qué no pudo asistir al paciente?', null=True, verbose_name='motivo de inasistencia'),
        ),
    ]
