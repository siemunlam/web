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

# API QUE RETORNA LOS DATOS PARA EL GRAFICO DE TORTA
# CON LOS TIPOS DE AUXILIOS (SEGUN LA CATEGORIA)
class Cat_Aux(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        # ESTOS DATOS ESTAN HARDCODEADOS POR AHORA
        # UNA VEZ QUE TENGAMOS EL MODELO TERMINADO HAY QUE LEVANTAR LA INFO DE AHI
        labels = ["Rojo", "Amarillo", "Verde"]
        default_items = [75, 26, 7]
        data = {
                "labels": labels,
                "default": default_items,
        }
        return Response(data)

# API QUE RETORNA LOS DATOS PARA EL GRAFICO DE BARRA
# CON LOS ORIGENES DE LAS SOLICITUDES
class Sol_Aux(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        # ESTOS DATOS ESTAN HARDCODEADOS POR AHORA
        # UNA VEZ QUE TENGAMOS EL MODELO TERMINADO HAY QUE LEVANTAR LA INFO DE AHI
        labels = ["Telefónico", "Mobile", "WhatsApp"]
        default_items = [235, 128, 14]
        data = {
                "labels": labels,
                "default": default_items,
        }
        return Response(data)

# API QUE RETORNA LOS DATOS PARA EL GRAFICO DE LINEA
# CON LA CANTIDAD DE SOLICITUDES POR DIA
class Q_Aux_x_dia(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        # ESTOS DATOS ESTAN HARDCODEADOS POR AHORA
        # UNA VEZ QUE TENGAMOS EL MODELO TERMINADO HAY QUE LEVANTAR LA INFO DE AHI
        labels = ["01/06/17", "02/06/17", "03/06/17", "04/06/17", "05/06/17", "06/06/17", "07/06/17", "08/06/17", "09/06/17", "10/06/17", "11/06/17", "12/06/17", "13/06/17", "14/06/17", "15/06/17", "16/06/17", "17/06/17", "18/06/17", "19/06/17", "20/06/17", "21/06/17", "22/06/17", "23/06/17", "24/06/17", "25/06/17", "26/06/17", "27/06/17", "28/06/17", "29/06/17", "30/06/17", "01/07/17", "02/07/17", "03/07/17", "04/07/17", "05/07/17", "06/07/17", "07/07/17", "08/07/17", "09/07/17", "10/07/17", "11/07/17", "12/07/17", "13/07/17", "14/07/17", "15/07/17", "16/07/17", "17/07/17", "18/07/17", "19/07/17", "20/07/17", "21/07/17", "22/07/17", "23/07/17", "24/07/17", "25/07/17", "26/07/17"]
        default_items = [168, 139, 133, 148, 166, 137, 127, 175, 273, 317, 179, 241, 193, 214, 250, 370, 379, 360, 246, 339, 224, 393, 180, 259, 251, 309, 343, 438, 284, 316, 251, 397, 428, 259, 382, 368, 462, 340, 464, 534, 446, 507, 396, 392, 501, 566, 342, 399, 394, 417, 554, 517, 516, 550, 336, 398]
        data = {
                "labels": labels,
                "default": default_items,
        }
        return Response(data)