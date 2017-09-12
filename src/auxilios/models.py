# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import (BooleanField, CASCADE, CharField, DateField,
							  DateTimeField, ForeignKey, ManyToManyField,
							  Model, OneToOneField, PositiveIntegerField,
							  PositiveSmallIntegerField, TextField)

from rules.models import Categoria
from medicos.models import Medico
import random

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
	ESTADO_CHOICES = ((PENDIENTE, 'Pendiente'), (EN_CAMINO, 'En camino'),
					  (EN_LUGAR, 'En el lugar'), (CANCELADA, 'Cancelada'),
					  (EN_TRASLADO,
					   'En traslado'), (DESVIADA, 'Desviada'), (FINALIZADA,
																'Finalizada'))
	medico = ForeignKey(Medico, null=True)
	estado = CharField(max_length=1, choices=ESTADO_CHOICES, default=PENDIENTE)
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
	codigo_suscripcion = CharField(max_length=10, verbose_name=u'código de suscripción', unique=True)
	suscriptores = ManyToManyField('Suscriptor', blank=True)

	def save(self, *args, **kwargs):
		if not self.id:
			self.codigo_suscripcion = str(random.randint(0, 9999999999))
		super(Auxilio, self).save(*args, **kwargs)

	class Meta:
		ordering = ['categoria', 'prioridad', 'solicitud']
		verbose_name = 'Auxilio'


class EstadoAuxilio(Model):
	PENDIENTE = '1'
	EN_CURSO = '2'
	CANCELADO = '3'
	FINALIZADO = '4'
	ESTADO_CHOICES = ((PENDIENTE, 'Pendiente'), (EN_CURSO, 'En curso'),
					  (CANCELADO, 'Cancelado'), (FINALIZADO, 'Finalizado'))

	fecha = DateTimeField(auto_now_add=True)
	estado = CharField(max_length=1, choices=ESTADO_CHOICES, default=PENDIENTE)

	class Meta:
		ordering = ['-id']
		verbose_name = 'Estado de auxilio'


class Movil(Model):
	DISPONIBLE = '1'
	NO_DISPONIBLE = '2'
	EN_AUXILIO = '3'
	ESTADO_CHOICES = ((DISPONIBLE, 'Disponible'),
					  (NO_DISPONIBLE, 'No disponible'), (EN_AUXILIO,
														 'En auxilio'))
	estado = CharField(
		max_length=1, choices=ESTADO_CHOICES, default=NO_DISPONIBLE)
	patente = CharField(max_length=10)
	generador = ForeignKey(User)

	class Meta:
		ordering = ['-id']
		verbose_name = u'Móvil'
		verbose_name_plural = u'Móviles'


class SolicitudDeAuxilio(Model):
	FEMENINO = 'F'
	MASCULINO = 'M'
	SEXO_CHOICES = ((FEMENINO, 'F'), (MASCULINO, 'M'))
	fecha = DateTimeField(auto_now_add=True)
	nombre = CharField(max_length=120, blank=True)
	sexo = CharField(max_length=1, choices=SEXO_CHOICES, blank=True)
	cantidad_pacientes = PositiveSmallIntegerField(
		default=1,
		verbose_name=u'cantidad de pacientes',
		validators=[MinValueValidator(1)])
	cantidad_moviles = PositiveSmallIntegerField(
		default=1, help_text='Cantidad de médicos requeridos')
	ubicacion = CharField(verbose_name=u'ubicación', max_length=120)
	ubicacion_especifica = CharField(
		verbose_name=u'ubicación especifica', max_length=120, blank=True)
	ubicacion_coordenadas = CharField(
		verbose_name=u'ubicación coordenadas', max_length=120, blank=True)
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


class FormularioFinalizacion(Model):
	asignacion = OneToOneField(Asignacion, on_delete=CASCADE, primary_key=True)
	asistencia_realizada = BooleanField()
	observaciones = TextField(blank=True)
	# Asistencia realizada FALSE
	UBICACION_INCORRECTA = '1'
	NO_RESPONDE = '2'
	YA_FUE_TRANSLADADO = '3'
	OTRO = '4'
	INASISTENCIA_CHOICES = ((UBICACION_INCORRECTA, u'Ubicación incorrecta'),
							(NO_RESPONDE, 'No responde'),
							(YA_FUE_TRANSLADADO,
							 'Ya fue trasladado'), (OTRO, 'Otro'))
	motivo_inasistencia = CharField(
		max_length=1,
		choices=INASISTENCIA_CHOICES,
		help_text=u'¿Por qué no pudo asistir al paciente?',
		blank=True)
	# Asistencia realizada TRUE
	SOBRECATEGORIZADO = '1'
	CORRECTO = '2'
	SUBCATEGORIZADO = '3'
	OPINION_CHOICES = ((SUBCATEGORIZADO, 'Sub-categorizado'),
					   (CORRECTO, 'Apropiadamente categorizado'),
					   (SOBRECATEGORIZADO, 'Sobre-categorizado'))
	categorizacion = CharField(
		max_length=1,
		choices=OPINION_CHOICES,
		verbose_name=u'categorización',
		help_text=
		u'¿Cuál es su opinión acerca de la categorización del auxilio?',
		blank=True)
	pacientes = ManyToManyField('Paciente', blank=True)


class Paciente(Model):
	dni = PositiveIntegerField(
		verbose_name='DNI',
		validators=[MaxValueValidator(99999999),
					MinValueValidator(1000000)],
		blank=True,
		null=True)
	apellido = CharField(max_length=40, blank=True)
	nombre = CharField(max_length=40, blank=True)
	fecha_nacimiento = DateField(
		verbose_name='fecha de nacimiento', blank=True, null=True)
	telefono = CharField(max_length=15, verbose_name=u'teléfono', blank=True)
	# TODO: el motivo que sea seleccionable / parametrizable + un campo de detalle
	motivo_atencion = TextField()
	trasladado = BooleanField()


class Suscriptor(Model):
	codigo = CharField(
		max_length=250,
		blank=True,
		verbose_name=u'código',
		help_text='Firebase Cloud Messaging Code')
	added = DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.codigo

	class Meta:
		ordering = ['-added']
		verbose_name_plural = 'Suscriptores'