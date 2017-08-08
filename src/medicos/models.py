# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import CASCADE, CharField, ForeignKey, Model, OneToOneField, PositiveIntegerField


# Create your models here.
User = get_user_model()

class Medico(Model):
	dni = PositiveIntegerField(primary_key=True, verbose_name='DNI')
	matricula = PositiveIntegerField(unique=True, verbose_name=u'matrícula')
	telefono = CharField(max_length=15, verbose_name=u'teléfono')
	usuario = OneToOneField(User, related_name='medico_usuario', on_delete=CASCADE)
	fcm_code = CharField(max_length=250, blank=True, verbose_name='FCM', help_text='Firebase Cloud Messaging Code')
	generador = ForeignKey(User, related_name='medico_generador')

	def __str__(self):
		return self.usuario.get_full_name() + str(self.matricula)

	class Meta:
		ordering = ['dni']
		verbose_name = u'Médico'
		verbose_name_plural = u'Médicos'