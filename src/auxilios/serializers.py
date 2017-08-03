# -*- coding: utf-8 -*-
from rest_framework import serializers

from .models import SolicitudDeAuxilio, Movil, Asignacion, Auxilio, Medico, EstadoAuxilio
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
		fields = ('patente', 'estado', 'generador')


class AsignacionSerializer(serializers.ModelSerializer):
	generador = serializers.ReadOnlyField(source='generador.username')

	class Meta:
		model = Asignacion
		fields = ('movil', 'estado', 'generador')


class EstadoAuxilioSerializer(serializers.ModelSerializer):
	estado = serializers.CharField(source='get_estado_display')
	generador = serializers.ReadOnlyField(source='generador.username')

	class Meta:
		model = EstadoAuxilio
		fields = ('id', 'fecha', 'estado', 'generador')


class AuxilioSerializer(serializers.ModelSerializer):
	estados = EstadoAuxilioSerializer(many=True, read_only=True)
	solicitud = SolicitudDeAuxilioSerializer(many=False, read_only=True)
	categoria = CategoriaSerializer(many=False, read_only=True)
	asignaciones = AsignacionSerializer(many=True, read_only=True)

	class Meta:
		model = Auxilio
		fields = ('id', 'estados', 'solicitud', 'categoria', 'prioridad', 'asignaciones')


class MedicoSerializer(serializers.ModelSerializer):
	generador = serializers.ReadOnlyField(source='generador.username')

	class Meta:
		model = Medico
		fields = ('dni', 'matricula', 'apellido', 'nombre', 'sexo', 'telefono', 'generador')

