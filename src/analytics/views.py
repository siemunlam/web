from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import View

from rest_framework.views import APIView
from rest_framework.response import Response


class AnalyticsView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'analytics_home.html')

class Report_1View(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'report_1.html')

class Cat_Aux(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        labels = ["Rojo", "Amarillo", "Verde"]
        default_items = [75, 26, 7]
        data = {
                "labels": labels,
                "default": default_items,
        }
        return Response(data)

class Sol_Aux(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        labels = ["Telefónico", "Mobile", "WhatsApp"]
        default_items = [235, 128, 14]
        data = {
                "labels": labels,
                "default": default_items,
        }
        return Response(data)

class Q_Aux_x_dia(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        labels = ["01/06/2017", "02/06/2017", "03/06/2017", "04/06/2017", "05/06/2017", "06/06/2017", "07/06/2017", "08/06/2017", "09/06/2017", "10/06/2017", "11/06/2017", "12/06/2017", "13/06/2017", "14/06/2017", "15/06/2017", "16/06/2017", "17/06/2017", "18/06/2017", "19/06/2017", "20/06/2017", "21/06/2017", "22/06/2017", "23/06/2017", "24/06/2017", "25/06/2017", "26/06/2017", "27/06/2017", "28/06/2017", "29/06/2017", "30/06/2017", "01/07/2017", "02/07/2017", "03/07/2017", "04/07/2017", "05/07/2017", "06/07/2017", "07/07/2017", "08/07/2017", "09/07/2017", "10/07/2017", "11/07/2017", "12/07/2017", "13/07/2017", "14/07/2017", "15/07/2017", "16/07/2017", "17/07/2017", "18/07/2017", "19/07/2017", "20/07/2017", "21/07/2017", "22/07/2017", "23/07/2017", "24/07/2017", "25/07/2017", "26/07/2017"]
        default_items = [168, 139, 133, 148, 166, 137, 127, 175, 273, 317, 179, 241, 193, 214, 250, 370, 379, 360, 246, 339, 224, 393, 180, 259, 251, 309, 343, 438, 284, 316, 251, 397, 428, 259, 382, 368, 462, 340, 464, 534, 446, 507, 396, 392, 501, 566, 342, 399, 394, 417, 554, 517, 516, 550, 336, 398]
        data = {
                "labels": labels,
                "default": default_items,
        }
        return Response(data)