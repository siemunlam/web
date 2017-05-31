# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import models

# Create your models here.
class Categoria(models.Model):
	descripcion = models.CharField(verbose_name=u'descripción', max_length=25, unique=True)
	prioridad = models.PositiveSmallIntegerField(unique=True)
	color = models.CharField(max_length=6, unique=True)
	fue_anulado = models.BooleanField(default=False)

	def __str__(self):
		return self.descripcion

	class Meta:
		ordering = ['prioridad']
		verbose_name = 'categoría'
		verbose_name_plural = 'categorías'


class Ajuste(models.Model):
	valor = models.SmallIntegerField(unique=True)
	fue_anulado = models.BooleanField(default=False)

	def __str__(self):
		return self.valor

	class Meta:
		ordering = ['valor']
		verbose_name_plural = 'ajustes'


class FactorDeAjuste(models.Model):
	descripcion = models.CharField(verbose_name=u'descripción', max_length=50, unique=True)
	fue_anulado = models.BooleanField(default=False)

	def __str__(self):
		return self.descripcion

	class Meta:
		ordering = ['descripcion']
		verbose_name = 'factor de ajuste'
		verbose_name_plural = 'factores de ajuste'


class FactorDePreCategorizacion(models.Model):
	descripcion = models.CharField(verbose_name=u'descripción', max_length=50, unique=True)
	fue_anulado = models.BooleanField(default=False)

	def __str__(self):
		return self.descripcion

	class Meta:
		ordering = ['descripcion']
		verbose_name = 'factor de pre-categorización'
		verbose_name_plural = 'factores de pre-categorización'


class ValorDeFactorDeAjuste(models.Model):
	descripcion = models.CharField(verbose_name=u'descripción', max_length=50, unique=True)
	factorDeAjuste = models.ForeignKey(FactorDeAjuste)
	fue_anulado = models.BooleanField(default=False)

	def __str__(self):
		return self.factorDeAjuste.descripcion +" > "+ self.descripcion

	class Meta:
		ordering = ['descripcion']
		verbose_name = 'Valor de factor de ajuste'
		verbose_name_plural = 'Valores de factor de ajuste'


class ValorDeFactorDePreCategorizacion(models.Model):
	descripcion = models.CharField(verbose_name=u'descripción', max_length=50, unique=True)
	factorDePreCategorizacion = models.ForeignKey(FactorDePreCategorizacion)
	fue_anulado = models.BooleanField(default=False)
	
	def __str__(self):
		return self.factorDePreCategorizacion.descripcion +" > "+ self.descripcion

	class Meta:
		ordering = ['descripcion']
		verbose_name = 'Valor de factor de pre-categorización'
		verbose_name_plural = 'Valores de factor de pre-categorización'


class ReglaDeAjuste(models.Model):
	condicion = models.ForeignKey(ValorDeFactorDeAjuste)
	resultado = models.ForeignKey(Ajuste)
	prioridad = models.PositiveSmallIntegerField()
	fue_anulado = models.BooleanField(default=False)

	def __str__(self):
		return "Regla "+ self.id +": IF "+ self.condicion +" => AJUSTE:"+ self.resultado

	class Meta:
		ordering = ['id']
		unique_together = ('resultado', 'prioridad')
		verbose_name = 'Regla de ajuste'
		verbose_name_plural = 'Reglas de ajuste'


class ReglaDePreCategorizacion(models.Model):
	condicion = models.ForeignKey(ValorDeFactorDePreCategorizacion)
	resultado = models.ForeignKey(Categoria)
	prioridad = models.PositiveSmallIntegerField()
	fue_anulado = models.BooleanField(default=False)

	def __str__(self):
		return "Regla "+ self.id +": IF "+ self.condicion +" => PRECATEGORIZACION:"+ self.resultado

	class Meta:
		ordering = ['id']
		unique_together = ('resultado', 'prioridad')
		verbose_name = 'Regla de pre-categorización'
		verbose_name_plural = 'Reglas de pre-categorización'
