# -*- coding: utf-8 -*-
from rest_framework.serializers import ModelSerializer, ReadOnlyField, CharField, ChoiceField, HiddenField, CurrentUserDefault

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
	generador = HiddenField(default=CurrentUserDefault())

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


class AuxilioCambioEstadoSerializer(ModelSerializer):
	estados = EstadoAuxilioSerializer(many=True)

	class Meta:
		model = Auxilio
		fields = ('estados',)
	
	def update(self, instance, validated_data):
		estado = EstadoAuxilio.objects.create(estado=validated_data['estados'][0]['get_estado_display'], generador=validated_data['generador'])
		estado.save()
		instance.estados.add(estado)
		return instance