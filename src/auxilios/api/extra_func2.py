# -*- coding: utf-8 -*-
import requests
from rest_framework.exceptions import APIException

def notificarSuscriptores(auxilio, nuevoEstado):
	for suscriptor in auxilio.suscriptores.all():
		url = 'https://fcm.googleapis.com/fcm/send'
		headers = {
			'Authorization': 'key=AAAACZOgn48:APA91bGC3G0xrAbVpOHAIx8zYnhk5fcIGahsgnfx-4fU5-IDGghNrSH0viM5JV2jjLL3PakaDPU5jlMvrKw9Mq9BkfQANGsI0f6weSXuDoDPc32qNQzzYhc-gBYtJy8KKzITU5mCPW6o',
			'Content-Type': 'application/json'
		}
		mensaje = {
			'status': nuevoEstado.estado,
			'timestamp': nuevoEstado.fecha
		}
		payload = {
			'to': suscriptor.codigo,
			'data': mensaje
		}
		try:
			response = requests.post(url, headers=headers, json=payload, timeout=10)
			if response.status_code == requests.codes.ok:
				return True
			else:
				response.raise_for_status()
		except Exception as e:
			raise APIException(u'No fue posible enviar la notificación al suscriptor: %s.\nError: %s' %(suscriptor, e))