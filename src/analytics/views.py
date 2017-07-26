# -*- coding: utf-8 -*-
from rest_framework import permissions, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from django.views.generic import TemplateView

class AnalyticsView(TemplateView):
	template_name = 'analytics.html'


class Cat_Aux(APIView):
    authentication_classes = []
    permission_clases = []

    def get(self, request, format=None):
        data = {
            "Rojo":124,
            "Naranja":73,
            "Verde":14,
        }
        return Response(data)

