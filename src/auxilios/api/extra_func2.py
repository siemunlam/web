# -*- coding: utf-8 -*-
import json, requests
from django.conf import settings
from rest_framework.exceptions import APIException

def notificarSuscriptores(suscriptores, mensaje):
	for suscriptor in suscriptores:
		url = 'https://fcm.googleapis.com/fcm/send'
		headers = {
			'Authorization': 'key=%s' %settings.FIREBASE_AUTHORIZATION_KEY_SUSCRIPTORES,
			'Content-Type': 'application/json'
		}
		payload = {
			'to': suscriptor.codigo,
			'data': mensaje
		}
		payload = json.dumps(payload, ensure_ascii=False, default=str)
		# print(payload)
		try:
			response = requests.post(url, headers=headers, data=payload, timeout=10)
			# print("Response status %s - text %s\n" %(response.status_code, response.text))
			# if response.status_code == requests.codes.ok:
			# 	print(u'mensaje a suscriptor enviado con éxito')
			# else:
			# 	print(u'mensaje a suscriptor falló')
			# 	# TODO: hacer algo para evitar la Exception
			# 	response.raise_for_status()
		except Exception as e:
			pass
			# raise APIException(u'No fue posible enviar la notificación al suscriptor: %s.\nError: %s' %(suscriptor, e))