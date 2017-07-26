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

