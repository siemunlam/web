# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from rest_framework.filters import SearchFilter
from rest_framework.generics import RetrieveUpdateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.viewsets import ModelViewSet

from .serializers import AsignacionSerializer, AuxilioSerializer, AuxilioCambioEstadoSerializer, EstadoAuxilioSerializer, SolicitudDeAuxilioSerializer
from ..models import Asignacion, Auxilio, EstadoAuxilio, SolicitudDeAuxilio #Movil
from rules.models import Categoria

import requests, json


# Create your views here.
User = get_user_model()

class AsignacionViewSet(ModelViewSet):
	queryset = Asignacion.objects.all()
	serializer_class = AsignacionSerializer
	permission_classes = (IsAuthenticatedOrReadOnly, )

	def perform_create(self, serializer):
		serializer.save(generador=self.request.user)


class AuxilioViewSet(ModelViewSet):	
	serializer_class = AuxilioSerializer
	def get_queryset(self):
		estado_filter = ', '.join(self.request.GET.getlist('estado', None))
		if estado_filter:
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
						AND (auxilios_estadoauxilio.estado in (%s)))'''%estado_filter			
			object_list = list(Auxilio.objects.raw(query))
		else:
			object_list = Auxilio.objects.all()
		return object_list
	#permission_classes = (IsAuthenticatedOrReadOnly, )


class AuxilioCambioEstadoUpdateAPIView(RetrieveUpdateAPIView):
	permission_classes = [IsAuthenticated]
	queryset = Auxilio.objects.all()
	serializer_class = AuxilioCambioEstadoSerializer

	def perform_update(self, serializer):
		serializer.save(generador=self.request.user)


class SolicitudDeAuxilioViewSet(ModelViewSet):
	queryset = SolicitudDeAuxilio.objects.all()
	serializer_class = SolicitudDeAuxilioSerializer
	#permission_classes = (IsAuthenticatedOrReadOnly, )

	def perform_create(self, serializer):
		estado = EstadoAuxilio(estado=EstadoAuxilio.PENDIENTE, generador=User.objects.first())# self.request.user
		estado.save()
		solicitud = serializer.save(generador=User.objects.first())# self.request.user
		categorizarResultados = json.loads('{"categoria": "Rojo", "prioridad":15}') #self.categorizar(solicitud.motivo)
		categorizacion = Categoria.objects.get(descripcion=categorizarResultados['categoria'])
		auxilio = Auxilio(solicitud=solicitud, categoria=categorizacion, prioridad=categorizarResultados['prioridad'])
		auxilio.save()
		auxilio.estados.add(estado)
		auxilio.save()
	
	def categorizar(self, motivo):
		url = 'http://ec2-18-231-57-236.sa-east-1.compute.amazonaws.com:8085/serviciosSoporte/obtenerCategoria/'
		try:
			response = requests.post(url, data='inputjson='+motivo, timeout=10)
			result = None
			if response.status_code == requests.codes.ok:
				result = response.json()
			else:
				response.raise_for_status()
			return result
		except Exception as e:
			messages.error(self.request, u'No fue posible comunicarse con el servidor de categorizacion. Error: %s' %e, extra_tags='danger')
			return HttpResponseRedirect(reverse_lazy('home'))