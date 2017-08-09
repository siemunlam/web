# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework.filters import SearchFilter
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveDestroyAPIView, UpdateAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from .serializers import MedicoCreateSerializer, MedicoDetailSerializer, MedicoLogoutSerializer, MedicoUpdateSerializer
from ..models import Medico


# Create your views here.
User = get_user_model()


class MedicoCreateAPIView(CreateAPIView):
	permission_classes = [IsAdminUser]
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
		print(authenticated_user)
		return Medico.objects.get(usuario=authenticated_user)

	def perform_update(self, serializer):
		serializer.save(fcm_code='')


class MedicosRetrieveDestroyAPIView(RetrieveDestroyAPIView):
	permission_classes = [IsAuthenticated]
	queryset = Medico.objects.all()
	serializer_class = MedicoDetailSerializer

	def perform_destroy(self, instance):
		instance.usuario.delete()


class MedicoUpdateAPIView(UpdateAPIView):
	permission_classes = [IsAuthenticated]
	queryset = Medico.objects.all()
	serializer_class = MedicoUpdateSerializer