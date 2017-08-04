# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-04 20:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auxilios', '0013_auto_20170804_1527'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medico',
            name='dni',
            field=models.PositiveIntegerField(primary_key=True, serialize=False, verbose_name='DNI'),
        ),
        migrations.AlterField(
            model_name='medico',
            name='matricula',
            field=models.PositiveIntegerField(verbose_name='Matrícula'),
        ),
        migrations.AlterField(
            model_name='medico',
            name='sexo',
            field=models.CharField(choices=[('F', 'F'), ('M', 'M')], max_length=1),
        ),
        migrations.AlterField(
            model_name='medico',
            name='telefono',
            field=models.CharField(max_length=15, verbose_name='teléfono'),
        ),
    ]
