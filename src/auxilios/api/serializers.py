# -*- coding: utf-8 -*-
from rest_framework.serializers import CharField, CurrentUserDefault, HiddenField, ModelSerializer, ReadOnlyField

from ..models import Asignacion, Auxilio, EstadoAuxilio, SolicitudDeAuxilio # Movil 
from rules.api.serializers import CategoriaSerializer


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
		extra_kwargs = {
			'motivo': {'error_messages': {'required': 'Debe ingresar al menos un motivo'}}
		}


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


class AuxiliosUpdateSerializer(ModelSerializer):
	nombre = CharField(max_length=120)

	class Meta:
		model = Auxilio
		fields = ['nombre']
		# extra_kwargs = {
		# 	'nombre': {'label': u'Matrícula', 'style': {'placeholder': 'Ej: 123456', 'autofocus': True}},
		# }
	
	def update(self, instance, validated_data):
		instance = super(AuxiliosUpdateSerializer, self).update(instance, validated_data)
		instance.usuario.nombre = validated_data.get('nombre', instance.usuario.nombre)
		instance.usuario.save()
		return instance
	