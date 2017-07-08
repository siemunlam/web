# -*- coding: utf-8 -*-
from rest_framework import permissions, viewsets
from django.views.generic import TemplateView
from .models import SolicitudDeAuxilio, Movil

from.serializers import SolicitudDeAuxilioSerializer, MovilSerializer


# Create your views here.
class SolicitudDeAuxilioViewSet(viewsets.ModelViewSet):
    queryset = SolicitudDeAuxilio.objects.all()
    serializer_class = SolicitudDeAuxilioSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

    def perform_create(self, serializer):
        serializer.save(generador=self.request.user)


#@method_decorator(login_required, name='dispatch')
class AuxiliosListView(TemplateView):
	template_name = 'auxilios-list.html'


class MovilViewSet(viewsets.ModelViewSet):
    queryset = Movil.objects.all()
    serializer_class = MovilSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

    def perform_create(self, serializer):
        serializer.save(generador=self.request.user)


#@method_decorator(login_required, name='dispatch')
class MovilListView(TemplateView):
	template_name = 'moviles-list.html'