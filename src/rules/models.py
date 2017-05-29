# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import models

# Create your models here.
class Categoria(models.Model):
	descripcion = models.CharField(verbose_name=u'descripción', max_length=25, unique=True)
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
	descripcion = models.CharField(verbose_name=u'descripción', max_length=50, unique=True)

	def __str__(self):
		return self.descripcion

	class Meta:
		ordering = ['descripcion']
		verbose_name = 'factor de ajuste'
		verbose_name_plural = 'factores de ajuste'


class FactorDeCategorizacion(models.Model):
	descripcion = models.CharField(verbose_name=u'descripción', max_length=50, unique=True)

	def __str__(self):
		return self.descripcion

	class Meta:
		ordering = ['descripcion']
		verbose_name = 'factor de categorización'
		verbose_name_plural = 'factores de categorización'


class ValorPosibleDeAjuste(models.Model):
	descripcion = models.CharField(verbose_name=u'descripción', max_length=50, unique=True)
	factorDeAjuste = models.ForeignKey(FactorDeAjuste)

	def __str__(self):
		return self.factorDeAjuste.descripcion +" > "+ self.descripcion

	class Meta:
		ordering = ['descripcion']
		verbose_name = 'Valor posible de factor de ajuste'
		verbose_name_plural = 'Valores posibles de factores de ajuste'


class ValorPosibleDeCategorizacion(models.Model):
	descripcion = models.CharField(verbose_name=u'descripción', max_length=50, unique=True)
	factorDeCategorizacion = models.ForeignKey(FactorDeCategorizacion)

	def __str__(self):
		return self.factorDeCategorizacion.descripcion +" > "+ self.descripcion

	class Meta:
		ordering = ['descripcion']
		verbose_name = 'Valor posible de factor de categorización'
		verbose_name_plural = 'Valores posibles de factores de categorización'


class ReglaDeAjuste(models.Model):
	condicion = models.ForeignKey(ValorPosibleDeAjuste)
	resultado = models.ForeignKey(Ajuste)

	def __str__(self):
		return "Regla "+ self.id +": IF "+ self.condicion +" => AJUSTE:"+ self.resultado

	class Meta:
		ordering = ['id']
		verbose_name = 'Regla de ajuste'
		verbose_name_plural = 'Reglas de ajuste'


class ReglaDePreCategorizacion(models.Model):
	condicion = models.ForeignKey(ValorPosibleDeCategorizacion)
	resultado = models.ForeignKey(Categoria)

	def __str__(self):
		return "Regla "+ self.id +": IF "+ self.condicion +" => PRECATEGORIZACION:"+ self.resultado

	class Meta:
		ordering = ['id']
		verbose_name = 'Regla de ajuste'
		verbose_name_plural = 'Reglas de ajuste'