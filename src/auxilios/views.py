# -*- coding: utf-8 -*-
from rest_framework import permissions, viewsets
from django.views.generic import TemplateView
from django.core.urlresolvers import reverse_lazy

from .serializers import SolicitudDeAuxilioSerializer, MovilSerializer, AsignacionSerializer, AuxilioSerializer, MedicoSerializer, EstadoAuxilioSerializer
from .forms import SolicitudDeAuxilioForm
from .models import SolicitudDeAuxilio, Movil, Asignacion, Auxilio, Medico, EstadoAuxilio
from rules.models import Categoria

from django.contrib.auth.models import User
import requests

# Create your views here.
class SolicitudDeAuxilioViewSet(viewsets.ModelViewSet):
	queryset = SolicitudDeAuxilio.objects.all()
	serializer_class = SolicitudDeAuxilioSerializer
	#permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

	def perform_create(self, serializer):
		estado = EstadoAuxilio(estado=EstadoAuxilio.PENDIENTE, generador=User.objects.first())# self.request.user
		estado.save()
		solicitud = serializer.save(generador=User.objects.first())# self.request.user
		categorizacion = Categoria.objects.get(descripcion='Rojo')#self.categorizar(solicitud.motivo))
		auxilio = Auxilio(solicitud=solicitud, categoria=categorizacion)
		auxilio.save()
		auxilio.estados.add(estado)
		auxilio.save()
	
	def categorizar(self, motivo):
		url = 'http://ec2-54-232-217-35.sa-east-1.compute.amazonaws.com:8085/serviciosSoporte/obtenerCategoria/'
		response = requests.post(url, data='inputjson='+motivo, timeout=10)
		result = None
		if response.status_code == requests.codes.ok:
			result = response.text
			print(result)
		else:
			response.raise_for_status()
		return result


class AuxilioViewSet(viewsets.ModelViewSet):
	queryset = Auxilio.objects.all()
	serializer_class = AuxilioSerializer
	#permission_classes = (permissions.IsAuthenticatedOrReadOnly, )


#@method_decorator(login_required, name='dispatch')
class AuxiliosListView(TemplateView):
	template_name = 'auxilios-list.html'

	def get_context_data(self, **kwargs):
		context = super(AuxiliosListView, self).get_context_data(**kwargs)
		context['form'] = SolicitudDeAuxilioForm
		context['apiURL'] = reverse_lazy('api:vdfda-list')#, reverse_lazy('api:vdfdpc')]
		return context


class MovilViewSet(viewsets.ModelViewSet):
	queryset = Movil.objects.all()
	serializer_class = MovilSerializer
	permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

	def perform_create(self, serializer):
		serializer.save(generador=self.request.user)


#@method_decorator(login_required, name='dispatch')
class MovilListView(TemplateView):
	template_name = 'moviles-list.html'


class AsignacionViewSet(viewsets.ModelViewSet):
	queryset = Asignacion.objects.all()
	serializer_class = AsignacionSerializer
	permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

	def perform_create(self, serializer):
		serializer.save(generador=self.request.user)


#@method_decorator(login_required, name='dispatch')
class AsignacionListView(TemplateView):
	template_name = 'asignaciones-list.html'


class MedicoViewSet(viewsets.ModelViewSet):
	queryset = Medico.objects.all()
	serializer_class = MedicoSerializer
	permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

	def perform_create(self, serializer):
		serializer.save(generador=self.request.user)


#@method_decorator(login_required, name='dispatch')
class MedicoListView(TemplateView):
	template_name = 'medicos-list.html'