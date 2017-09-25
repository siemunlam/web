# -*- coding: utf-8 -*-
import json

from rest_framework.exceptions import APIException

from medicos.api.serializers import MedicoCambioEstadoSerializer
from medicos.models import Medico

def notificarMedico(medico, mensaje):
	url = 'https://fcm.googleapis.com/fcm/send'
	headers = {
		'Authorization': 'key=AAAACZOgn48:APA91bGC3G0xrAbVpOHAIx8zYnhk5fcIGahsgnfx-4fU5-IDGghNrSH0viM5JV2jjLL3PakaDPU5jlMvrKw9Mq9BkfQANGsI0f6weSXuDoDPc32qNQzzYhc-gBYtJy8KKzITU5mCPW6o',
		'Content-Type': 'application/json'
	}
	payload = {
		'to': medico.fcm_code,
		'data': mensaje #json.dumps(mensaje, ensure_ascii=False, default=str)
	}
	try:
		response = requests.post(url, headers=headers, json=payload, timeout=10)
		if response.status_code == requests.codes.ok:
			return True
		else:
			# TODO: Verificar codigo de error de google
			serializer = MedicoCambioEstadoSerializer(medico, data={'estado': Medico.NO_DISPONIBLE})
			serializer.is_valid()
			serializer.save()
			return False
	except Exception as e:
		raise APIException(u'No fue posible enviar la notificación al médico DNI: %s.\nError: %s' %(medico.dni, e))