# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.urlresolvers import reverse_lazy
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator

from accounts.helper_func import es_supervisor
from .api.serializers import MedicoCreateSerializer, MedicoUpdateSerializer


# Create your views here.
@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(es_supervisor, redirect_field_name=reverse_lazy('home')), name='dispatch')
class MedicoListView(TemplateView):
	template_name = 'medicos.html'

	def get_context_data(self, **kwargs):
		context = super(MedicoListView, self).get_context_data(**kwargs)
		context['serializer'] = MedicoCreateSerializer
		context['page_size'] = settings.FRONTEND_PAGE_SIZE
		context['update_serializer'] = MedicoUpdateSerializer
		context['apiListURL'] = reverse_lazy('medicos-api:list')
		context['apiRegisterURL'] = reverse_lazy('medicos-api:register')
		return context