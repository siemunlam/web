# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework.filters import SearchFilter
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveDestroyAPIView, RetrieveUpdateAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_403_FORBIDDEN



from .serializers import MedicoActualizarFCMSerializer, MedicoActualizarGPSSerializer,  MedicoCambioEstadoSerializer, MedicoCreateSerializer, MedicoDetailSerializer, MedicoLogoutSerializer, MedicoUpdateSerializer
from ..models import Medico
from auxilios.models import Asignacion


# Create your views here.
User = get_user_model()


class MedicoCreateAPIView(CreateAPIView):
	permission_classes = [IsAuthenticated]
	queryset = Medico.objects.all()
	serializer_class = MedicoCreateSerializer


class MedicoListAPIView(ListAPIView):
	permission_classes = [IsAuthenticated]
	queryset = Medico.objects.all()
	serializer_class = MedicoDetailSerializer
	filter_backends = [SearchFilter,]
	search_fields = ['dni', 'matricula', 'usuario__first_name', 'usuario__last_name']


class MedicosLogoutAPIView(UpdateAPIView):
	permission_classes = [IsAuthenticated]
	serializer_class = MedicoLogoutSerializer

	def get_object(self):
		authenticated_user = self.request.user
		return Medico.objects.get(usuario=authenticated_user)

	def perform_update(self, serializer):
		serializer.save(estado=Medico.NO_DISPONIBLE, fcm_code='', latitud_gps=None, longitud_gps=None)


class MedicosRetrieveDestroyAPIView(RetrieveDestroyAPIView):
	permission_classes = [IsAuthenticated]
	queryset = Medico.objects.all()
	serializer_class = MedicoDetailSerializer

	def destroy(self, request, *args, **kwargs):
		instance = self.get_object()
		if Asignacion.objects.filter(medico=instance).exists():
			error_message = { 
				'error_message' : u'El médico ya estuvo asignado a algún auxilio y no puede ser eliminado.'
			}
			return Response(error_message, status=HTTP_403_FORBIDDEN)
		self.perform_destroy(instance)
		return Response(status=HTTP_204_NO_CONTENT)

	def perform_destroy(self, instance):
		instance.usuario.delete()


class MedicoUpdateAPIView(UpdateAPIView):
	permission_classes = [IsAuthenticated]
	queryset = Medico.objects.all()
	serializer_class = MedicoUpdateSerializer


class MedicoCambioEstadoUpdateAPIView(RetrieveUpdateAPIView):
	permission_classes = [IsAuthenticated]
	queryset = Medico.objects.all()
	serializer_class = MedicoCambioEstadoSerializer

	def get_object(self):
		authenticated_user = self.request.user
		return Medico.objects.get(usuario=authenticated_user)

	def perform_update(self, serializer):
		serializer.save(generador=self.request.user)


class MedicoActualizarGPSUpdateAPIView(RetrieveUpdateAPIView):
	permission_classes = [IsAuthenticated]
	queryset = Medico.objects.all()
	serializer_class = MedicoActualizarGPSSerializer

	def get_object(self):
		authenticated_user = self.request.user
		return Medico.objects.get(usuario=authenticated_user)


class MedicoActualizarFCMUpdateAPIView(RetrieveUpdateAPIView):
	permission_classes = [IsAuthenticated]
	queryset = Medico.objects.all()
	serializer_class = MedicoActualizarFCMSerializer

	def get_object(self):
		authenticated_user = self.request.user
		return Medico.objects.get(usuario=authenticated_user)