# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-27 18:26
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auxilios', '0009_auto_20170726_2028'),
    ]

    operations = [
        migrations.CreateModel(
            name='EstadoAuxilio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('estado', models.CharField(choices=[('1', 'Pendiente'), ('2', 'En curso'), ('3', 'Cancelado'), ('4', 'Finalizado')], default='1', max_length=1)),
                ('generador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Estado de auxilio',
                'ordering': ['-id'],
            },
        ),
        migrations.RemoveField(
            model_name='auxilio',
            name='estado',
        ),
        migrations.AddField(
            model_name='auxilio',
            name='estados',
            field=models.ManyToManyField(to='auxilios.EstadoAuxilio'),
        ),
    ]
