# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.validators import MaxValueValidator
from django.db import models
from django.db.models import Max, Min

from .extra_func import MAX_REGLAS_CAT, calcAjustesResultantes


# Create your models here.
class Categoria(models.Model):
	descripcion = models.CharField(verbose_name=u'descripción', max_length=25, unique=True)
	prioridad = models.PositiveSmallIntegerField(unique=True)
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
	descripcion = models.CharField(verbose_name=u'descripción', max_length=50)
	factorDePreCategorizacion = models.ForeignKey(FactorDePreCategorizacion, verbose_name=u'factor de pre-categorización')
	fue_anulado = models.BooleanField(default=False)
	
	def __str__(self):
		return self.factorDePreCategorizacion.descripcion +" es "+ self.descripcion

	class Meta:
		ordering = ['factorDePreCategorizacion']
		unique_together = ['descripcion', 'factorDePreCategorizacion']
		verbose_name = 'Valor de factor de pre-categorización'
		verbose_name_plural = 'Valores de factor de pre-categorización'


class ValorDeFactorDeAjuste(models.Model):
	descripcion = models.CharField(verbose_name=u'descripción', max_length=50)
	factorDeAjuste = models.ForeignKey(FactorDeAjuste, verbose_name=u'factor de ajuste')
	fue_anulado = models.BooleanField(default=False)

	def __str__(self):
		return self.factorDeAjuste.descripcion +" es "+ self.descripcion

	class Meta:
		ordering = ['factorDeAjuste']
		unique_together = ['descripcion', 'factorDeAjuste']
		verbose_name = 'Valor de factor de ajuste'
		verbose_name_plural = 'Valores de factor de ajuste'


class ReglaDeAjuste(models.Model):
	condicion = models.ForeignKey(ValorDeFactorDeAjuste)
	resultado = models.ForeignKey(Ajuste)
	prioridad = models.PositiveSmallIntegerField(unique=True, validators=[MaxValueValidator(MAX_REGLAS_CAT - 1)])
	fue_anulado = models.BooleanField(default=False)

	def __str__(self):
		return "Regla "+ str(self.id) +": if "+ str(self.condicion.factorDeAjuste) +" == "+ self.condicion.descripcion +" => ajuste = "+ str(self.resultado)

	class Meta:
		ordering = ['id']
		unique_together = ('resultado', 'prioridad')
		verbose_name = 'Regla de ajuste'
		verbose_name_plural = 'Reglas de ajuste'
	
	@staticmethod
	def escribirReglas(prioridad_base):
		reglas = ReglaDeAjuste.objects.filter(fue_anulado = False, resultado__valor__gte = 0).order_by('resultado', 'prioridad')
		texto = ''
		resultado_actual = Ajuste.objects.order_by('valor').first()
		for regla in reglas:
			if not regla.resultado == resultado_actual:
				prioridad_base += MAX_REGLAS_CAT
			texto += regla.escribirRDA(prioridad_base)
			resultado_actual = regla.resultado
		return texto
	
	def escribirRDA(self, prioridad_base):
		texto = ''
		texto += 'rule "ruleAjuste%s"\n' %str(self.id)
		texto += '\t\tno-loop\n'
		texto += '\t\tsalience %s\n' %str(prioridad_base + self.prioridad)
		texto += '\twhen\n'
		texto += '\t\tpersona : Persona()\n'
		texto += '\t\t\teval( persona.getDato("%s").equals("%s") )\n' %(self.condicion.factorDeAjuste.descripcion, self.condicion.descripcion)
		texto += '\tthen\n'
		texto += '\t\tpersona.setAjuste("%s");\n' %self.resultado.valor
		texto += 'end\n\n'
		return texto


class ReglaDePreCategorizacion(models.Model):
	condicion = models.ForeignKey(ValorDeFactorDePreCategorizacion)
	resultado = models.ForeignKey(Categoria)
	prioridad = models.PositiveSmallIntegerField(unique=True, validators=[MaxValueValidator(MAX_REGLAS_CAT - 1)])
	fue_anulado = models.BooleanField(default=False)

	def __str__(self):
		return "Regla "+ str(self.id) +": if "+ str(self.condicion.factorDePreCategorizacion) +" == "+ self.condicion.descripcion +" => precategorizacion = "+ str(self.resultado)

	class Meta:
		ordering = ['id']
		unique_together = ('resultado', 'prioridad')
		verbose_name = 'Regla de pre-categorización'
		verbose_name_plural = 'Reglas de pre-categorización'
	
	@staticmethod
	def escribirReglas(prioridad_base):
		reglas = ReglaDePreCategorizacion.objects.filter(fue_anulado = False).order_by('resultado', 'prioridad')
		texto = ''
		resultado_actual = Categoria.objects.first()
		for regla in reglas:
			if not regla.resultado == resultado_actual:
				prioridad_base += MAX_REGLAS_CAT
			texto += regla.escribirRDPC(prioridad_base)
			resultado_actual = regla.resultado
		return texto
	
	def escribirRDPC(self, prioridad_base):
		texto = ''
		texto += 'rule "rulePreCategorizacion%s"\n' %str(self.id)
		texto += '\t\tno-loop\n'
		texto += '\t\tsalience %s\n' %str(prioridad_base + self.prioridad)
		texto += '\twhen\n'
		texto += '\t\tpersona : Persona()\n'
		texto += '\t\t\teval( persona.getDato("%s").equals("%s") )\n' %(self.condicion.factorDePreCategorizacion.descripcion, self.condicion.descripcion)
		texto += '\tthen\n'
		texto += '\t\tpersona.setPreCategoria("%s");\n' %self.resultado.descripcion
		texto += 'end\n\n'
		return texto
