# -*- coding: utf-8 -*-
from rest_framework.serializers import ModelSerializer, ReadOnlyField

from ..models import Ajuste, Categoria, FactorDePreCategorizacion, ValorDeFactorDePreCategorizacion, ReglaDePreCategorizacion, Ajuste, FactorDeAjuste, ValorDeFactorDeAjuste, ReglaDeAjuste


# Create your serializers here.

class AjusteSerializer(ModelSerializer):
	class Meta:
		model = Ajuste
		fields = ['id', 'valor']


class CategoriaSerializer(ModelSerializer):
	class Meta:
		model = Categoria
		fields = ['id', 'descripcion', 'prioridad', 'color']
		extra_kwargs = {
			'descripcion': {'style': {'autofocus': True}},
			'prioridad': {'min_value': 0},
			'color': {'style': {'input_type': 'color'}}
		}


class UpdateCategoriaSerializer(ModelSerializer):
	class Meta:
		model = Categoria
		fields = ['id', 'descripcion', 'prioridad', 'color']
		extra_kwargs = {
			'descripcion': {'style': {'autofocus': True}},
			'prioridad': {'min_value': 0},
			'color': {'style': {'input_type': 'color'}}
		}

	def update(self, instance, validated_data):
		instance = super(UpdateCategoriaSerializer, self).update(instance, validated_data)
		instance.descripcion = validated_data.get('descripcion', instance.descripcion)
		instance.prioridad = validated_data.get('prioridad', instance.prioridad)
		instance.color = validated_data.get('color', instance.color)
		instance.save()
		return instance


class FactorDeAjusteSerializer(ModelSerializer):
	class Meta:
		model = FactorDeAjuste
		fields = ['id', 'descripcion']
		extra_kwargs = {
			'descripcion': {'style': {'autofocus': True}}
		}

class UpdateFactorDeAjusteSerializer(ModelSerializer):
	class Meta:
		model = FactorDeAjuste
		fields = ['id', 'descripcion']
		extra_kwargs = {
			'descripcion': {'style': {'autofocus': True}}
		}

	def update(self, instance, validated_data):
		instance = super(UpdateFactorDeAjusteSerializer, self).update(instance, validated_data)
		instance.descripcion = validated_data.get('descripcion', instance.descripcion)
		instance.save()
		return instance
	

class ValorDeFactorDeAjusteSerializer(ModelSerializer):
	factorDeAjuste_descripcion = ReadOnlyField(source='factorDeAjuste.descripcion')

	class Meta:
		model = ValorDeFactorDeAjuste
		fields = ['id', 'descripcion', 'factorDeAjuste', 'factorDeAjuste_descripcion']


class UpdateValorDeFactorDeAjusteSerializer(ModelSerializer):
	factorDeAjuste_descripcion = ReadOnlyField(source='factorDeAjuste.descripcion')

	class Meta:
		model = ValorDeFactorDeAjuste
		fields = ['id', 'descripcion', 'factorDeAjuste_descripcion']
		extra_kwargs = {
			'descripcion': {'style': {'autofocus': True}}
		}

	def update(self, instance, validated_data):
		instance = super(UpdateValorDeFactorDeAjusteSerializer, self).update(instance, validated_data)
		instance.descripcion = validated_data.get('descripcion', instance.descripcion)
		instance.save()
		return instance


class FactorDePreCategorizacionSerializer(ModelSerializer):
	class Meta:
		model = FactorDePreCategorizacion
		fields = ['id', 'descripcion']
		extra_kwargs = {
			'descripcion': {'style': {'autofocus': True}}
		}


class UpdateFactorDePreCategorizacionSerializer(ModelSerializer):
	class Meta:
		model = FactorDePreCategorizacion
		fields = ['id', 'descripcion']
		extra_kwargs = {
			'descripcion': {'style': {'autofocus': True}}
		}

	def update(self, instance, validated_data):
		instance = super(UpdateFactorDePreCategorizacionSerializer, self).update(instance, validated_data)
		instance.descripcion = validated_data.get('descripcion', instance.descripcion)
		instance.save()
		return instance


