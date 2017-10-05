# -*- coding: utf-8 -*-

from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import View

from rest_framework.views import APIView
from rest_framework.response import Response

# PAGINA PRINCIPAL DE REPORTES
class AnalyticsView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'analytics_home.html')

# PAGINA DE LOS PRIMEROS REPORTES (AUXILIOS)
class Report_1View(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'report_1.html')

# PAGINA DE LOS PRIMEROS REPORTES (AUXILIOS OCURRENCIA)
class Report_2View(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'report_2.html')

# PAGINA DE LOS PRIMEROS REPORTES (TIEMPOS DE DEMORA Y ATENCION)
class Report_3View(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'report_3.html')

# PAGINA DE LOS PRIMEROS REPORTES (TIEMPOS DE DEMORA Y ATENCION)
class HeatMapView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'heatmap.html')

########
# APIS #
########


# API QUE RETORNA LOS TIEMPOS PROMEDIO DE ESPERA
# Y DE ATENCION POR TIPO DE AUXILIO (CATEGORIA  )
class Tiem_demora_ate(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        # ESTOS DATOS ESTAN HARDCODEADOS POR AHORA
        # UNA VEZ QUE TENGAMOS EL MODELO TERMINADO HAY QUE LEVANTAR LA INFO DE AHI
        labels = ["Rojo", "Amarillo", "Verde"]
        default_items = [15, 24, 38]
        data = {
                "labels": labels,
                "default": default_items,
        }
        return Response(data)

# API QUE RETORNA LOS TIEMPOS PROMEDIO DE ESPERA
# Y DE ATENCION POR TIPO DE AUXILIO (CATEGORIA  )
class Tiem_espera_cola(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        # ESTOS DATOS ESTAN HARDCODEADOS POR AHORA
        # UNA VEZ QUE TENGAMOS EL MODELO TERMINADO HAY QUE LEVANTAR LA INFO DE AHI
        labels = ["Rojo", "Amarillo", "Verde"]
        default_items = [4, 12, 15]
        data = {
                "labels": labels,
                "default": default_items,
        }
        return Response(data)

# API QUE RETORNA LOS DATOS GEOLOCALIZADOS DE LAS SOLICITUDES DE AUXILIOS
class Localizacion_aux(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        # ESTOS DATOS ESTAN HARDCODEADOS POR AHORA
        # UNA VEZ QUE TENGAMOS EL MODELO TERMINADO HAY QUE LEVANTAR LA INFO DE AHI
        
        latitudes_default = [-34.614671, -34.642158, -34.607874]
        
        longitudes_default = [-58.437786, -58.37133, -58.435876]

        data = {
                "logitudes": latitudes_default,
                "latitudes": longitudes_default
        }
        return Response(data)

        