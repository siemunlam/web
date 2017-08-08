# -*- coding: utf-8 -*-
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet

from .serializers import AsignacionSerializer, AuxilioSerializer, EstadoAuxilioSerializer, SolicitudDeAuxilioSerializer
from ..models import Asignacion, Auxilio, EstadoAuxilio, SolicitudDeAuxilio #Movil


# Create your views here.
class AsignacionViewSet(ModelViewSet):
	queryset = Asignacion.objects.all()
	serializer_class = AsignacionSerializer
	permission_classes = (IsAuthenticatedOrReadOnly, )

	def perform_create(self, serializer):
		serializer.save(generador=self.request.user)


class AuxilioViewSet(ModelViewSet):
	queryset = Auxilio.objects.all()
	serializer_class = AuxilioSerializer
	#permission_classes = (IsAuthenticatedOrReadOnly, )


class SolicitudDeAuxilioViewSet(ModelViewSet):
	queryset = SolicitudDeAuxilio.objects.all()
	serializer_class = SolicitudDeAuxilioSerializer
	#permission_classes = (IsAuthenticatedOrReadOnly, )

	def perform_create(self, serializer):
		estado = EstadoAuxilio(estado=EstadoAuxilio.PENDIENTE, generador=User.objects.first())# self.request.user
		estado.save()
		solicitud = serializer.save(generador=User.objects.first())# self.request.user
		categorizarResultados = json.loads('{"categoria": "Rojo", "prioridad":15}') #self.categorizar(solicitud.motivo)
		categorizacion = Categoria.objects.get(descripcion=categorizarResultados['categoria'])
		auxilio = Auxilio(solicitud=solicitud, categoria=categorizacion, prioridad=categorizarResultados['prioridad'])
		auxilio.save()
		auxilio.estados.add(estado)
		auxilio.save()
	
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
			messages.error(self.request, u'No fue posible comunicarse con el servidor de categorizacion. Error: %s' %e, extra_tags='danger')
			return HttpResponseRedirect(reverse_lazy('home'))