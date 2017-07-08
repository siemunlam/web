# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import models


# Create your models here.
class SolicitudDeAuxilio(models.Model):
	FEMENINO = 'F'
	MASCULINO = 'M'
	SEXO_CHOICES = (
		(FEMENINO, 'F'),
		(MASCULINO, 'M')
	)
	fecha = models.DateTimeField(auto_now_add=True)
	nombre = models.CharField(max_length=120, blank=True)
	sexo = models.CharField(
		max_length = 1,
		choices = SEXO_CHOICES,
		blank = True
	)
	cantidad_pacientes = models.PositiveSmallIntegerField(default=1)
	ubicacion = models.CharField(verbose_name=u'ubicación', max_length=120)
	ubicacion_especifica = models.CharField(verbose_name=u'ubicación especifica', max_length=120, blank=True)
	ubicacion_coordenadas = models.CharField(verbose_name=u'ubicación coordenadas', max_length=120, blank=True)
	contacto = models.CharField(verbose_name=u'contacto', max_length=120, blank=True)
	motivo = models.TextField()
	observaciones = models.CharField(max_length=120, blank=True)
	generador = models.ForeignKey(settings.AUTH_USER_MODEL)
	
	def __str__(self):
		return self.id

	class Meta:
		ordering = ['-id']
		verbose_name = 'Solicitud de auxilio'
		verbose_name_plural = 'Solicitudes de auxilio'
