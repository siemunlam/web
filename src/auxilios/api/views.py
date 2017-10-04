# -*- coding: utf-8 -*-
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
from .extra_func import generarAsignacion
from .serializers import (
	AsignacionCambioEstadoSerializer, AsignacionSerializer, AsignacionDesvincularSerializer,
	AuxilioCambioEstadoSerializer, AuxilioSerializer, EstadoAuxilioSerializer,
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
			raise NotFound(detail=u'El médico no está vinculado a un auxilio')


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
			raise NotFound(detail=u'El médico no está vinculado a un auxilio')

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
			raise NotFound(detail=u'El médico no está vinculado a un auxilio')

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

	def categorizar(self, motivo):
		url = 'http://ec2-54-233-80-23.sa-east-1.compute.amazonaws.com:8085/serviciosSoporte/obtenerCategoria/'
		try:
			response = requests.post(
				url, data='inputjson=' + motivo.encode('utf-8'), timeout=10)
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
			# Solamente paso el ID de la solicitud 
			custom_response.update({'id': auxilio_creado.id})
		return Response(custom_response, status=HTTP_201_CREATED, headers=headers)

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
						AND (auxilios_estadoauxilio.estado in (%s)))''' % estado_filter
			object_list = list(Auxilio.objects.raw(query))
		else:
			object_list = Auxilio.objects.all()
		return object_list

	def perform_create(self, serializer):
		solicitud = serializer.save(
			generador=User.objects.first())  # self.request.user
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


class SolicitudDeAuxilioDetailsListAPIView(ListAPIView):
	permission_classes = [IsAuthenticated]
	queryset = SolicitudDeAuxilio.objects.all()
	serializer_class = SolicitudDeAuxilioDetailSerializer
	filter_backends = [SearchFilter,]
	search_fields = ['fecha']


class SuscriptoresDeAuxilio(ListCreateAPIView):
	permission_classes = [IsAuthenticated]
	queryset = Suscriptor.objects.all()
	serializer_class = SuscriptorDetailSerializer

	def create(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		self.perform_create(serializer)
		headers = self.get_success_headers(serializer.data)
		responseData = dict(serializer.data)
		responseData['status'] = Auxilio.objects.get(id=self.kwargs['pk']).estados.first().estado
		return Response(responseData, status=HTTP_201_CREATED, headers=headers)


class FormularioFinalizacionRetrieveAPIView(RetrieveAPIView):
	permission_classes = [IsAuthenticated]
	queryset = FormularioFinalizacion.objects.all()
	serializer_class = FormularioFinalizacionSerializer