class ValorDeFactorDePreCategorizacionSerializer(ModelSerializer):
	factorDePreCategorizacion_descripcion = ReadOnlyField(source='factorDePreCategorizacion.descripcion')

	class Meta:
		model = ValorDeFactorDePreCategorizacion
		fields = ['id', 'descripcion', 'factorDePreCategorizacion', 'factorDePreCategorizacion_descripcion']
		extra_kwargs = {
			'descripcion': {'style': {'autofocus': True}}
		}


class UpdateValorDeFactorDePreCategorizacionSerializer(ModelSerializer):
	factorDePreCategorizacion_descripcion = ReadOnlyField(source='factorDePreCategorizacion.descripcion')

	class Meta:
		model = ValorDeFactorDePreCategorizacion
		fields = ['id', 'descripcion', 'factorDePreCategorizacion_descripcion']
		extra_kwargs = {
			'descripcion': {'style': {'autofocus': True}}
		}

	def update(self, instance, validated_data):
		instance = super(UpdateValorDeFactorDePreCategorizacionSerializer, self).update(instance, validated_data)
		instance.descripcion = validated_data.get('descripcion', instance.descripcion)
		instance.save()
		return instance


class ReglaDeAjusteSerializer(ModelSerializer):
	condicion_descripcion = ReadOnlyField(source='condicion.descripcion')
	condicion_factora_descripcion = ReadOnlyField(source='condicion.factorDeAjuste.descripcion')
	resultado_valor = ReadOnlyField(source='resultado.valor')
	class Meta:
		model = ReglaDeAjuste
		fields = ['id', 'condicion', 'condicion_descripcion', 'condicion_factora_descripcion', 'resultado', 'resultado_valor', 'prioridad']
		extra_kwargs = {
			'condicion': {'style': {'autofocus': True}},
			'resultado': {'label': 'Ajuste'},
			'prioridad': {'min_value': 0},
		}


class UpdateReglaDeAjusteSerializer(ModelSerializer):
	class Meta:
		model = ReglaDeAjuste
		fields = ['id', 'condicion', 'resultado', 'prioridad']
		extra_kwargs = {
			'condicion': {'style': {'autofocus': True}},
			'resultado': {'label': 'Ajuste'},
			'prioridad': {'min_value': 0},
		}

	def update(self, instance, validated_data):
		instance = super(UpdateReglaDeAjusteSerializer, self).update(instance, validated_data)
		instance.condicion = validated_data.get('condicion', instance.condicion)
		instance.resultado = validated_data.get('resultado', instance.resultado)
		instance.prioridad = validated_data.get('prioridad', instance.prioridad)
		instance.save()
		return instance


class ReglaDePreCategorizacionSerializer(ModelSerializer):
	condicion_descripcion = ReadOnlyField(source='condicion.descripcion')
	condicion_factorpc_descripcion = ReadOnlyField(source='condicion.factorDePreCategorizacion.descripcion')
	resultado_descripcion = ReadOnlyField(source='resultado.descripcion')
	class Meta:
		model = ReglaDePreCategorizacion
		fields = ['id', 'condicion', 'condicion_descripcion', 'condicion_factorpc_descripcion', 'resultado', 'resultado_descripcion', 'prioridad']
		extra_kwargs = {
			'condicion': {'style': {'autofocus': True}},
			'resultado': {'label': 'Categoría'},
			'prioridad': {'min_value': 0},
		}


class UpdateReglaDePreCategorizacionSerializer(ModelSerializer):
	class Meta:
		model = ReglaDePreCategorizacion
		fields = ['id', 'condicion', 'resultado', 'prioridad']
		extra_kwargs = {
			'condicion': {'style': {'autofocus': True}},
			'resultado': {'label': 'Categoría'},
			'prioridad': {'min_value': 0},
		}

	def update(self, instance, validated_data):
		instance = super(UpdateReglaDePreCategorizacionSerializer, self).update(instance, validated_data)
		instance.condicion = validated_data.get('condicion', instance.condicion)
		instance.resultado = validated_data.get('resultado', instance.resultado)
		instance.prioridad = validated_data.get('prioridad', instance.prioridad)
		instance.save()
		return instance
