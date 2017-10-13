# -*- coding: utf-8 -*-
from rest_framework.serializers import ModelSerializer, ReadOnlyField

from ..models import Categoria, FactorDePreCategorizacion, ValorDeFactorDePreCategorizacion, ReglaDePreCategorizacion, Ajuste, FactorDeAjuste, ValorDeFactorDeAjuste, ReglaDeAjuste


# Create your serializers here.
class CategoriaSerializer(ModelSerializer):
	class Meta:
		model = Categoria
		fields = ['id', 'descripcion', 'prioridad', 'color']
		extra_kwargs = {
			'descripcion': {'style': {'autofocus': True}},
			'prioridad': {'min_value': 0},
			'color': {'style': {'input_type': 'color'}}
		}


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
		fields = ['descripcion',]


class ValorDeFactorDeAjusteSerializer(ModelSerializer):
	factorDeAjuste = ReadOnlyField(source='factorDeAjuste.descripcion')

	class Meta:
		model = ValorDeFactorDeAjuste
		fields = ['descripcion', 'factorDeAjuste']
		

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
	factorDePreCategorizacion = ReadOnlyField(source='factorDePreCategorizacion.descripcion')

	class Meta:
		model = ValorDeFactorDePreCategorizacion
		fields = ['descripcion', 'factorDePreCategorizacion']


class ReglaDeAjusteSerializer(ModelSerializer):
	class Meta:
		model = ReglaDeAjuste
		fields = ['condicion', 'resultado', 'prioridad']


class ReglaDePreCategorizacionSerializer(ModelSerializer):
	class Meta:
		model = ReglaDePreCategorizacion
		fields = ['id', 'condicion', 'resultado', 'prioridad']
		extra_kwargs = {
			'condicion': {'style': {'autofocus': True}},
