# -*- coding: utf-8 -*-
from django.conf import settings
from rest_framework.serializers import CharField, CurrentUserDefault, HiddenField, ModelSerializer, ReadOnlyField, SerializerMethodField, ValidationError

from .extra_func2 import notificarSuscriptores
from ..models import Asignacion, Auxilio, EstadoAuxilio, FormularioFinalizacion, SolicitudDeAuxilio, Suscriptor # Movil 
from rules.api.serializers import CategoriaSerializer
from medicos.api.helper_functions import notificarMedico
from medicos.api.serializers import MedicoCambioEstadoSerializer
from medicos.models import Medico
import datetime, json

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
	class Meta:
		model = FormularioFinalizacion
		fields = ['asignacion', 'asistencia_realizada', 'observaciones', 'motivo_inasistencia', 'categorizacion', 'pacientes']
		read_only_fields = ['asignacion',]
		depth = 1
	
	def create(self, validated_data):
		instance = super(FormularioFinalizacionSerializer, self).create(validated_data)
		# Realizar cambio de estado de la asignación
		serializer = AsignacionCambioEstadoSerializer(instance.asignacion, data={'estado': Asignacion.FINALIZADA})
		serializer.is_valid()
		serializer.save()
		# Realizar cambio de estado del médico
		serializer = MedicoCambioEstadoSerializer(instance.asignacion.medico, data={'estado': Medico.NO_DISPONIBLE})
		serializer.is_valid()
		serializer.save()
		# Si todas las asignaciones fueron finalizadas o canceladas, paso el estado del auxilio a FINALIZADO
		auxilio = Auxilio.objects.get(asignaciones=instance.asignacion)
		if not auxilio.asignaciones.filter(estado__in=[Asignacion.EN_CAMINO, Asignacion.EN_LUGAR, Asignacion.EN_TRASLADO]).exists():
			serializer = AuxilioCambioEstadoSerializer(auxilio, data={'estados': [{'estado': EstadoAuxilio.FINALIZADO}]})
			serializer.is_valid()
			serializer.save()
		return instance


class FormularioFinalizacionDetailSerializer(ModelSerializer):
	categorizacion = CharField(source='get_categorizacion_display')
	motivo_inasistencia = CharField(source='get_motivo_inasistencia_display')

	class Meta:
		model = FormularioFinalizacion
		fields = ['asignacion', 'asistencia_realizada', 'observaciones', 'motivo_inasistencia', 'categorizacion', 'pacientes']
		read_only_fields = ['asignacion', 'asistencia_realizada', 'observaciones', 'motivo_inasistencia', 'categorizacion', 'pacientes']
		depth = 1


class AsignacionSerializer(ModelSerializer):
	estado = CharField(source='get_estado_display')
	formulariofinalizacion = FormularioFinalizacionDetailSerializer(read_only=True)

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

	class Meta:
		model = SolicitudDeAuxilio
		fields = ['id', 'fecha', 'nombre', 'sexo', 'cantidad_pacientes', 'ubicacion', 'ubicacion_especifica', 'latitud_gps', 'longitud_gps', 'contacto', 'motivo', 'observaciones', 'origen', 'generador']
		extra_kwargs = { 'motivo': {'error_messages': {'required': 'Debe ingresar al menos un motivo'}} }


class SolicitudDeAuxilioDetailSerializer(ModelSerializer):
	generador = ReadOnlyField(source='generador.username')
	origen = CharField(source='get_origen_display')

	class Meta:
		model = SolicitudDeAuxilio
		fields = ['id', 'fecha', 'nombre', 'sexo', 'cantidad_pacientes', 'ubicacion', 'ubicacion_especifica', 'latitud_gps', 'longitud_gps', 'contacto', 'motivo', 'observaciones', 'origen', 'generador']
		read_only_fields = ['id', 'fecha', 'nombre', 'sexo', 'cantidad_pacientes', 'ubicacion', 'ubicacion_especifica', 'latitud_gps', 'longitud_gps', 'contacto', 'motivo', 'observaciones', 'origen', 'generador']


class AuxilioSerializer(ModelSerializer):
	estados = EstadoAuxilioSerializer(many=True, read_only=True)
	solicitud = SolicitudDeAuxilioDetailSerializer(many=False, read_only=True)
	categoria = CategoriaSerializer(many=False, read_only=True)
	asignaciones = AsignacionSerializer(many=True, read_only=True)

	class Meta:
		model = Auxilio
		fields = ['id', 'estados', 'solicitud', 'categoria', 'prioridad', 'asignaciones', 'codigo_suscripcion']



