# -*- coding: utf-8 -*-
from rest_framework import serializers

from .models import Categoria, FactorDePreCategorizacion, ValorDeFactorDePreCategorizacion, ReglaDePreCategorizacion, Ajuste, FactorDeAjuste, ValorDeFactorDeAjuste, ReglaDeAjuste


# Create your serializers here.
class FactorDeAjusteSerializer(serializers.ModelSerializer):
    class Meta:
        model = FactorDeAjuste
        fields = ('descripcion',)


class FactorDePreCategorizacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FactorDePreCategorizacion
        fields = ('descripcion',)


class ValorDeFactorDeAjusteSerializer(serializers.ModelSerializer):
    factorDeAjuste = serializers.ReadOnlyField(source='factorDeAjuste.descripcion')

    class Meta:
        model = ValorDeFactorDeAjuste
        fields = ('descripcion', 'factorDeAjuste')


class ValorDeFactorDePreCategorizacionSerializer(serializers.ModelSerializer):
    factorDePreCategorizacion = serializers.ReadOnlyField(source='factorDePreCategorizacion.descripcion')

    class Meta:
        model = ValorDeFactorDePreCategorizacion
        fields = ('descripcion', 'factorDePreCategorizacion')