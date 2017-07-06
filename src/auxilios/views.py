from django.http import Http404
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, status
from rest_framework.response import Response

from .models import SolicitudDeAuxilio

from.serializers import SolicitudDeAuxilioSerializer


# Create your views here.
class SolicitudDeAuxilioList(generics.ListCreateAPIView):
    queryset = SolicitudDeAuxilio.objects.all()
    serializer_class = SolicitudDeAuxilioSerializer

    def post(self, request, format=None):
        serializer = SolicitudDeAuxilioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(generador=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SolicitudDeAuxilioDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = SolicitudDeAuxilio.objects.all()
    serializer_class = SolicitudDeAuxilioSerializer