class AuxilioUbicacionGPSSerializer(ModelSerializer):
	categoria = CategoriaSerializer(many=False, read_only=True)
	direccion = CharField(source='solicitud.ubicacion')
	estado = SerializerMethodField()
	latitud = CharField(source='solicitud.latitud_gps')
	longitud = CharField(source='solicitud.longitud_gps')
	medicos = SerializerMethodField()

	class Meta:
		model = Auxilio
		fields = ['id', 'categoria', 'direccion', 'estado', 'latitud', 'longitud', 'medicos', 'prioridad']
		read_only_fields = ['id', 'categoria', 'direccion', 'estado', 'latitud', 'longitud', 'medicos', 'prioridad']
	
	def get_estado(self, obj):
		return obj.estados.first().get_estado_display()

	def get_medicos(self, obj):
		return obj.asignaciones.filter(medico__isnull=False).values_list('medico_id')


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
		if estadoActual:
			if estadoActual.estado == EstadoAuxilio.CANCELADO:
				raise ValidationError(u'Operación no permitida. El auxilio ya ha sido cancelado.')
			if estadoActual.estado == EstadoAuxilio.FINALIZADO:
				raise ValidationError(u'Operación no permitida. El auxilio ya ha sido finalizado.')
		if not estadoActual or nuevoEstado.estado != estadoActual.estado:
			if nuevoEstado.estado == EstadoAuxilio.CANCELADO:
				se_cancelaron_asignaciones = False
				for asignacion in instance.asignaciones.filter(estado__in=[Asignacion.PENDIENTE, Asignacion.EN_CAMINO]):
					se_cancelaron_asignaciones = True
					serializer = AsignacionCambioEstadoSerializer(asignacion, data={'estado': Asignacion.CANCELADA})
					serializer.is_valid()
					serializer.save()
					if asignacion.medico:
						notificarMedico(medico=asignacion.medico, mensaje={
							'code': settings.CODE_AUXILIO_CANCELADO,
							'mensaje': 'El auxilio #%s ha sido cancelado.' %(instance.id)
						})
						serializer = MedicoCambioEstadoSerializer(asignacion.medico, data={'estado': Medico.NO_DISPONIBLE})
						serializer.is_valid()
						serializer.save()
				if not instance.asignaciones.filter(estado__in=[Asignacion.EN_LUGAR, Asignacion.EN_TRASLADO]).exists():
					# Si el auxilio ya no posee asignaciones EN_LUGAR o EN_TRASLADO, es decir, si todas sus asignaciones están en estado: CANCELADA o FINALIZADA, le cambio el estado a CANCELADO.
					nuevoEstado.save()
					instance.estados.add(nuevoEstado)
				else:
					if se_cancelaron_asignaciones:
						raise ValidationError(u'No se pudo cancelar el auxilio porque posee asignaciones "En el lugar" o "En traslado".\nSolamente se cancelaron las asignaciones en estado "Pendiente" o "En camino".')
					else:
						raise ValidationError(u'No se pudo cancelar el auxilio porque posee asignaciones "En el lugar" o "En traslado".')
			else:
				nuevoEstado.save()
				instance.estados.add(nuevoEstado)
			if nuevoEstado.estado in [EstadoAuxilio.CANCELADO, EstadoAuxilio.EN_CURSO, EstadoAuxilio.FINALIZADO, EstadoAuxilio.PENDIENTE]:
				mensaje = {
					'auxilio': instance.codigo_suscripcion,
					'status': nuevoEstado.get_estado_display(),
					'timestamp': datetime.datetime.strftime(nuevoEstado.fecha, "%Y-%m-%d %H:%M:%S")
				}
				if nuevoEstado.estado == EstadoAuxilio.EN_CURSO:
					from medicos.api.helper_functions import get_estimated_time_distance
					# Uso el médico de la primer asignación
					medico = instance.asignaciones.first().medico
					desde = {
						'lat': medico.latitud_gps,
						'long': medico.longitud_gps
					}
					hasta = {
						'lat': instance.solicitud.latitud_gps,
						'long': instance.solicitud.longitud_gps
					}
					mensaje['estimacion'] = get_estimated_time_distance(desde, hasta)
				notificarSuscriptores(instance.suscriptores.all(), mensaje=mensaje)
		return instance


class AuxiliosUpdateSerializer(ModelSerializer):
	nombre = CharField(max_length=120)

	class Meta:
		model = Auxilio
		fields = ['nombre',]
	
	def update(self, instance, validated_data):
		instance = super(AuxiliosUpdateSerializer, self).update(instance, validated_data)
		instance.usuario.nombre = validated_data.get('nombre', instance.usuario.nombre)
		instance.usuario.save()
		return instance


class SuscriptorDetailSerializer(ModelSerializer):
	timestamp = SerializerMethodField()

	class Meta:
		model = Suscriptor
		fields = ['codigo', 'timestamp']
		read_only_fields = ['timestamp',]

	def get_timestamp(self, obj):
		return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	
	def create(self, validated_data):
		instance = super(SuscriptorDetailSerializer, self).create(validated_data)
		# Add suscriptor to Auxilio
		auxilio = Auxilio.objects.get(codigo_suscripcion=self.context.get('codigo_suscripcion'))
		auxilio.suscriptores.add(instance)
		return instance