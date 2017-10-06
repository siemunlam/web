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


class AsignacionDesvincularSerializer(ModelSerializer):
	class Meta:
		model = Asignacion
		fields = ['medico', 'estado', 'creada', 'modificada']
		read_only_fields = ['medico', 'estado']
	
	def update(self, instance, validated_data):
		from .extra_func import generarAsignacion

		# El médico pasa a NO DISPONIBLE
		serializer = MedicoCambioEstadoSerializer(instance.medico, data={'estado': Medico.NO_DISPONIBLE})
		serializer.is_valid()
		serializer.save()
		# La asignaciòn queda sin médico y en estado PENDIENTE
		instance.medico = None
		instance.estado = Asignacion.PENDIENTE
		instance.save()
		# Si el auxilio no tiene otras asignaciones "EN CURSO", lo paso a PENDIENTE y busco generarAsignacion nuevamente.
		auxilio = Auxilio.objects.get(asignaciones=instance)
		if not auxilio.asignaciones.filter(estado__in=[Asignacion.EN_CAMINO, Asignacion.EN_LUGAR, Asignacion.EN_TRASLADO]).exists():
			serializer = AuxilioCambioEstadoSerializer(auxilio, data={'estados': [{'estado': EstadoAuxilio.PENDIENTE}]})
			serializer.is_valid()
			serializer.save()
			generarAsignacion()
		return instance

class FormularioFinalizacionSerializer(ModelSerializer):
	categorizacion = CharField(source='get_categorizacion_display')
	motivo_inasistencia = CharField(source='get_motivo_inasistencia_display')

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
	estado = CharField(source='get_estado_display')
	formulariofinalizacion = FormularioFinalizacionSerializer(read_only=True)

	class Meta:
		model = Asignacion
		fields = ['id', 'medico', 'estado', 'creada', 'modificada', 'formulariofinalizacion']


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
	origen = CharField(source='get_origen_display')

	class Meta:
		model = SolicitudDeAuxilio
		fields = ['id', 'fecha', 'nombre', 'sexo', 'cantidad_pacientes', 'ubicacion', 'ubicacion_especifica', 'latitud_gps', 'longitud_gps', 'contacto', 'motivo', 'observaciones', 'origen', 'generador']
		extra_kwargs = { 'motivo': {'error_messages': {'required': 'Debe ingresar al menos un motivo'}} }


class SolicitudDeAuxilioDetailSerializer(ModelSerializer):
	class Meta:
		model = SolicitudDeAuxilio
		fields = ['fecha', 'generador', 'origen', 'latitud_gps', 'longitud_gps']
		read_only_fields = ['fecha', 'generador', 'origen', 'latitud_gps', 'longitud_gps']


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
		nuevoEstado = EstadoAuxilio.objects.create(estado=validated_data['estados'][0]['estado'])
		estadoActual = instance.estados.first()
		if not estadoActual or nuevoEstado.estado != estadoActual.estado:
			nuevoEstado.save()
			instance.estados.add(nuevoEstado)
			if nuevoEstado.estado == EstadoAuxilio.CANCELADO:
				for asignacion in instance.asignaciones.filter(estado__in=[Asignacion.PENDIENTE, Asignacion.EN_CAMINO]):
					serializer = AsignacionCambioEstadoSerializer(asignacion, data={'estado': Asignacion.CANCELADA})
					serializer.is_valid()
					serializer.save()
					if asignacion.medico:
						notificarMedico(medico=asignacion.medico, mensaje={
							'mensaje': 'El auxilio #%s ha sido cancelado.' %(instance.id)
						})
						serializer = MedicoCambioEstadoSerializer(asignacion.medico, data={'estado': Medico.DISPONIBLE})
						serializer.is_valid()
						serializer.save()
			elif nuevoEstado.estado in [EstadoAuxilio.EN_CURSO, EstadoAuxilio.FINALIZADO]:
				notificarSuscriptores(instance.suscriptores.all(), mensaje={
					'status': nuevoEstado.get_estado_display(),
					'timestamp': nuevoEstado.fecha
				})
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