# -*- coding: utf-8 -*-
from rest_framework import permissions, viewsets

from .models import SolicitudDeAuxilio

from.serializers import SolicitudDeAuxilioSerializer


# Create your views here.
class SolicitudDeAuxilioViewSet(viewsets.ModelViewSet):
    queryset = SolicitudDeAuxilio.objects.all()
    serializer_class = SolicitudDeAuxilioSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

    def perform_create(self, serializer):
        serializer.save(generador=self.request.user)
