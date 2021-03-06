# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-12 17:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auxilios', '0027_auto_20170911_1703'),
    ]

    operations = [
        migrations.CreateModel(
            name='Suscriptor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(blank=True, help_text='Firebase Cloud Messaging Code', max_length=250, verbose_name='código')),
                ('added', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Suscriptores',
                'ordering': ['-added'],
            },
        ),
        migrations.AddField(
            model_name='auxilio',
            name='suscriptores',
            field=models.ManyToManyField(blank=True, to='auxilios.Suscriptor'),
        ),
    ]
