# -*- coding: utf-8 -*-
from rest_framework import serializers

from .models import SolicitudDeAuxilio, Movil, Asignacion, Auxilio

# Create your serializers here.
class SolicitudDeAuxilioSerializer(serializers.ModelSerializer):
    generador = serializers.ReadOnlyField(source='generador.username')

    class Meta:
        model = SolicitudDeAuxilio
        fields = ('id', 'fecha', 'nombre', 'sexo', 'cantidad_pacientes', 'ubicacion', 'ubicacion_especifica', 'ubicacion_coordenadas', 'contacto', 'motivo', 'observaciones', 'generador')


class MovilSerializer(serializers.ModelSerializer):
    generador = serializers.ReadOnlyField(source='generador.username')

    class Meta:
        model = Movil
        fields = ('estado', 'patente', 'generador')


class AsignacionSerializer(serializers.ModelSerializer):
    generador = serializers.ReadOnlyField(source='generador.username')

    class Meta:
        model = Asignacion
        fields = ('movil', 'estado', 'generador')


class AuxilioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auxilio
        fields = ('estado', 'solicitud', 'categoria', 'asignaciones')
