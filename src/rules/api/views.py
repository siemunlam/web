# -*- coding: utf-8 -*-
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .extra_func import parseData

from .serializers import CategoriaSerializer, FactorDeAjusteSerializer, ReglaDeAjusteSerializer, ReglaDePreCategorizacionSerializer, ValorDeFactorDeAjusteSerializer, FactorDePreCategorizacionSerializer, ValorDeFactorDePreCategorizacionSerializer

from ..models import (Ajuste, Categoria, FactorDeAjuste,
					 FactorDePreCategorizacion, ReglaDeAjuste,
					 ReglaDePreCategorizacion, ValorDeFactorDeAjuste,
					 ValorDeFactorDePreCategorizacion)

# Create your views here.
class CategoriaViewset(ModelViewSet):
	permission_classes = [IsAuthenticatedOrReadOnly]
	queryset = Categoria.objects.all()
	serializer_class = CategoriaSerializer


class FactorDeAjusteViewSet(ModelViewSet):
	permission_classes = [IsAuthenticatedOrReadOnly]
	queryset = FactorDeAjuste.objects.all()
	serializer_class = FactorDeAjusteSerializer


class FactorDePreCategorizacionViewSet(ModelViewSet):
	permission_classes = [IsAuthenticatedOrReadOnly]
	queryset = FactorDePreCategorizacion.objects.all()
	serializer_class = FactorDePreCategorizacionSerializer


class ValorDeFactorDeAjusteViewSet(ModelViewSet):
	permission_classes = [IsAuthenticatedOrReadOnly]
	queryset = ValorDeFactorDeAjuste.objects.all()
	serializer_class = ValorDeFactorDeAjusteSerializer


class ValorDeFactorDePreCategorizacionViewSet(ModelViewSet):
	permission_classes = [IsAuthenticatedOrReadOnly]
	queryset = ValorDeFactorDePreCategorizacion.objects.all()
	serializer_class = ValorDeFactorDePreCategorizacionSerializer


class ReglaDeAjusteViewSet(ModelViewSet):
	permission_classes = [IsAuthenticatedOrReadOnly]
	queryset = ReglaDeAjuste.objects.all()
	serializer_class = ReglaDeAjusteSerializer


class ReglaDePreCategorizacionViewSet(ModelViewSet):
	permission_classes = [IsAuthenticatedOrReadOnly]
	queryset = ReglaDePreCategorizacion.objects.all()
	serializer_class = ReglaDePreCategorizacionSerializer


class MotivosAjustePIView(ListAPIView):
	permission_classes = [AllowAny]
	queryset = ValorDeFactorDeAjuste.objects.all()
	serializer_class = ValorDeFactorDeAjusteSerializer

	def list(self, request):
		queryset = self.get_queryset()
		serializer = ValorDeFactorDeAjusteSerializer(queryset, many=True)
		parsedData = parseData(serializer.data, 'factorDeAjuste')
		return Response(parsedData)


class MotivosPCAPIView(ListAPIView):
	permission_classes = [AllowAny]
	queryset = ValorDeFactorDePreCategorizacion.objects.all()
	serializer_class = ValorDeFactorDePreCategorizacionSerializer

	def list(self, request):
		queryset = self.get_queryset()
		serializer = ValorDeFactorDePreCategorizacionSerializer(queryset, many=True)
		parsedData = parseData(serializer.data, 'factorDePreCategorizacion')
		return Response(parsedData)