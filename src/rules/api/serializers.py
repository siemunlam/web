# -*- coding: utf-8 -*-
from rest_framework.serializers import ModelSerializer, ReadOnlyField

from ..models import Categoria, FactorDePreCategorizacion, ValorDeFactorDePreCategorizacion, ReglaDePreCategorizacion, Ajuste, FactorDeAjuste, ValorDeFactorDeAjuste, ReglaDeAjuste


# Create your serializers here.
class CategoriaSerializer(ModelSerializer):
    class Meta:
        model = Categoria
        fields = ('id', 'descripcion', 'prioridad', 'color')


class FactorDeAjusteSerializer(ModelSerializer):
    class Meta:
        model = FactorDeAjuste
        fields = ('descripcion',)


class FactorDePreCategorizacionSerializer(ModelSerializer):
    class Meta:
        model = FactorDePreCategorizacion
        fields = ('descripcion',)


class ValorDeFactorDeAjusteSerializer(ModelSerializer):
    factorDeAjuste = ReadOnlyField(source='factorDeAjuste.descripcion')

    class Meta:
        model = ValorDeFactorDeAjuste
        fields = ('descripcion', 'factorDeAjuste')


class ValorDeFactorDePreCategorizacionSerializer(ModelSerializer):
    factorDePreCategorizacion = ReadOnlyField(source='factorDePreCategorizacion.descripcion')

    class Meta:
        model = ValorDeFactorDePreCategorizacion
        fields = ('descripcion', 'factorDePreCategorizacion')


class ReglaDeAjusteSerializer(ModelSerializer):
    class Meta:
        model = ReglaDeAjuste
        fields = ('condicion', 'resultado', 'prioridad')


class ReglaDePreCategorizacionSerializer(ModelSerializer):
    class Meta:
        model = ReglaDePreCategorizacion
        fields = ('condicion', 'resultado', 'prioridad')