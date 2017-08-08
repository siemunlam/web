# -*- coding: utf-8 -*-
from rest_framework.serializers import ModelSerializer, ReadOnlyField, CharField

from ..models import Asignacion, Auxilio, EstadoAuxilio, SolicitudDeAuxilio # Movil 
from rules.serializers import CategoriaSerializer


# Create your serializers here.
class AsignacionSerializer(ModelSerializer):
	generador = ReadOnlyField(source='generador.username')

	class Meta:
		model = Asignacion
		fields = ('movil', 'estado', 'generador')


class EstadoAuxilioSerializer(ModelSerializer):
	estado = CharField(source='get_estado_display')
	generador = ReadOnlyField(source='generador.username')

	class Meta:
		model = EstadoAuxilio
		fields = ('id', 'fecha', 'estado', 'generador')


# class MovilSerializer(ModelSerializer):
# 	generador = ReadOnlyField(source='generador.username')

# 	class Meta:
# 		model = Movil
# 		fields = ('patente', 'estado', 'generador')


class SolicitudDeAuxilioSerializer(ModelSerializer):
	generador = ReadOnlyField(source='generador.username')

	class Meta:
		model = SolicitudDeAuxilio
		fields = ('id', 'fecha', 'nombre', 'sexo', 'cantidad_pacientes', 'ubicacion', 'ubicacion_especifica', 'ubicacion_coordenadas', 'contacto', 'motivo', 'observaciones', 'generador')


class AuxilioSerializer(ModelSerializer):
	estados = EstadoAuxilioSerializer(many=True, read_only=True)
	solicitud = SolicitudDeAuxilioSerializer(many=False, read_only=True)
	categoria = CategoriaSerializer(many=False, read_only=True)
	asignaciones = AsignacionSerializer(many=True, read_only=True)

	class Meta:
		model = Auxilio
		fields = ('id', 'estados', 'solicitud', 'categoria', 'prioridad', 'asignaciones')