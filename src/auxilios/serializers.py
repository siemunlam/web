# -*- coding: utf-8 -*-
from rest_framework import serializers

from .models import SolicitudDeAuxilio, Movil, Asignacion, Auxilio
from rules.serializers import CategoriaSerializer


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
    estado = serializers.CharField(source='get_estado_display')
    solicitud = SolicitudDeAuxilioSerializer(many=False, read_only=True)
    categoria = CategoriaSerializer(many=False, read_only=True)
    asignaciones = AsignacionSerializer(many=True, read_only=True)

    class Meta:
        model = Auxilio
        fields = ('id', 'estado', 'solicitud', 'categoria', 'asignaciones')