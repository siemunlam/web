# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.urlresolvers import reverse_lazy
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator

from .api.serializers import MedicoCreateSerializer


# Create your views here.
def es_medico(user):
    return user.groups.filter(name='medicos').exists()


@method_decorator(user_passes_test(es_medico), name='dispatch')
class MedicoListView(TemplateView):
	template_name = 'medicos.html'

	def get_context_data(self, **kwargs):
		context = super(MedicoListView, self).get_context_data(**kwargs)
		context['serializer'] = MedicoCreateSerializer
		context['apiURL'] = reverse_lazy('medicos-api:list')
		return context