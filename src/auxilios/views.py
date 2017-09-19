# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView


from accounts.helper_func import es_supervisor, es_directivo
from .forms import SolicitudDeAuxilioForm
from .api.serializers import AuxiliosUpdateSerializer


# Create your views here.
@method_decorator(login_required, name='dispatch')
class HomeView(TemplateView):
	template_name = 'welcome.html'


@method_decorator(login_required, name='dispatch')
class AsignacionListView(TemplateView):
	template_name = 'asignaciones-list.html'


@method_decorator(login_required, name='dispatch')
class AuxiliosListView(TemplateView):
	template_name = 'auxilios-list.html'

	def get_context_data(self, **kwargs):
		context = super(AuxiliosListView, self).get_context_data(**kwargs)
		context['form'] = SolicitudDeAuxilioForm
		context['auxilios_api'] = reverse_lazy('api:auxilios-list')
		context['solicitudes_api'] = reverse_lazy('api:solicitudes-list')
		context['vdfda_api'] = reverse_lazy('rules-api:motivos_ajuste')
		context['vdfdpc_api'] = reverse_lazy('rules-api:motivos_pc')
		context['update_serializer'] = AuxiliosUpdateSerializer
		return context


@method_decorator(login_required, name='dispatch')
class AuxiliosMovilesMapaView(TemplateView):
    def get(self, request, *args, **kwargs):
        return render(request, 'auxilios-moviles-mapa.html')


# @method_decorator(login_required, name='dispatch')
# class MovilViewSet(viewsets.ModelViewSet):
# 	queryset = Movil.objects.all()
# 	serializer_class = MovilSerializer
# 	permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

# 	def perform_create(self, serializer):
# 		serializer.save(generador=self.request.user)


#@method_decorator(login_required, name='dispatch')
# class MovilListView(TemplateView):
# 	template_name = 'moviles-list.html'

# 	def get_context_data(self, **kwargs):
# 		context = super(MovilListView, self).get_context_data(**kwargs)
# 		context['serializer'] = MovilSerializer
# 		return context