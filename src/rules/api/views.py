# -*- coding: utf-8 -*-
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveDestroyAPIView, RetrieveUpdateAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .extra_func import parseData
from .serializers import (CategoriaSerializer, UpdateCategoriaSerializer,
						  ReglaDeAjusteSerializer,
						  FactorDeAjusteSerializer, UpdateFactorDeAjusteSerializer,
						  ValorDeFactorDeAjusteSerializer, UpdateValorDeFactorDeAjusteSerializer,
						  ReglaDePreCategorizacionSerializer, UpdateReglaDePreCategorizacionSerializer,
						  FactorDePreCategorizacionSerializer, UpdateFactorDePreCategorizacionSerializer, 
						  ValorDeFactorDePreCategorizacionSerializer, UpdateValorDeFactorDePreCategorizacionSerializer)

from ..models import (Ajuste, Categoria, FactorDeAjuste,
					 FactorDePreCategorizacion, ReglaDeAjuste,
					 ReglaDePreCategorizacion, ValorDeFactorDeAjuste,
					 ValorDeFactorDePreCategorizacion)

# Create your views here.
class CategoriaViewset(ModelViewSet):
	permission_classes = [IsAuthenticated]
	queryset = Categoria.objects.all()
	serializer_class = CategoriaSerializer

class CategoriaUpdateAPIView(UpdateAPIView):
	permission_classes = [IsAuthenticated]
	queryset = Categoria.objects.all()
	serializer_class = UpdateCategoriaSerializer

class FactorDeAjusteViewSet(ModelViewSet):
	permission_classes = [IsAuthenticated]
	queryset = FactorDeAjuste.objects.all()
	serializer_class = FactorDeAjusteSerializer

class FactorDeAjusteUpdateAPIView(UpdateAPIView):
	permission_classes = [IsAuthenticated]
	queryset = FactorDeAjuste.objects.all()
	serializer_class = UpdateFactorDeAjusteSerializer


class ValorDeFactorDeAjusteViewSet(ModelViewSet):
	permission_classes = [IsAuthenticated]
	queryset = ValorDeFactorDeAjuste.objects.all()
	serializer_class = ValorDeFactorDeAjusteSerializer


class ValorDeFactorDeAjusteUpdateAPIView(UpdateAPIView):
	permission_classes = [IsAuthenticated]
	queryset = ValorDeFactorDeAjuste.objects.all()
	serializer_class = UpdateValorDeFactorDeAjusteSerializer


class FactorDePreCategorizacionViewSet(ModelViewSet):
	permission_classes = [IsAuthenticated]
	queryset = FactorDePreCategorizacion.objects.all()
	serializer_class = FactorDePreCategorizacionSerializer


class FactorDePreCategorizacionUpdateAPIView(UpdateAPIView):
	permission_classes = [IsAuthenticated]
	queryset = FactorDePreCategorizacion.objects.all()
	serializer_class = UpdateFactorDePreCategorizacionSerializer


class ValorDeFactorDePreCategorizacionViewSet(ModelViewSet):
	permission_classes = [IsAuthenticated]
	queryset = ValorDeFactorDePreCategorizacion.objects.all()
	serializer_class = ValorDeFactorDePreCategorizacionSerializer


class ValorDeFactorDePreCategorizacionUpdateAPIView(UpdateAPIView):
	permission_classes = [IsAuthenticated]
	queryset = ValorDeFactorDePreCategorizacion.objects.all()
	serializer_class = UpdateValorDeFactorDePreCategorizacionSerializer


class ReglaDeAjusteViewSet(ModelViewSet):
	permission_classes = [IsAuthenticated]
	queryset = ReglaDeAjuste.objects.all()
	serializer_class = ReglaDeAjusteSerializer


class ReglaDePreCategorizacionViewSet(ModelViewSet):
	permission_classes = [IsAuthenticated]
	queryset = ReglaDePreCategorizacion.objects.all()
	serializer_class = ReglaDePreCategorizacionSerializer


class ReglaDePreCategorizacionUpdateAPIView(UpdateAPIView):
	permission_classes = [IsAuthenticated]
	queryset = ReglaDePreCategorizacion.objects.all()
	serializer_class = UpdateReglaDePreCategorizacionSerializer


class MotivosAjustePIView(ListAPIView):
	permission_classes = [AllowAny]
	queryset = ValorDeFactorDeAjuste.objects.all()
	serializer_class = ValorDeFactorDeAjusteSerializer

	def list(self, request):
		queryset = self.get_queryset()
		serializer = ValorDeFactorDeAjusteSerializer(queryset, many=True)
		data = parseData(serializer.data, 'factorDeAjuste')
		return Response(data)


class MotivosPCAPIView(ListAPIView):
	permission_classes = [AllowAny]
	queryset = ValorDeFactorDePreCategorizacion.objects.all()
	serializer_class = ValorDeFactorDePreCategorizacionSerializer

	def list(self, request):
		queryset = self.get_queryset()
		serializer = ValorDeFactorDePreCategorizacionSerializer(queryset, many=True)
		data = parseData(serializer.data, 'factorDePreCategorizacion')
		return Response(data)