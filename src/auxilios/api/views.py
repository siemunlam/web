# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from rest_framework.exceptions import APIException, NotFound
from rest_framework.filters import SearchFilter
from rest_framework.generics import (CreateAPIView, ListAPIView, ListCreateAPIView,
									 RetrieveAPIView, RetrieveUpdateAPIView)
from rest_framework.permissions import (AllowAny, IsAuthenticated)
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_404_NOT_FOUND
from rest_framework.viewsets import ModelViewSet
from rules.models import Categoria

from ..models import (
	Asignacion,
	Auxilio,
	EstadoAuxilio,  # Movil
	FormularioFinalizacion,
	Medico,
	Paciente,
	Suscriptor,
	SolicitudDeAuxilio)
from .extra_func import generarAsignacion, filtrarAuxiliosPorEstado, filtrarAuxiliosPorCategoria, filtrarAuxiliosPorFecha, filtrarAuxiliosPorUltimaActualizacion, ordenarAuxilios, MedicoNoVinculado
from .serializers import (
	AsignacionCambioEstadoSerializer, AsignacionSerializer, AsignacionDesvincularSerializer,
	AuxilioCambioEstadoSerializer, AuxilioUbicacionGPSSerializer, AuxilioSerializer, EstadoAuxilioSerializer,
	FormularioFinalizacionSerializer, SolicitudDeAuxilioSerializer, SolicitudDeAuxilioDetailSerializer,
	SuscriptorDetailSerializer)

import json, requests

# Create your views here.
User = get_user_model()

class AsignacionViewSet(ModelViewSet):
	permission_classes = [IsAuthenticated]
	queryset = Asignacion.objects.all()
	serializer_class = AsignacionSerializer


class AsignacionCambioEstadoAPIView(RetrieveUpdateAPIView):
	permission_classes = [IsAuthenticated]
	queryset = Asignacion.objects.all()
	serializer_class = AsignacionCambioEstadoSerializer

	def get_object(self):
		# Busca la asignación activa a la que está asociado el médico logueado
		try:
			return Asignacion.objects.get(
			medico__usuario=self.request.user,
			estado__in=[
				Asignacion.EN_CAMINO, Asignacion.EN_LUGAR,
				Asignacion.EN_TRASLADO
			])
		except Asignacion.DoesNotExist as e:
			raise MedicoNoVinculado()


class AsignacionDesvincularAPIView(RetrieveUpdateAPIView):
	permission_classes = [IsAuthenticated]
	queryset = Asignacion.objects.all()
	serializer_class = AsignacionDesvincularSerializer

	def get_object(self):
		# Busca la asignación activa a la que está asociado el médico logueado
		try:
			return Asignacion.objects.get(
			medico__usuario=self.request.user,
			estado__in=[
				Asignacion.EN_CAMINO, Asignacion.EN_LUGAR,
				Asignacion.EN_TRASLADO
			])
		except Asignacion.DoesNotExist as e:
			raise MedicoNoVinculado()

	def perform_update(self, serializer):
		serializer.save()


class AsignacionFinalizarAPIView(CreateAPIView):
	permission_classes = [IsAuthenticated]
	queryset = FormularioFinalizacion.objects.all()
	serializer_class = FormularioFinalizacionSerializer

	def get_object(self):
		# Busca la asignación activa a la que está asociado el médico logueado
		try:
			return Asignacion.objects.get(
			medico__usuario=self.request.user,
			estado__in=[
				Asignacion.EN_LUGAR,
				Asignacion.EN_TRASLADO
			])
		except Asignacion.DoesNotExist as e:
			raise MedicoNoVinculado()

	def perform_create(self, serializer):
		serializer.save(asignacion=self.get_object(),
						pacientes=self.getPacientesObj(self.request.data.get('pacientes', list())))
	
	def getPacientesObj(self, json_data):
		# Crea objetos Paciente desde JSON data
		pacientes = list()
		for paciente in json_data:
			dni = paciente.get('dni')
			apellido = paciente.get('apellido', "")
			nombre = paciente.get('nombre', "")
			edad = paciente.get('edad')
			telefono = paciente.get('telefono', "")
			diagnostico = paciente.get('diagnostico')
			trasladado = paciente.get('trasladado')
			p = Paciente.objects.create(
				dni=dni,
				apellido=apellido,
				nombre=nombre,
				edad=edad,
				telefono=telefono,
				diagnostico=diagnostico,
				trasladado=trasladado)
			pacientes.append(p.id)
		return pacientes


