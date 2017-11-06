# -*- coding: utf-8 -*-
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveDestroyAPIView, RetrieveUpdateAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet

from .extra_func import parseData
from ..extra_func import calcAjustesResultantes
from .serializers import (AjusteSerializer,
						  CategoriaSerializer, UpdateCategoriaSerializer,
						  ReglaDeAjusteSerializer, UpdateReglaDeAjusteSerializer,
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

class AjusteViewSet(ModelViewSet):
	permission_classes = [IsAuthenticated]
	queryset = Ajuste.objects.all()
	serializer_class = AjusteSerializer


class CategoriaViewset(ModelViewSet):
	permission_classes = [IsAuthenticated]
	queryset = Categoria.objects.all()
	serializer_class = CategoriaSerializer

	def destroy(self, request, *args, **kwargs):
		# No elimina categorías con reglas de precategorización asociadas
		# o categorías que provocarían la eliminación de ajustes con reglas de ajuste asociadas
		instance = self.get_object()
		if ReglaDePreCategorizacion.objects.filter(resultado=instance).exists():
			return Response(u'Imposible eliminar la categoría "%s" porque tiene reglas de precategorización asociadas.' %(instance.descripcion), status=status.HTTP_403_FORBIDDEN)
		elif ReglaDeAjuste.objects.filter(resultado=ajuste_top).exists():
			return Response(u'Imposible eliminar la categoría "%s" porque borraría el ajuste de valor %d, el cual tiene reglas de precategorización asociadas.' %(instance.descripcion, ajuste_top.valor), status=status.HTTP_403_FORBIDDEN)
		elif ReglaDeAjuste.objects.filter(resultado=Ajuste.objects.last()).exists():
			return Response(u'Imposible eliminar la categoría "%s" porque borraría el ajuste de valor %d, el cual tiene reglas de precategorización asociadas.' %(instance.descripcion, ajuste_bottom.valor), status=status.HTTP_403_FORBIDDEN)
		elif Ajuste.objects.count() == 3 and ReglaDeAjuste.objects.filter(resultado=Ajuste.objects.get(valor=0)).exists():
			return Response(u'Imposible eliminar la categoría "%s" porque borraría el ajuste de valor 0, el cual tiene reglas de ajuste asociadas.' %(instance.descripcion), status=status.HTTP_403_FORBIDDEN)
		else:
			self.perform_destroy(instance)
			return Response(status=status.HTTP_204_NO_CONTENT)

	def perform_create(self, serializer):
		serializer.save()
		cantAjustesCreados = Ajuste.crearAjustes(self, calcAjustesResultantes(Categoria.objects.count()))
	
	def perform_destroy(self, instance):
		instance.delete()
		cantAjustesBorrados = Ajuste.borrarAjustes(self, calcAjustesResultantes(Categoria.objects.count()))


class CategoriaUpdateAPIView(UpdateAPIView):
	permission_classes = [IsAuthenticated]
	queryset = Categoria.objects.all()
	serializer_class = UpdateCategoriaSerializer

class FactorDeAjusteViewSet(ModelViewSet):
	permission_classes = [IsAuthenticated]
	queryset = FactorDeAjuste.objects.all()
	serializer_class = FactorDeAjusteSerializer

	def destroy(self, request, *args, **kwargs):
		# No elimina factores de ajuste con valores de ajuste que tengan reglas de ajuste asociadas
		instance = self.get_object()
		if ValorDeFactorDeAjuste.objects.filter(factorDeAjuste=instance).exists():
			tieneReglas = False
			valores = ValorDeFactorDeAjuste.objects.filter(factorDeAjuste=instance)
			for valor in valores:
				if ReglaDeAjuste.objects.filter(condicion=valor):
					tieneReglas = True
			if tieneReglas:
				return Response(u'Imposible eliminar el factor de ajuste "%s" porque sus valores tienen reglas asociadas.' %(instance.descripcion), status=status.HTTP_403_FORBIDDEN)
			else:
				cant = valores.count()
				map(lambda val: val.delete(), valores)
				descripcion = instance.descripcion
				instance.delete()
				return Response(status=status.HTTP_204_NO_CONTENT)
		else:
			self.perform_destroy(instance)
			return Response(status=status.HTTP_204_NO_CONTENT)

class FactorDeAjusteUpdateAPIView(UpdateAPIView):
	permission_classes = [IsAuthenticated]
	queryset = FactorDeAjuste.objects.all()
	serializer_class = UpdateFactorDeAjusteSerializer


class ValorDeFactorDeAjusteViewSet(ModelViewSet):
	permission_classes = [IsAuthenticated]
	queryset = ValorDeFactorDeAjuste.objects.all()
	serializer_class = ValorDeFactorDeAjusteSerializer

	def destroy(self, request, *args, **kwargs):
		# No elimina VDFDA con reglas de ajuste asociadas
		instance = self.get_object()
		if ReglaDeAjuste.objects.filter(condicion=instance).exists():
			return Response(u'Imposible eliminar el valor de factor de ajuste "%s" porque tiene reglas de ajuste asociadas.' %(instance.descripcion), status=status.HTTP_403_FORBIDDEN)
		else:
			self.perform_destroy(instance)
			return Response(status=status.HTTP_204_NO_CONTENT)

class ValorDeFactorDeAjusteUpdateAPIView(UpdateAPIView):
	permission_classes = [IsAuthenticated]
	queryset = ValorDeFactorDeAjuste.objects.all()
	serializer_class = UpdateValorDeFactorDeAjusteSerializer


class FactorDePreCategorizacionViewSet(ModelViewSet):
	permission_classes = [IsAuthenticated]
	queryset = FactorDePreCategorizacion.objects.all()
	serializer_class = FactorDePreCategorizacionSerializer

	def destroy(self, request, *args, **kwargs):
		# No elimina factores de precategorización con valores de precategorización  que tengas reglas de precategorización asociadas
		instance = self.get_object()
		if ValorDeFactorDePreCategorizacion.objects.filter(factorDePreCategorizacion=instance).exists():
			tieneReglas = False
			valores = ValorDeFactorDePreCategorizacion.objects.filter(factorDePreCategorizacion=instance)
			for valor in valores:
				if ReglaDePreCategorizacion.objects.filter(condicion=valor):
					tieneReglas = True
			if tieneReglas:
				return Response(u'Imposible eliminar el factor de precategorización "%s" porque sus valores tienen reglas asociadas.' %(instance.descripcion), status=status.HTTP_403_FORBIDDEN)
			else:
				cant = valores.count()
				map(lambda val: val.delete(), valores)
				descripcion = instance.descripcion
				instance.delete()
				return Response(status=status.HTTP_204_NO_CONTENT)
		else:
			self.perform_destroy(instance)
			return Response(status=status.HTTP_204_NO_CONTENT)


class FactorDePreCategorizacionUpdateAPIView(UpdateAPIView):
	permission_classes = [IsAuthenticated]
	queryset = FactorDePreCategorizacion.objects.all()
	serializer_class = UpdateFactorDePreCategorizacionSerializer


class ValorDeFactorDePreCategorizacionViewSet(ModelViewSet):
	permission_classes = [IsAuthenticated]
	queryset = ValorDeFactorDePreCategorizacion.objects.all()
	serializer_class = ValorDeFactorDePreCategorizacionSerializer

	def destroy(self, request, *args, **kwargs):
		# No elimina VDFDPC con reglas de precategorización asociadas
		instance = self.get_object()
		if ReglaDePreCategorizacion.objects.filter(condicion=instance).exists():
			return Response(u'Imposible eliminar el valor de factor de precategorización "%s" porque tiene reglas de precategorización asociadas.' %(instance.descripcion), status=status.HTTP_403_FORBIDDEN)
		else:
			self.perform_destroy(instance)
			return Response(status=status.HTTP_204_NO_CONTENT)


class ValorDeFactorDePreCategorizacionUpdateAPIView(UpdateAPIView):
	permission_classes = [IsAuthenticated]
	queryset = ValorDeFactorDePreCategorizacion.objects.all()
	serializer_class = UpdateValorDeFactorDePreCategorizacionSerializer


class ReglaDeAjusteViewSet(ModelViewSet):
	permission_classes = [IsAuthenticated]
	queryset = ReglaDeAjuste.objects.all()
	serializer_class = ReglaDeAjusteSerializer


class ReglaDeAjusteUpdateAPIView(UpdateAPIView):
	permission_classes = [IsAuthenticated]
	queryset = ReglaDeAjuste.objects.all()
	serializer_class = UpdateReglaDeAjusteSerializer


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
		data = parseData(serializer.data, 'factorDeAjuste_descripcion')
		return Response(data)


class MotivosPCAPIView(ListAPIView):
	permission_classes = [AllowAny]
	queryset = ValorDeFactorDePreCategorizacion.objects.all()
	serializer_class = ValorDeFactorDePreCategorizacionSerializer

	def list(self, request):
		queryset = self.get_queryset()
		serializer = ValorDeFactorDePreCategorizacionSerializer(queryset, many=True)
		data = parseData(serializer.data, 'factorDePreCategorizacion_descripcion')
		return Response(data)