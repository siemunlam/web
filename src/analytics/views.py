# -*- coding: utf-8 -*-
from rest_framework import permissions, viewsets
from django.views.generic import TemplateView

class AnalyticsView(TemplateView):
	template_name = 'analytics.html'

