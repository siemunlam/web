# -*- coding: utf-8 -*-
import json

import requests
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from rest_framework.exceptions import APIException
from rest_framework.filters import SearchFilter
from rest_framework.generics import (CreateAPIView, ListAPIView,
                                     RetrieveUpdateAPIView)
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.viewsets import ModelViewSet
from rules.models import Categoria

from ..models import (Asignacion, Auxilio, EstadoAuxilio,  # Movil
                      FormularioFinalizacion, Paciente, SolicitudDeAuxilio)
from .extra_func import generarAsignacion
from .serializers import (AsignacionCambioEstadoSerializer,
                          AsignacionSerializer, AuxilioCambioEstadoSerializer,
                          AuxilioSerializer, EstadoAuxilioSerializer,
                          FormularioFinalizacionSerializer,
                          SolicitudDeAuxilioSerializer)


# Create your views here.
User = get_user_model()

class AsignacionViewSet(ModelViewSet):
	queryset = Asignacion.objects.all()
	serializer_class = AsignacionSerializer
	permission_classes = [AllowAny, ]


class AsignacionCambioEstadoAPIView(RetrieveUpdateAPIView):
	permission_classes = [AllowAny]
	queryset = Asignacion.objects.all()
	serializer_class = AsignacionCambioEstadoSerializer

	def get_object(self):
		# Busca la asignación activa a la que está asociado el médico logueado
		return Asignacion.objects.get(medico__usuario=self.request.user, estado__in=[Asignacion.EN_CAMINO, Asignacion.EN_LUGAR, Asignacion.EN_TRASLADO])


class AsignacionDesvincularAPIView(RetrieveUpdateAPIView):
	permission_classes = [AllowAny]
	queryset = Asignacion.objects.all()
	serializer_class = AsignacionCambioEstadoSerializer

	def get_object(self):
		# Busca la asignación activa a la que está asociado el médico logueado
		return Asignacion.objects.get(medico__usuario=self.request.user, estado__in=[Asignacion.EN_CAMINO, Asignacion.EN_LUGAR, Asignacion.EN_TRASLADO])

	def perform_update(self, serializer):
		serializer.save(medico = None, estado = Asignacion.PENDIENTE)


class AsignacionFinalizarAPIView(CreateAPIView):
	permission_classes = [AllowAny]
	queryset = FormularioFinalizacion.objects.all()
	serializer_class = FormularioFinalizacionSerializer

	def create(self, request, *args, **kwargs):
		# Crea los pacientes y envía al formulario los IDs
		pacientes = []
		for paciente in request.data.get('pacientes', []):
			dni = paciente.get('dni')
			apellido = paciente.get('apellido', "")
			nombre = paciente.get('nombre', "")
			fecha_naciemiento = paciente.get('fecha_nacimiento')
			telefono = paciente.get('telefono', "")
			motivo_atencion = paciente.get('motivo_atencion')
			trasladado = paciente.get('trasladado')
			p = Paciente.objects.create(dni=dni, apellido=apellido, nombre=nombre, fecha_naciemiento=fecha_naciemiento, telefono=telefono, motivo_atencion=motivo_atencion, trasladado=trasladado)
			pacientes.append(p.id)
		request.data['pacientes'] = pacientes
		return super(AsignacionFinalizarAPIView, self).create(request, *args, **kwargs)


	def perform_create(self, serializer):
		# Asocia el formulario a la ÚNICA asignación activa a la que está asociado el médico logueado
		asignacion = Asignacion.objects.get(medico__usuario=self.request.user, estado__in=[Asignacion.EN_LUGAR, Asignacion.EN_TRASLADO])
		serializer.save(asignacion = asignacion)


class AuxilioViewSet(ModelViewSet):	
	permission_classes = [AllowAny, ]
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


class AuxilioCambioEstadoUpdateAPIView(RetrieveUpdateAPIView):
	permission_classes = [AllowAny]
	queryset = Auxilio.objects.all()
	serializer_class = AuxilioCambioEstadoSerializer

	def perform_update(self, serializer):
		serializer.save(generador=self.request.user)


class SolicitudDeAuxilioViewSet(ModelViewSet):
	permission_classes = [AllowAny, ]
	queryset = SolicitudDeAuxilio.objects.all()
	serializer_class = SolicitudDeAuxilioSerializer
	
	def perform_create(self, serializer):
		solicitud = serializer.save(generador=User.objects.first())# self.request.user
		categorizarResultados = json.loads('{"categoria": "Rojo", "prioridad":15}')#self.categorizar(solicitud.motivo)
		categorizacion = Categoria.objects.get(descripcion=categorizarResultados['categoria'])
		auxilio = Auxilio.objects.create(solicitud=solicitud, categoria=categorizacion, prioridad=categorizarResultados['prioridad'])
		estado = EstadoAuxilio.objects.create(estado=EstadoAuxilio.PENDIENTE)
		auxilio.estados.add(estado)
		for i in range(solicitud.cantidad_moviles):
			asignacion = Asignacion.objects.create(estado=Asignacion.PENDIENTE)
			auxilio.asignaciones.add(asignacion)
		generarAsignacion()
	
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
			raise APIException(u'No fue posible comunicarse con el servidor de categorización.\nError: %s' %e)
