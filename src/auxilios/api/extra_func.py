# -*- coding: utf-8 -*-
import json
from math import asin, cos, pi, sin, sqrt

import requests
from django.contrib import messages
from medicos.models import Medico
from rest_framework.exceptions import APIException

from ..models import Asignacion, Auxilio, EstadoAuxilio
from auxilios.api.serializers import AuxilioSerializer


def generarAsignacion():
	# 1. Buscar auxilio pendiente o en_curso màs prioritario que posea una asignacion vacia
	## Si no encuentro ninguno, salir.
	auxilio_a_asignar = getAuxilioAAsignar()
	print(u"El auxilio a asignar es el #%s" %(auxilio_a_asignar.id))
	if auxilio_a_asignar is None:
		print("No se encontraron auxilios para asignar")
		return False
	# 2 Buscar médico disponible que no esté en ninguna asignación 'EN CAMINO', 'EN EL LUGAR' o 'EN TRASLADO'
	# TODO: también buscar médicos disponibles con asignación 'EN CAMINO' y con categorización y prioridad del auxilio menor a la del auxilio a asignar.
	# Filtro por cercanìa. Me quedo solamente con uno.
	## Si no encuentro ninguno, salir.
	medicos_libres = getMedicoAAsignar()
	if not medicos_libres.exists():
		print(u"No se encontraron médicos libres para asignarle un auxilio")
		return False
	# 3.0 Seleccionar el médico màs cercano al auxilio
	medico_a_asignar = filtrar_por_cercania(medicos_libres, auxilio_a_asignar.solicitud.ubicacion_coordenadas)
	print(u"El médico más cercano al auxilio #%s es DNI%s" %(auxilio_a_asignar.id, medico_a_asignar.dni))
	# 3.1 Asignar el médico al auxilio
	nueva_asignacion = Asignacion.objects.create(medico=medico_a_asignar, estado=Asignacion.EN_CAMINO)
	auxilio_a_asignar.asignaciones.add(nueva_asignacion)
	# 3.2 Actualizar el estado del auxilio
	actualizarEstado(auxilio_a_asignar)
	print(u"Se cambió el estado del auxilio a EN_CURSO")
	# 3.3 Enviar notificacion al médico
	notificarMedico(medico_a_asignar, auxilio_a_asignar)
	# 3.4.1 Si el médico que encontré estaba vinculado a otro auxilio, lo desvinculo y llamo otra vez a generarAsignacion()
	# 3.4.2 Si el médico que encontré era el ùnico "asignado" a ese auxilio, pongo ese auxilio en 'pendiente'
	vincularMedico(medico_a_asignar, auxilio_a_asignar)


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
	# Busca el auxilio en estado PENDIENTE o EN CURSO màs prioritario que posea una asignacion sin atender
	# Es decir, que posea menos asignaciones que no tengas estado CANCELADA que moviles_requeridos
	## 1- Busco los auxilios en estado PENDIENTE o EN CURSO
	auxilios = filtrarAuxiliosPorEstado([EstadoAuxilio.PENDIENTE, EstadoAuxilio.EN_CURSO])
	## 2- Ya que los auxilios estan ordenados por categoria, prioridad y orden de llegada,
	## devuelvo el primero que encuentre que posee asignaciones sin atender.
	for auxilio in auxilios:
		if auxilio.solicitud.cantidad_moviles > obtenerAsignacionesAtendidas(auxilio.asignaciones):
			return auxilio
	return None


def obtenerAsignacionesAtendidas(asignaciones):
	asignaciones_atendidas = 0
	if asignaciones.count() > 0:
		for asignacion in asignaciones.all():
			if asignacion.estado in [Asignacion.EN_CAMINO, Asignacion.EN_LUGAR, Asignacion.EN_TRASLADO, Asignacion.FINALIZADA]:
				asignaciones_atendidas += 1
	return asignaciones_atendidas


def getMedicoAAsignar():
	# Busca los médicos en estado DISPONIBLE que tengan Ubicación y Firebase Code
	medicos_disponibles = Medico.objects.filter(estado=Medico.DISPONIBLE).exclude(latitud_gps=None, longitud_gps=None, fcm_code__exact='')
	# Busca a los médicos que estén atendiendo algún auxilio.
	medicos_asignados = Medico.objects.filter(asignacion__estado__in=[Asignacion.EN_CAMINO, Asignacion.EN_LUGAR, Asignacion.EN_TRASLADO])
	# Hace la diferencia limpiando los campos de ordenamiento de las queries
	# porque a Django no le gusta   -.-'
	medicos_disponibles.query.clear_ordering(force_empty=True)
	medicos_asignados.query.clear_ordering(force_empty=True)
	medicos_sin_asignar = medicos_disponibles.difference(medicos_asignados)
	# TODO:Éste es por las dudas. Tal vez se pueda sacar
	medicos_sin_asignar.query.clear_ordering(force_empty=True)
	return medicos_sin_asignar


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
	json1 = json.loads(coordenadas_1)
	json2 = json.loads(coordenadas_2)
	lat1 = json1['lat']
	long1 = json1['long']
	lat2 = json2['lat']
	long2 = json2['long']
	
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


def notificarMedico(medico, auxilio):
	url = 'https://fcm.googleapis.com/fcm/send'
	headers = {
		'Authorization': 'key=AAAACZOgn48:APA91bGC3G0xrAbVpOHAIx8zYnhk5fcIGahsgnfx-4fU5-IDGghNrSH0viM5JV2jjLL3PakaDPU5jlMvrKw9Mq9BkfQANGsI0f6weSXuDoDPc32qNQzzYhc-gBYtJy8KKzITU5mCPW6o',
		'Content-Type': 'application/json'
	}
	serializer = AuxilioSerializer(auxilio)
	payload = {
		'to': 'fQvZLJTvY-w:APA91bEDwlGbWbH6xdhy7U1xQP75-NLTtVqrOad7kv5-3rvIaMTW0xV_vKWfGOLQhSDooDbgZSD_pS1rS0wfA7yAM7_brlfoS_zii5RY6Pg5iX_gU3YpsB2584clUxwONv2zWqL-PHOy', #medico.fcm_code,
		'data': serializer.data
	}
	try:
		response = requests.post(url, headers=headers, json=payload, timeout=10)
		if response.status_code == requests.codes.ok:
			return True
		else:
			response.raise_for_status()
	except Exception as e:
		raise APIException(u'No fue posible enviar la notificación al médico DNI: %s.\nError: %s' %(medico.dni, e))


def vincularMedico(medico, auxilio=None, estado=Asignacion.DESVIADA):
	asignacion = Asignacion.objects.filter(medico=medico, estado__in=[Asignacion.EN_CAMINO, Asignacion.EN_LUGAR, Asignacion.EN_TRASLADO]).first()
	asignacion.estado = estado
	asignacion.save()
	if auxilio:
		nueva_asignacion = Asignacion.objects.create(medico=medico)
		auxilio.asignaciones.add(nueva_asignacion)
	#TODO
	#else:
		# Médico se desvincula y se crea otro auxilio?