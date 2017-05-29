# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import models

# Create your models here.
class Categoria(models.Model):
	descripcion = models.CharField(verbose_name=u'descripción', max_length=30, unique=True)
	prioridad = models.PositiveSmallIntegerField(unique=True)
	color = models.CharField(max_length=6, unique=True)
	creado = models.DateTimeField(auto_now_add=True)
	modificado = models.DateTimeField(auto_now=True)
	modificado_por = models.ForeignKey(settings.AUTH_USER_MODEL)

	def __str__(self):
		return self.descripcion

	class Meta:
		ordering = ['prioridad']
		verbose_name = 'categoría'
		verbose_name_plural = 'categorías'


class Ajuste(models.Model):
	valor = models.SmallIntegerField(unique=True)

	def __str__(self):
		return self.valor

	class Meta:
		ordering = ['valor']
		verbose_name_plural = 'ajustes'


class FactorDeAjuste(models.Model):
	descripcion = models.CharField(verbose_name=u'descripción', max_length=30, unique=True)

	def __str__(self):
		return self.descripcion

	class Meta:
		ordering = ['descripcion']
		verbose_name = 'factor de ajuste'
		verbose_name_plural = 'factores de ajuste'


class Regla(models.Model):
	pass


class FactorDeCategorizacion(models.Model):
	descripcion = models.CharField(verbose_name=u'descripción', max_length=30, unique=True)

	def __str__(self):
		return self.descripcion

	class Meta:
		ordering = ['descripcion']
		verbose_name = 'factor de categorización'
		verbose_name_plural = 'factores de categorización'