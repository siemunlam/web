# -*- coding: utf-8 -*-
from rest_framework.serializers import CharField, CurrentUserDefault, HiddenField, ModelSerializer, ReadOnlyField

from ..models import Asignacion, Auxilio, EstadoAuxilio, FormularioFinalizacion, SolicitudDeAuxilio, Suscriptor # Movil 
from rules.api.serializers import CategoriaSerializer
from .extra_func2 import notificarSuscriptores
from medicos.api.helper_functions import notificarMedico
from medicos.api.serializers import MedicoCambioEstadoSerializer
from medicos.models import Medico


# Create your serializers here.
class AsignacionCambioEstadoSerializer(ModelSerializer):
	class Meta:
		model = Asignacion
		fields = ['medico', 'estado', 'creada', 'modificada']
		read_only_fields = ['medico',]


class FormularioFinalizacionSerializer(ModelSerializer):
	class Meta:
		model = FormularioFinalizacion
		fields = ['asignacion', 'asistencia_realizada', 'observaciones', 'motivo_inasistencia', 'categorizacion', 'pacientes']
		read_only_fields = ['asignacion',]
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
		fields = ['id', 'medico', 'estado', 'creada', 'modificada']


class EstadoAuxilioSerializer(ModelSerializer):
	estado = CharField(source='get_estado_display')

	class Meta:
		model = EstadoAuxilio
		fields = ['id', 'fecha', 'estado']


# class MovilSerializer(ModelSerializer):
# 	generador = ReadOnlyField(source='generador.username')

# 	class Meta:
# 		model = Movil
# 		fields = ('patente', 'estado', 'generador')


class SolicitudDeAuxilioSerializer(ModelSerializer):
	generador = ReadOnlyField(source='generador.username')

	class Meta:
		model = SolicitudDeAuxilio
		fields = ['id', 'fecha', 'nombre', 'sexo', 'cantidad_pacientes', 'ubicacion', 'ubicacion_especifica', 'ubicacion_coordenadas', 'contacto', 'motivo', 'observaciones', 'origen', 'generador']
		extra_kwargs = { 'motivo': {'error_messages': {'required': 'Debe ingresar al menos un motivo'}} }


class SolicitudDeAuxilioDetailSerializer(ModelSerializer):
	class Meta:
		model = SolicitudDeAuxilio
		fields = ['fecha', 'generador', 'origen', 'ubicacion_coordenadas']
		read_only_fields = ['fecha', 'generador', 'origen', 'ubicacion_coordenadas']


class AuxilioSerializer(ModelSerializer):
	estados = EstadoAuxilioSerializer(many=True, read_only=True)
	solicitud = SolicitudDeAuxilioSerializer(many=False, read_only=True)
	categoria = CategoriaSerializer(many=False, read_only=True)
	asignaciones = AsignacionSerializer(many=True, read_only=True)

	class Meta:
		model = Auxilio
		fields = ['id', 'estados', 'solicitud', 'categoria', 'prioridad', 'asignaciones', 'codigo_suscripcion']


class EstadoCambioAuxilioSerializer(ModelSerializer):
	class Meta:
		model = EstadoAuxilio
		fields = ['id', 'fecha', 'estado']
		read_only_fields = ['id', 'fecha']


class AuxilioCambioEstadoSerializer(ModelSerializer):
	estados = EstadoCambioAuxilioSerializer(many=True)

	class Meta:
		model = Auxilio
		fields = ['estados',]
	
	def update(self, instance, validated_data):
		estado = EstadoAuxilio.objects.create(estado=validated_data['estados'][0]['estado'])
		estado.save()
		instance.estados.add(estado)
		if estado.estado == EstadoAuxilio.CANCELADO:
			for asignacion in instance.asignaciones.filter(estado__in=[Asignacion.PENDIENTE, Asignacion.EN_CAMINO]):
				serializer = AsignacionCambioEstadoSerializer(asignacion, data{'estado': Asignacion.CANCELADA})
				serializer.is_valid()
				serializer.save()
				if asignacion.medico:					
					notificarMedico(asignacion.medico,
						mensaje={'mensaje': 'El auxilio #%s ha sido cancelado.\nUd. ha sido desvinculado del mismo.' %(instance.id)})
					serializer = MedicoCambioEstadoSerializer(asignacion.medico, data={'estado': Medico.DISPONIBLE})
					serializer.is_valid()
					serializer.save()
		elif estado.estado in [EstadoAuxilio.EN_CURSO, EstadoAuxilio.FINALIZADO]:
			notificarSuscriptores(instance, estado)
		return instance


class AuxiliosUpdateSerializer(ModelSerializer):
	nombre = CharField(max_length=120)

	class Meta:
		model = Auxilio
		fields = ['nombre',]
		# extra_kwargs = {
		# 	'nombre': {'label': u'Matrícula', 'style': {'placeholder': 'Ej: 123456', 'autofocus': True}},
		# }
	
	def update(self, instance, validated_data):
		instance = super(AuxiliosUpdateSerializer, self).update(instance, validated_data)
		instance.usuario.nombre = validated_data.get('nombre', instance.usuario.nombre)
		instance.usuario.save()
		return instance


class SuscriptorDetailSerializer(ModelSerializer):
	class Meta:
		model = Suscriptor
		fields = ['codigo',]