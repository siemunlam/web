# -*- coding: utf-8 -*-
from rest_framework import serializers

from .models import SolicitudDeAuxilio, Movil

# Create your serializers here.
class SolicitudDeAuxilioSerializer(serializers.ModelSerializer):
    generador = serializers.ReadOnlyField(source='generador.username')

    class Meta:
        model = SolicitudDeAuxilio
        fields = ('fecha', 'nombre', 'sexo', 'cantidad_pacientes', 'ubicacion', 'ubicacion_especifica', 'ubicacion_coordenadas', 'contacto', 'motivo', 'observaciones', 'generador')


class MovilSerializer(serializers.ModelSerializer):
    generador = serializers.ReadOnlyField(source='generador.username')

    class Meta:
        model = Movil
        fields = ('estado', 'patente', 'generador')

