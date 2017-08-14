# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import CASCADE, CharField, ForeignKey, Model, OneToOneField, PositiveIntegerField, PositiveSmallIntegerField


# Create your models here.
User = get_user_model()

class Medico(Model):
	DISPONIBLE = 1
	NO_DISPONIBLE = 2
	EN_AUXILIO = 3
	ESTADO_CHOICES = (
		(DISPONIBLE, 'Disponible'),
		(NO_DISPONIBLE, 'No disponible'),
		(EN_AUXILIO, 'En auxilio')
	)

	dni = PositiveIntegerField(primary_key=True, verbose_name='DNI', validators=[MaxValueValidator(99999999), MinValueValidator(1000000)])
	matricula = PositiveIntegerField(unique=True, verbose_name=u'matrícula')
	telefono = CharField(max_length=15, verbose_name=u'teléfono')
	usuario = OneToOneField(User, related_name='medico_usuario', on_delete=CASCADE)
	fcm_code = CharField(max_length=250, blank=True, verbose_name='FCM', help_text='Firebase Cloud Messaging Code')
	estado = PositiveSmallIntegerField(choices = ESTADO_CHOICES, default = NO_DISPONIBLE)
	generador = ForeignKey(User, related_name='medico_generador')

	def __str__(self):
		return self.usuario.get_full_name() + str(self.matricula)

	class Meta:
		ordering = ['dni']
		verbose_name = u'médico'
		verbose_name_plural = u'médicos'