class AuxilioViewSet(ModelViewSet):
	permission_classes = [AllowAny]
	serializer_class = AuxilioSerializer
	filter_backends = [SearchFilter]
	search_fields = ['solicitud__ubicacion']

	def categorizar(self, motivo):
		url = settings.WS_CATEGORIZAR
		try:
			response = requests.post(
				url, data='inputjson=' + motivo, timeout=10)
			result = None
			if response.status_code == requests.codes.ok:
				result = response.json()
			else:
				response.raise_for_status()
			return result
		except Exception as e:
			raise APIException(
				u'No fue posible comunicarse con el servidor de categorización.\nError: %s'
				% e)

	def create(self, request, *args, **kwargs):
		serializer = SolicitudDeAuxilioSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		self.perform_create(serializer)
		headers = self.get_success_headers(serializer.data)
		auxilio_creado = Auxilio.objects.get(solicitud__id=serializer.data['id'])
		custom_response = {'codigo_suscripcion': auxilio_creado.codigo_suscripcion}
		if serializer.data['origen'] == SolicitudDeAuxilio.WEB_APP:
			custom_response.update({'id': auxilio_creado.id})
		return Response(custom_response, status=HTTP_201_CREATED, headers=headers)

	def get_queryset(self):
		object_list = Auxilio.objects.all()
		object_list = filtrarAuxiliosPorFecha(object_list, self.request.GET.get('desde'), self.request.GET.get('hasta'))
		object_list = filtrarAuxiliosPorUltimaActualizacion(object_list, self.request.GET.get('fin_desde'), self.request.GET.get('fin_hasta'))
		object_list = filtrarAuxiliosPorCategoria(object_list, self.request.GET.getlist('categoria'))
		object_list = filtrarAuxiliosPorEstado(object_list, self.request.GET.getlist('estado'))
		if self.request.GET.get('ordering'):
			object_list = ordenarAuxilios(object_list, self.request.GET.getlist('ordering'))
		return object_list

	def perform_create(self, serializer):
		if not self.request.user.is_anonymous():
			solicitud = serializer.save(generador=self.request.user)
		else:
			solicitud = serializer.save()
		# categorizarResultados = {
		# 	"categoria": "Rojo",
		# 	"prioridad": 15
		# }
		categorizarResultados = self.categorizar(solicitud.motivo)
		categorizacion = Categoria.objects.get(
			descripcion=categorizarResultados['categoria'])
		auxilio = Auxilio.objects.create(
			solicitud=solicitud,
			categoria=categorizacion,
			prioridad=categorizarResultados['prioridad'])
		serializer = AuxilioCambioEstadoSerializer(auxilio, data={'estados': [{'estado': EstadoAuxilio.PENDIENTE}]})
		serializer.is_valid()
		serializer.save()
		for index in range(solicitud.cantidad_moviles):
			asignacion = Asignacion.objects.create(estado=Asignacion.PENDIENTE)
			auxilio.asignaciones.add(asignacion)
		generarAsignacion()


class AuxilioCambioEstadoUpdateAPIView(RetrieveUpdateAPIView):
	permission_classes = [IsAuthenticated]
	queryset = Auxilio.objects.all()
	serializer_class = AuxilioCambioEstadoSerializer

	def perform_update(self, serializer):
		serializer.save(generador=self.request.user)


class AuxilioUbicacionGPSListAPIView(ListAPIView):
	permission_classes = [IsAuthenticated]
	serializer_class = AuxilioUbicacionGPSSerializer

	def get_queryset(self):
		object_list = Auxilio.objects.all()
		object_list = filtrarAuxiliosPorCategoria(object_list, self.request.GET.getlist('categoria'))
		object_list = filtrarAuxiliosPorEstado(object_list, self.request.GET.getlist('estado'))
		return object_list


class SolicitudDeAuxilioDetailsListAPIView(ListAPIView):
	permission_classes = [IsAuthenticated]
	queryset = SolicitudDeAuxilio.objects.all()
	serializer_class = SolicitudDeAuxilioDetailSerializer
	filter_backends = [SearchFilter,]
	search_fields = ['fecha']


class SuscriptoresDeAuxilio(CreateAPIView):
	permission_classes = [AllowAny]
	queryset = Suscriptor.objects.all()
	serializer_class = SuscriptorDetailSerializer

	def create(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		self.perform_create(serializer)
		headers = self.get_success_headers(serializer.data)
		responseData = dict(serializer.data)
		responseData['status'] = Auxilio.objects.get(codigo_suscripcion=self.kwargs['codigo_suscripcion']).estados.first().get_estado_display()
		return Response(responseData, status=HTTP_201_CREATED, headers=headers)

	def get_serializer_context(self):
		return {'codigo_suscripcion': self.kwargs['codigo_suscripcion']}


class FormularioFinalizacionRetrieveAPIView(RetrieveAPIView):
	permission_classes = [IsAuthenticated]
	queryset = FormularioFinalizacion.objects.all()
	serializer_class = FormularioFinalizacionSerializer