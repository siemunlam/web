from django.http import Http404
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework import viewsets

from .models import SolicitudDeAuxilio

from.serializers import SolicitudDeAuxilioSerializer


# Create your views here.
class SolicitudDeAuxilioViewSet(viewsets.ModelViewSet):
    queryset = SolicitudDeAuxilio.objects.all()
    serializer_class = SolicitudDeAuxilioSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

    def perform_create(self, serializer):
        serializer.save(generador=self.request.user)