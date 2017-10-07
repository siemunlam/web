# -*- coding: utf-8 -*-
import json
from math import asin, cos, pi, sin, sqrt

from django.contrib import messages
from medicos.models import Medico
from medicos.api.helper_functions import notificarMedico
from rest_framework.exceptions import APIException

from ..models import Asignacion, Auxilio, EstadoAuxilio

def generarAsignacion():
	from .serializers import AsignacionCambioEstadoSerializer, AuxilioCambioEstadoSerializer
	from medicos.api.serializers import MedicoCambioEstadoSerializer

	# Obtener todos los auxilios con alguna asignación PENDIENTE.
	auxilios_a_asignar = getAuxilioAAsignar()
	
	for	auxilio_a_asignar in auxilios_a_asignar:
		for asignacion in auxilio_a_asignar.asignaciones.all():
			if not asignacion.medico:
				medicos_libres = getMedicoAAsignar()
				# Si no hay médicos libres, no puedo asignar.
				if not medicos_libres:
					return True
				coordenadas_destino = {
					'lat': auxilio_a_asignar.solicitud.latitud_gps,
					'long': auxilio_a_asignar.solicitud.longitud_gps
				}
				medico_a_asignar = filtrar_por_cercania(medicos_libres, coordenadas_destino)
				asignacion.medico = medico_a_asignar
				serializer = AsignacionCambioEstadoSerializer(asignacion, data={'estado': Asignacion.EN_CAMINO})
				serializer.is_valid()
				serializer.save()
				serializer = AuxilioCambioEstadoSerializer(auxilio_a_asignar, data={'estados': [{'estado': EstadoAuxilio.EN_CURSO}]})
				serializer.is_valid()
				serializer.save()
				# TODO: Verificar return de notificarMedico y ver que hacer.
				# Loguear en el servidor en la tabla de logueos.
				notificarMedico(medico=medico_a_asignar, mensaje={
					'colorDescripcion': auxilio_a_asignar.categoria.descripcion,
					'colorHexa': auxilio_a_asignar.categoria.color,
					'direccion': auxilio_a_asignar.solicitud.ubicacion,
					'lat': auxilio_a_asignar.solicitud.latitud_gps,
					'long':auxilio_a_asignar.solicitud.longitud_gps,
					'motivos': json.loads(auxilio_a_asignar.solicitud.motivo),
					'paciente': auxilio_a_asignar.solicitud.nombre
				})
				serializer = MedicoCambioEstadoSerializer(medico_a_asignar, data={'estado': Medico.EN_AUXILIO})
				serializer.is_valid()
				serializer.save()


def filtrarAuxiliosPorEstado(estados=None):
	# La función retorna un listado de auxilios cuyo estado actual es alguno de los ingresados en el array
	# Si no se ingresa nada, se retornan todos los auxilios
	if not estados is None:
		if len(estados) > 1:
			estados = ', '.join(estados)
		query = '''	SELECT *
					FROM auxilios_auxilio
					WHERE EXISTS (SELECT 1
					FROM auxilios_auxilio_estados
					INNER JOIN auxilios_estadoauxilio
						ON auxilios_estadoauxilio.id = auxilios_auxilio_estados.estadoauxilio_id
					GROUP BY auxilios_auxilio_estados.auxilio_id
					HAVING auxilios_estadoauxilio.fecha = (SELECT MAX(auxilios_estadoauxilio.fecha)
					FROM auxilios_estadoauxilio
					WHERE auxilios_estadoauxilio.id = auxilios_auxilio_estados.estadoauxilio_id
					AND auxilios_auxilio.id = auxilios_auxilio_estados.auxilio_id)
					AND (auxilios_estadoauxilio.estado in (%s)))'''%estados			
		object_list = list(Auxilio.objects.raw(query))
	else:
		object_list = Auxilio.objects.all()
	return object_list


def getAuxilioAAsignar():
	return filtrarAuxiliosPorEstado([EstadoAuxilio.PENDIENTE, EstadoAuxilio.EN_CURSO])


def obtenerAsignacionesAtendidas(asignaciones):
	asignaciones_atendidas = 0
	if asignaciones.count() > 0:
		for asignacion in asignaciones.all():
			if asignacion.medico:
				asignaciones_atendidas += 1
	return asignaciones_atendidas


def getMedicoAAsignar():
	# Busca los médicos en estado DISPONIBLE que tengan Ubicación y Firebase Code
	medicos_disponibles = Medico.objects.filter(estado=Medico.DISPONIBLE).exclude(latitud_gps=None, longitud_gps=None, fcm_code__exact='')
	medicos_disponibles.query.clear_ordering(force_empty=True)
	# TODO:Éste es por las dudas. Tal vez se pueda sacar
	return medicos_disponibles


def filtrar_por_cercania(medicos_sin_asignar, coordenadas):
	""" Retorna el médico más próximo a las coordenadas proporcionadas """
	medico_mas_cercano = None
	menor_distancia = None
	for medico in medicos_sin_asignar:
		distancia_medico_auxilio = calcular_distancia({'lat': medico.latitud_gps, 'long': medico.longitud_gps}, coordenadas)
		if not medico_mas_cercano or distancia_medico_auxilio < menor_distancia:
			medico_mas_cercano = medico
			menor_distancia = distancia_medico_auxilio
	return medico_mas_cercano


def calcular_distancia(coordenadas_1, coordenadas_2):
	lat1 = coordenadas_1['lat']
	long1 = coordenadas_1['long']
	lat2 = coordenadas_2['lat']
	long2 = coordenadas_2['long']
	
	r = 6371000 #radio terrestre medio, en metros
	c = pi / 180 #constante para transformar grados en radianes
	
	# Fórmula de Haversine
	distanciaHaversine = 2*r*asin(sqrt(sin(c*(lat2-lat1)/2)**2 + cos(c*lat1)*cos(c*lat2)*sin(c*(long2-long1)/2)**2))
	return distanciaHaversine