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

# PAGINA DE LOS MOTIVOS DE SOLICITUD (AUXILIOS)
class Report_4View(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'report_4.html')

# PAGINA DE LOS PRIMEROS REPORTES (TIEMPOS DE DEMORA Y ATENCION)
class HeatMapView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'heatmap.html')
