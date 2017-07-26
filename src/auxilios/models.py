# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models

from rules.models import Categoria


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
	cantidad_moviles = models.PositiveSmallIntegerField(default=1, validators=[MinValueValidator(1)])
	ubicacion = models.CharField(verbose_name=u'ubicación', max_length=120)
	ubicacion_especifica = models.CharField(verbose_name=u'ubicación especifica', max_length=120, blank=True)
	ubicacion_coordenadas = models.CharField(verbose_name=u'ubicación coordenadas', max_length=120)
	contacto = models.CharField(verbose_name=u'contacto', max_length=120, blank=True)
	motivo = models.TextField()
	observaciones = models.CharField(max_length=120, blank=True)
	generador = models.ForeignKey(settings.AUTH_USER_MODEL)
	
	def __str__(self):
		return str(self.id)

	class Meta:
		ordering = ['-id']
		verbose_name = 'Solicitud de auxilio'
		verbose_name_plural = 'Solicitudes de auxilio'


class Movil(models.Model):
	DISPONIBLE = '1'
	NO_DISPONIBLE = '2'
	EN_AUXILIO = '3'
	ESTADO_CHOICES = (
		(DISPONIBLE, 'Disponible'),
		(NO_DISPONIBLE, 'No disponible'),
		(EN_AUXILIO, 'En auxilio')
	)
	estado = models.CharField(
		max_length = 1,
		choices = ESTADO_CHOICES,
		default = NO_DISPONIBLE
	)
	patente = models.CharField(max_length=10)
	generador = models.ForeignKey(settings.AUTH_USER_MODEL)

	class Meta:
		ordering = ['-id']
		verbose_name = u'Móvil'
		verbose_name_plural = u'Móviles'


class Asignacion(models.Model):
	EN_CAMINO = '1'
	EN_LUGAR = '2'
	CANCELADA = '3'
	EN_TRASLADO = '4'
	ESTADO_CHOICES = (
		(EN_CAMINO, 'En camino'),
		(EN_LUGAR, 'En el lugar'),
		(CANCELADA, 'Cancelada'),
		(EN_TRASLADO, 'En traslado')
	)
	movil = models.ForeignKey('Movil')
	estado = models.CharField(
		max_length = 1,
		choices = ESTADO_CHOICES,
		default = EN_CAMINO
	)
	generador = models.ForeignKey(settings.AUTH_USER_MODEL)

	def __str__(self):
		return self.id

	class Meta:
		ordering = ['id']
		verbose_name = u'Asignación'
		verbose_name_plural = u'Asignaciones'


class Auxilio(models.Model):
	PENDIENTE = '1'
	EN_CURSO = '2'
	CANCELADO = '3'
	FINALIZADO = '4'
	ESTADO_CHOICES = (
		(PENDIENTE, 'Pendiente'),
		(EN_CURSO, 'En curso'),
		(CANCELADO, 'Cancelado'),
		(FINALIZADO, 'Finalizado')
	)
	estado = models.CharField(
		max_length = 1,
		choices = ESTADO_CHOICES,
		default = PENDIENTE
	)
	solicitud = models.ForeignKey(SolicitudDeAuxilio)
	categoria = models.ForeignKey(Categoria)
	asignaciones = models.ManyToManyField(Asignacion, blank=True)

	class Meta:
		ordering = ['-id']
		verbose_name = 'Auxilio'


class Medico(models.Model):
	dni = models.CharField(max_length=10)
	matricula = models.CharField(max_length=10)
	nombre = models.CharField(max_length=50)
	apellido = models.CharField(max_length=50)
	sexo = models.CharField(max_length=2)
	telefono = models.CharField(max_length=15)
	fcmc = models.CharField(max_length=256, blank=True, verbose_name='Firebase Cloud Messaging Code')
	generador = models.ForeignKey(settings.AUTH_USER_MODEL)

	class Meta:
		ordering = ['-id']
		verbose_name = u'Médico'
		verbose_name_plural = u'Médicos'