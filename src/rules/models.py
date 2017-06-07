# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import models
from django.db.models import Max, Min

from .extra_func import calcAjustesResultantes


# Create your models here.
class Categoria(models.Model):
	descripcion = models.CharField(verbose_name=u'descripción', max_length=25, unique=True)
	prioridad = models.PositiveSmallIntegerField(unique=True, default=0)
	color = models.CharField(max_length=7, unique=True)
	fue_anulado = models.BooleanField(default=False)

	def __str__(self):
		return self.descripcion

	class Meta:
		ordering = ['prioridad']
		verbose_name = 'categoría'
		verbose_name_plural = 'categorías'


class Ajuste(models.Model):
	valor = models.SmallIntegerField(unique=True)

	def __str__(self):
		return str(self.valor)

	class Meta:
		ordering = ['-valor']
		verbose_name_plural = 'ajustes'
	
	@staticmethod
	def crearAjustes(self, ajustesResultantes):
		cantAjustesACrear = ajustesResultantes - Ajuste.objects.count()
		if cantAjustesACrear == 3:
			ajuste_cero = Ajuste(valor = 0)
			ajuste_cero.save()
		if cantAjustesACrear > 0:
			max_valor = Ajuste.objects.aggregate(Max('valor'))['valor__max']
			ajuste_positivo = Ajuste(valor = max_valor + 1)
			ajuste_positivo.save()
			ajuste_negativo = Ajuste(valor = - max_valor - 1)
			ajuste_negativo.save()
		return cantAjustesACrear
	
	@staticmethod
	def borrarAjustes(self, ajustesResultantes):
		cantAjustesABorrar = Ajuste.objects.count() - ajustesResultantes
		if cantAjustesABorrar == 3:
			ajuste_cero = Ajuste.objects.filter(valor = 0)
			ajuste_cero.delete()
		if cantAjustesABorrar >= 2:
			max_valor = Ajuste.objects.aggregate(Max('valor'))['valor__max']
			ajuste_positivo = Ajuste.objects.filter(valor = max_valor)
			ajuste_positivo.delete()
			ajuste_negativo = Ajuste.objects.filter(valor = - max_valor)
			ajuste_negativo.delete()
		return cantAjustesABorrar


class FactorDePreCategorizacion(models.Model):
	descripcion = models.CharField(verbose_name=u'descripción', max_length=50, unique=True)
	fue_anulado = models.BooleanField(default=False)

	def __str__(self):
		return self.descripcion

	class Meta:
		ordering = ['descripcion']
		verbose_name = 'factor de pre-categorización'
		verbose_name_plural = 'factores de pre-categorización'


class FactorDeAjuste(models.Model):
	descripcion = models.CharField(verbose_name=u'descripción', max_length=50, unique=True)
	fue_anulado = models.BooleanField(default=False)

	def __str__(self):
		return self.descripcion

	class Meta:
		ordering = ['descripcion']
		verbose_name = 'factor de ajuste'
		verbose_name_plural = 'factores de ajuste'


class ValorDeFactorDePreCategorizacion(models.Model):
	descripcion = models.CharField(verbose_name=u'descripción', max_length=50, unique=True)
	factorDePreCategorizacion = models.ForeignKey(FactorDePreCategorizacion, verbose_name=u'factor de pre-categorización')
	fue_anulado = models.BooleanField(default=False)
	
	def __str__(self):
		return self.factorDePreCategorizacion.descripcion +" es "+ self.descripcion

	class Meta:
		ordering = ['descripcion']
		verbose_name = 'Valor de factor de pre-categorización'
		verbose_name_plural = 'Valores de factor de pre-categorización'


class ValorDeFactorDeAjuste(models.Model):
	descripcion = models.CharField(verbose_name=u'descripción', max_length=50, unique=True)
	factorDeAjuste = models.ForeignKey(FactorDeAjuste, verbose_name=u'factor de ajuste')
	fue_anulado = models.BooleanField(default=False)

	def __str__(self):
		return self.factorDeAjuste.descripcion +" es "+ self.descripcion

	class Meta:
		ordering = ['descripcion']
		verbose_name = 'Valor de factor de ajuste'
		verbose_name_plural = 'Valores de factor de ajuste'


class ReglaDePreCategorizacion(models.Model):
	condicion = models.ForeignKey(ValorDeFactorDePreCategorizacion)
	resultado = models.ForeignKey(Categoria)
	prioridad = models.PositiveSmallIntegerField()
	fue_anulado = models.BooleanField(default=False)

	def __str__(self):
		return "Regla "+ str(self.id) +": if "+ str(self.condicion.factorDePreCategorizacion) +" == "+ self.condicion.descripcion +" => precategorizacion = "+ str(self.resultado)

	class Meta:
		ordering = ['id']
		unique_together = ('resultado', 'prioridad')
		verbose_name = 'Regla de pre-categorización'
		verbose_name_plural = 'Reglas de pre-categorización'


class ReglaDeAjuste(models.Model):
	condicion = models.ForeignKey(ValorDeFactorDeAjuste)
	resultado = models.ForeignKey(Ajuste)
	prioridad = models.PositiveSmallIntegerField(unique=True)
	fue_anulado = models.BooleanField(default=False)

	def __str__(self):
		return "Regla "+ str(self.id) +": if "+ str(self.condicion.factorDeAjuste) +" == "+ self.condicion.descripcion +" => ajuste = "+ str(self.resultado)

	class Meta:
		ordering = ['id']
		unique_together = ('resultado', 'prioridad')
		verbose_name = 'Regla de ajuste'
		verbose_name_plural = 'Reglas de ajuste'