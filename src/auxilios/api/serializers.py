# -*- coding: utf-8 -*-
from rest_framework.serializers import CharField, CurrentUserDefault, HiddenField, ModelSerializer, ReadOnlyField

from ..models import Asignacion, Auxilio, EstadoAuxilio, FormularioFinalizacion, SolicitudDeAuxilio # Movil 
from rules.api.serializers import CategoriaSerializer


# Create your serializers here.
class AsignacionCambioEstadoSerializer(ModelSerializer):
	class Meta:
		model = Asignacion
		fields = ('medico', 'estado', 'creada', 'modificada')
		read_only_fields = ('medico',)


class FormularioFinalizacionSerializer(ModelSerializer):
	class Meta:
		model = FormularioFinalizacion
		fields = ('asignacion', 'asistencia_realizada', 'observaciones', 'motivo_inasistencia', 'categorizacion', 'pacientes')
		read_only_fields = ('asignacion',)
		depth = 1
	
	def create(self, validated_data):
		instance = super(FormularioFinalizacionSerializer, self).create(validated_data)
		# Realizar cambio de estado de la asignación
		instance.asignacion.estado = Asignacion.FINALIZADA
		instance.asignacion.save()
		return instance


class AsignacionSerializer(ModelSerializer):
	class Meta:
		model = Asignacion
		fields = ('id', 'medico', 'estado', 'creada', 'modificada')


class EstadoAuxilioSerializer(ModelSerializer):
	estado = CharField(source='get_estado_display')

	class Meta:
		model = EstadoAuxilio
		fields = ('id', 'fecha', 'estado')


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


class EstadoCambioAuxilioSerializer(ModelSerializer):
	class Meta:
		model = EstadoAuxilio
		fields = ('id', 'fecha', 'estado')
		extra_kwargs = {
			'id': {'read_only': True},
			'fecha': {'read_only': True}
		}


class AuxilioCambioEstadoSerializer(ModelSerializer):
	estados = EstadoCambioAuxilioSerializer(many=True)

	class Meta:
		model = Auxilio
		fields = ('estados',)
	
	def update(self, instance, validated_data):
		estado = EstadoAuxilio.objects.create(estado=validated_data['estados'][0]['estado'])
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
	