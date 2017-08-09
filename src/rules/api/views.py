# -*- coding: utf-8 -*-
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from .serializers import CategoriaSerializer, FactorDeAjusteSerializer, ReglaDeAjusteSerializer, ReglaDePreCategorizacionSerializer, ValorDeFactorDeAjusteSerializer, FactorDePreCategorizacionSerializer, ValorDeFactorDePreCategorizacionSerializer

from ..models import (Ajuste, Categoria, FactorDeAjuste,
					 FactorDePreCategorizacion, ReglaDeAjuste,
					 ReglaDePreCategorizacion, ValorDeFactorDeAjuste,
					 ValorDeFactorDePreCategorizacion)

# Create your views here.
class CategoriaViewset(ModelViewSet):
	permission_classes = [IsAuthenticated]
	queryset = Categoria.objects.all()
	serializer_class = CategoriaSerializer


class FactorDeAjusteViewSet(ModelViewSet):
	permission_classes = [IsAuthenticated]
	queryset = FactorDeAjuste.objects.all()
	serializer_class = FactorDeAjusteSerializer


class FactorDePreCategorizacionViewSet(ModelViewSet):
	permission_classes = [IsAuthenticated]
	queryset = FactorDePreCategorizacion.objects.all()
	serializer_class = FactorDePreCategorizacionSerializer


class ValorDeFactorDeAjusteViewSet(ModelViewSet):
	permission_classes = [IsAuthenticated]
	queryset = ValorDeFactorDeAjuste.objects.all()
	serializer_class = ValorDeFactorDeAjusteSerializer


class ValorDeFactorDePreCategorizacionViewSet(ModelViewSet):
	permission_classes = [IsAuthenticated]
	queryset = ValorDeFactorDePreCategorizacion.objects.all()
	serializer_class = ValorDeFactorDePreCategorizacionSerializer


class ReglaDeAjusteViewSet(ModelViewSet):
	permission_classes = [IsAuthenticated]
	queryset = ReglaDeAjuste.objects.all()
	serializer_class = ReglaDeAjusteSerializer


class ReglaDePreCategorizacionViewSet(ModelViewSet):
	permission_classes = [IsAuthenticated]
	queryset = ReglaDePreCategorizacion.objects.all()
	serializer_class = ReglaDePreCategorizacionSerializer