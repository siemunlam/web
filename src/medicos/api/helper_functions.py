# -*- coding: utf-8 -*-
import json, requests
from django.conf import settings
from rest_framework.exceptions import APIException
from medicos.models import Medico

def notificarMedico(medico, mensaje):
	url = 'https://fcm.googleapis.com/fcm/send'
	headers = {
		'Authorization': 'key=%s' %settings.FIREBASE_AUTHORIZATION_KEY,
		'Content-Type': 'application/json'
	}
	payload = {
		'to': medico.fcm_code,
		'data': mensaje
	}
	try:
		response = requests.post(url, headers=headers, json=payload, timeout=10)
		# print("Response status %s - text %s\n" %(response.status_code, response.text))
		if response.status_code == requests.codes.ok:
			# print(u"Se notificó al médico %s" %medico.dni)
			return True
		else:
			# TODO: Verificar codigo de error de google
			medico.estado = Medico.NO_DISPONIBLE
			medico.save()
			return False
			# response.raise_for_status()
	except Exception as e:
		raise APIException(u'No fue posible enviar la notificación al médico DNI: %s.\nError: %s' %(medico.dni, e))


def get_estimated_time_distance(origen, destino):
	url = 'https://maps.googleapis.com/maps/api/distancematrix/json?language=es&'
	url += 'origins=' + str(origen['lat']) + ',' + str(origen['long']) + '&destinations=' + str(destino['lat']) + ',' + str(destino['long'])
	try:
		response = requests.get(url, timeout=10)
		# print("Response status %s - text %s\n" %(response.status_code, response.text))
		if response.status_code == requests.codes.ok:
			resp = response.json()
			return {
				'distancia': resp['rows'][0]['elements'][0]['distance']['text'],
				'tiempo':resp['rows'][0]['elements'][0]['duration']['text']
			}
		else:
			# TODO: Verificar codigo de error de google
			return False
	except Exception as e:
		return 'Ocurrió un error.'