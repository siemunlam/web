# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model
from django.db.models import Model, ForeignKey, CharField, ManyToManyField, PositiveSmallIntegerField, DateTimeField, TextField
from django.core.validators import MinValueValidator
from rules.models import Categoria
from medicos.models import Medico

# Create your models here.
User = get_user_model()

class Asignacion(Model):
	PENDIENTE = '0'
	EN_CAMINO = '1'
	EN_LUGAR = '2'
	CANCELADA = '3'
	EN_TRASLADO = '4'
	DESVIADA = '5'
	FINALIZADA = '6'
	ESTADO_CHOICES = (
		(PENDIENTE, 'Pendiente'),
		(EN_CAMINO, 'En camino'),
		(EN_LUGAR, 'En el lugar'),
		(CANCELADA, 'Cancelada'),
		(EN_TRASLADO, 'En traslado'),
		(DESVIADA, 'Desviada'),
		(FINALIZADA, 'Finalizada')
	)
	medico = ForeignKey(Medico, null=True)
	estado = CharField(
		max_length = 1,
		choices = ESTADO_CHOICES,
		default = PENDIENTE
	)
	creada = DateTimeField(auto_now_add=True)
	modificada = DateTimeField(auto_now=True)

	def __str__(self):
		return self.id

	class Meta:
		ordering = ['-id']
		verbose_name = u'Asignación'
		verbose_name_plural = 'Asignaciones'


class Auxilio(Model):
	estados = ManyToManyField('EstadoAuxilio')
	solicitud = ForeignKey('SolicitudDeAuxilio')
	categoria = ForeignKey(Categoria)
	prioridad = PositiveSmallIntegerField(default=100)
	asignaciones = ManyToManyField('Asignacion', blank=True)

	class Meta:
		ordering = ['categoria', 'prioridad', 'solicitud']
		verbose_name = 'Auxilio'


class EstadoAuxilio(Model):
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

	fecha = DateTimeField(auto_now_add=True)
	estado = CharField(
		max_length = 1,
 		choices = ESTADO_CHOICES,
 		default = PENDIENTE
 	)

	class Meta:
		ordering = ['-id']
		verbose_name = 'Estado de auxilio'


class Movil(Model):
	DISPONIBLE = '1'
	NO_DISPONIBLE = '2'
	EN_AUXILIO = '3'
	ESTADO_CHOICES = (
		(DISPONIBLE, 'Disponible'),
		(NO_DISPONIBLE, 'No disponible'),
		(EN_AUXILIO, 'En auxilio')
	)
	estado = CharField(
		max_length = 1,
		choices = ESTADO_CHOICES,
		default = NO_DISPONIBLE
	)
	patente = CharField(max_length=10)
	generador = ForeignKey(User)

	class Meta:
		ordering = ['-id']
		verbose_name = u'Móvil'
		verbose_name_plural = u'Móviles'


class SolicitudDeAuxilio(Model):
	FEMENINO = 'F'
	MASCULINO = 'M'
	SEXO_CHOICES = (
		(FEMENINO, 'F'),
		(MASCULINO, 'M')
	)
	fecha = DateTimeField(auto_now_add=True)
	nombre = CharField(max_length=120, blank=True)
	sexo = CharField(
		max_length = 1,
		choices = SEXO_CHOICES,
		blank = True
	)
	cantidad_pacientes = PositiveSmallIntegerField(default=1, verbose_name=u'cantidad de pacientes', validators=[MinValueValidator(1)])
	cantidad_moviles = PositiveSmallIntegerField(default=1, help_text='Cantidad de médicos requeridos')
	ubicacion = CharField(verbose_name=u'ubicación', max_length=120)
	ubicacion_especifica = CharField(verbose_name=u'ubicación especifica', max_length=120, blank=True)
	ubicacion_coordenadas = CharField(verbose_name=u'ubicación coordenadas', max_length=120, blank=True)
	contacto = CharField(verbose_name=u'contacto', max_length=120, blank=True)
	motivo = TextField()
	observaciones = CharField(max_length=120, blank=True)
	generador = ForeignKey(User)
	
	def __str__(self):
		return str(self.id)

	class Meta:
		ordering = ['-id']
		verbose_name = 'Solicitud de auxilio'
		verbose_name_plural = 'Solicitudes de auxilio'