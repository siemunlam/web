# -*- coding: utf-8 -*-
import json
from math import asin, cos, pi, sin, sqrt
from ast import literal_eval as make_tuple

import requests
from django.contrib import messages
from medicos.models import Medico
from rest_framework.exceptions import APIException

from ..models import Asignacion, Auxilio, EstadoAuxilio

def generarAsignacion():
	auxilios_a_asignar = getAuxilioAAsignar()
	
	for	auxilio_a_asignar in auxilios_a_asignar:
		for asignacion in auxilio_a_asignar.asignaciones.all():
			if not asignacion.medico:
				medicos_libres = getMedicoAAsignar()
				if not medicos_libres:
					return True
				medico_a_asignar = filtrar_por_cercania(medicos_libres, auxilio_a_asignar.solicitud.ubicacion_coordenadas)
				asignacion.medico = medico_a_asignar
				asignacion.estado = Asignacion.EN_CAMINO
				asignacion.save()
				actualizarEstado(auxilio_a_asignar)
				# TODO: Verificar return de notificarMedico y ver que hacer.
				# Loguear en el servidor en la tabla de logueos.
				notificarMedico(medico_a_asignar, auxilio_a_asignar)
				medico_a_asignar.estado = Medico.EN_AUXILIO
				medico_a_asignar.save()


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
	coordenadas_2 = make_tuple(coordenadas_2)
	lat1 = coordenadas_1['lat']
	long1 = coordenadas_1['long']
	lat2 = coordenadas_2[0]
	long2 = coordenadas_2[1]
	
	r = 6371000 #radio terrestre medio, en metros
	c = pi / 180 #constante para transformar grados en radianes
	
	# Fórmula de Haversine
	distanciaHaversine = 2*r*asin(sqrt(sin(c*(lat2-lat1)/2)**2 + cos(c*lat1)*cos(c*lat2)*sin(c*(long2-long1)/2)**2))
	return distanciaHaversine


def actualizarEstado(auxilio):
	estadoActual = auxilio.estados.first()
	if estadoActual.estado != EstadoAuxilio.EN_CURSO:
		nuevo_estado = EstadoAuxilio.objects.create(estado = EstadoAuxilio.EN_CURSO)
		auxilio.estados.add(nuevo_estado)
		return True
	return False


def formatearUbicacion(ubicacion_coordenadas):
	lat_start = ubicacion_coordenadas.index("(") + 1
	lat_end = ubicacion_coordenadas.index(",")
	long_start = ubicacion_coordenadas.index(",") + 1
	long_end = ubicacion_coordenadas.index(")")
	return {
		'lat': ubicacion_coordenadas[lat_start:lat_end],
		'long': ubicacion_coordenadas[long_start:long_end]
	}


def notificarMedico(medico, auxilio):
	from auxilios.api.serializers import AuxilioSerializer

	url = 'https://fcm.googleapis.com/fcm/send'
	headers = {
		'Authorization': 'key=AAAACZOgn48:APA91bGC3G0xrAbVpOHAIx8zYnhk5fcIGahsgnfx-4fU5-IDGghNrSH0viM5JV2jjLL3PakaDPU5jlMvrKw9Mq9BkfQANGsI0f6weSXuDoDPc32qNQzzYhc-gBYtJy8KKzITU5mCPW6o',
		'Content-Type': 'application/json'
	}
	ubicacion = formatearUbicacion(auxilio.solicitud.ubicacion_coordenadas)
	data = {
		'lat': ubicacion['lat'],
		'long':ubicacion['long'],
		'direccion': auxilio.solicitud.ubicacion,
		'paciente': auxilio.solicitud.nombre,
		'colorDescripcion': auxilio.categoria.descripcion,
		'colorHexa': auxilio.categoria.color,
		'Motivos': json.loads(auxilio.solicitud.motivo)
	}
	payload = {
		'to': medico.fcm_code,
		'data': data
	}
	try:
		response = requests.post(url, headers=headers, json=payload, timeout=10)
		if response.status_code == requests.codes.ok:
			return True
		else:
			# TODO: Verificar codigo de error de google
			medico.estado = Medico.NO_DISPONIBLE
			return False
			# response.raise_for_status()
	except Exception as e:
		raise APIException(u'No fue posible enviar la notificación al médico DNI: %s.\nError: %s' %(medico.dni, e))
