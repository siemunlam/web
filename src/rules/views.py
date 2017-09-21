# -*- coding: utf-8 -*-
import datetime, requests
# encoding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')

from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from accounts.helper_func import es_directivo
from .extra_func import (MAX_REGLAS_CAT, calcAjustesResultantes,
						 escribirReglasDeCategorizacion)
from .forms import (CategoriaForm, FDAForm, FDPCForm, RDAForm, RDPCForm,
					VDFDAForm, VDFDPCForm)
from .models import (Ajuste, Categoria, FactorDeAjuste,
					 FactorDePreCategorizacion, ReglaDeAjuste,
					 ReglaDePreCategorizacion, ValorDeFactorDeAjuste,
					 ValorDeFactorDePreCategorizacion)


# Create your views here.
@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(es_directivo, redirect_field_name=reverse_lazy('home')), name='dispatch')
class RulesView(TemplateView):
	template_name = 'home.html'

	def get_context_data(self, **kwargs):
		context = super(RulesView, self).get_context_data(**kwargs)
		context['categorias'] = Categoria.objects.all().values('id', 'descripcion', 'prioridad', 'color')
		context['ajustes'] = Ajuste.objects.all().values('id', 'valor')
		context['fdas'] = FactorDeAjuste.objects.all().values('id', 'descripcion')
		context['fdpcs'] = FactorDePreCategorizacion.objects.all().values('id', 'descripcion')
		context['vdfdas'] = ValorDeFactorDeAjuste.objects.all().only('id', 'descripcion', 'factorDeAjuste')
		context['vdfdpcs'] = ValorDeFactorDePreCategorizacion.objects.all().only('id', 'descripcion', 'factorDePreCategorizacion')
		context['rdas'] = ReglaDeAjuste.objects.all().only('id', 'condicion', 'resultado', 'prioridad')
		context['rdpcs'] = ReglaDePreCategorizacion.objects.all().only('id', 'condicion', 'resultado', 'prioridad')
		return context
	
	def post(self, request, *args, **kwargs):
		if 'drools' in request.POST:
			rulesFile = 'package com.siem.unlam;\n'
			rulesFile += 'import com.siem.unlam.Persona;\n\n'
			rulesFile += 'import java.util.ArrayList;\n\n'
			
			rulesFile += ReglaDePreCategorizacion.escribirReglas(0)
			rulesFile += ReglaDeAjuste.escribirReglas(MAX_REGLAS_CAT * Categoria.objects.all().count() + 1)
			rulesFile += escribirReglasDeCategorizacion(Categoria.objects.all(), Ajuste.objects.all())

			url = 'http://ec2-18-231-57-236.sa-east-1.compute.amazonaws.com:8085/serviciosSoporte/actualizarReglas/'
			try:
				response = requests.post(url, data='inputjson='+rulesFile, timeout=5)
				result = None
				if response.status_code == requests.codes.ok:
					result = response.text
					print(result)
					messages.success(request, u'Se ha modificado el archivo de reglas en el servidor')
				else:
					response.raise_for_status()
			except Exception as e:
				messages.error(request, u'No fue posible enviar el nuevo archivo de reglas al servidor. Error: %s' %e, extra_tags='danger')
			return HttpResponseRedirect(reverse_lazy('rules'))
			"""response = HttpResponse(rulesFile, content_type='text/plain; charset=utf8')
			response['Content-Disposition'] = u'attachment; filename="Rules.drl"'
			return response"""


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(es_directivo, redirect_field_name=reverse_lazy('home')), name='dispatch')
class AyudaView(TemplateView):
	template_name = 'ayuda.html'


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(es_directivo, redirect_field_name=reverse_lazy('home')), name='dispatch')
class CategoryCreateView(SuccessMessageMixin, CreateView):
	model = Categoria
	form_class = CategoriaForm
	template_name = 'category.html'
	success_message = u'Categoría "%(descripcion)s" creada'
	success_url = reverse_lazy('rules')

	def get_context_data(self, **kwargs):
		context = super(CategoryCreateView, self).get_context_data(**kwargs)
		context['form_title'] = u'Nueva categoría'
		context['btn_confirm_lbl'] = 'Crear'
		context['cancel_url'] = reverse_lazy('rules')
		return context
	
	def form_valid(self, form):
		form.instance.save()
		cantAjustesCreados = Ajuste.crearAjustes(self, calcAjustesResultantes(Categoria.objects.count()))
		if cantAjustesCreados > 0:
			messages.info(self.request, u'Fueron creados %s ajustes' %cantAjustesCreados)
		return super(CategoryCreateView, self).form_valid(form)


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(es_directivo, redirect_field_name=reverse_lazy('home')), name='dispatch')
class CategoryUpdateView(SuccessMessageMixin, UpdateView):
	model = Categoria
	form_class = CategoriaForm
	template_name = 'category.html'
	success_message = u'Categoría "%(descripcion)s" modificada'
	success_url = reverse_lazy('rules')

	def get_context_data(self, **kwargs):
		context = super(CategoryUpdateView, self).get_context_data(**kwargs)
		context['form_title'] = u'Modificar categoría'
		context['btn_confirm_lbl'] = 'Modificar'
		context['cancel_url'] = reverse_lazy('rules')
		return context


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(es_directivo, redirect_field_name=reverse_lazy('home')), name='dispatch')
class CategoryDeleteView(DeleteView):
	model = Categoria
	template_name = 'confirmDeletion.html'
	success_url = reverse_lazy('rules')
	context_object_name = 'instance'

	def get_context_data(self, **kwargs):
		context = super(CategoryDeleteView, self).get_context_data(**kwargs)
		context['form_title'] = u'Anular categoría'
		context['btn_confirm_lbl'] = 'Anular'
		context['cancel_url'] = reverse_lazy('rules')
		return context

	def delete(self, request, *args, **kwargs):
		# No elimina categorías con reglas de precategorización asociadas
		# o categorías que provocarían la eliminación de ajustes con reglas de ajuste asociadas
		self.object = self.get_object()
		ajuste_top = Ajuste.objects.first()
		ajuste_bottom = Ajuste.objects.last()
		if ReglaDePreCategorizacion.objects.filter(resultado=self.object).exists():
			messages.error(request, u'Imposible eliminar la categoría "%s" porque tiene reglas de pre-categorización asociadas.' %(self.object.descripcion), extra_tags='danger')
		elif ReglaDeAjuste.objects.filter(resultado=ajuste_top).exists():
			messages.error(request, u'Imposible eliminar la categoría "%s" porque borraría el ajuste de valor %d, el cual tiene reglas de pre-categorización asociadas.' %(self.object.descripcion, ajuste_top.valor),extra_tags='danger')
		elif ReglaDeAjuste.objects.filter(resultado=Ajuste.objects.last()).exists():
			messages.error(request, u'Imposible eliminar la categoría "%s" porque borraría el ajuste de valor %d, el cual tiene reglas de pre-categorización asociadas.' %(self.object.descripcion, ajuste_bottom.valor),extra_tags='danger')
		elif Ajuste.objects.count() == 3 and ReglaDeAjuste.objects.filter(resultado=Ajuste.objects.get(valor=0)).exists():
			messages.error(request, u'Imposible eliminar la categoría "%s" porque borraría el ajuste de valor 0, el cual tiene reglas de ajuste asociadas.' %(self.object.descripcion), extra_tags='danger')
		else:
			descripcion = self.object.descripcion
			self.object.delete()
			cantAjustesBorrados = Ajuste.borrarAjustes(self, calcAjustesResultantes(Categoria.objects.count()))
			messages.success(request, u'Categoría "%s" eliminada' %descripcion)
			print("cant de ajustes borrados: " + str(cantAjustesBorrados))
			if cantAjustesBorrados > 0:
				messages.info(self.request, u'Fueron borrados %s ajustes' %cantAjustesBorrados)
		return HttpResponseRedirect(self.get_success_url())


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(es_directivo, redirect_field_name=reverse_lazy('home')), name='dispatch')
class FDACreateView(SuccessMessageMixin, CreateView):
	model = FactorDeAjuste
	form_class = FDAForm
	template_name = 'fda.html'
	success_message = u'Factor de ajuste "%(descripcion)s" creado'
	success_url = reverse_lazy('rules')

	def get_context_data(self, **kwargs):
		context = super(FDACreateView, self).get_context_data(**kwargs)
		context['form_title'] = u'Nuevo factor de ajuste'
		context['btn_confirm_lbl'] = 'Crear'
		context['cancel_url'] = reverse_lazy('rules')
		return context


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(es_directivo, redirect_field_name=reverse_lazy('home')), name='dispatch')
class FDAUpdateView(SuccessMessageMixin, UpdateView):
	model = FactorDeAjuste
	form_class = FDAForm
	template_name = 'fda.html'
	success_message = u'Factor de ajuste "%(descripcion)s" modificado'
	success_url = reverse_lazy('rules')

	def get_context_data(self, **kwargs):
		context = super(FDAUpdateView, self).get_context_data(**kwargs)
		context['form_title'] = u'Modificar factor de ajuste'
		context['btn_confirm_lbl'] = 'Modificar'
		context['cancel_url'] = reverse_lazy('rules')
		return context


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(es_directivo, redirect_field_name=reverse_lazy('home')), name='dispatch')
class FDADeleteView(DeleteView):
	model = FactorDeAjuste
	template_name = 'confirmDeletion.html'
	success_url = reverse_lazy('rules')
	context_object_name = 'instance'

	def get_context_data(self, **kwargs):
		context = super(FDADeleteView, self).get_context_data(**kwargs)
		context['form_title'] = u'Anular factor de ajuste'
		context['btn_confirm_lbl'] = 'Anular'
		context['cancel_url'] = reverse_lazy('rules')
		return context

	def delete(self, request, *args, **kwargs):
		# No elimina factores de ajuste con valores de ajuste que tengan reglas de ajuste asociadas
		self.object = self.get_object()
		if ValorDeFactorDeAjuste.objects.filter(factorDeAjuste=self.object).exists():
			tieneReglas = False
			valores = ValorDeFactorDeAjuste.objects.filter(factorDeAjuste=self.object)
			for valor in valores:
				if ReglaDeAjuste.objects.filter(condicion=valor):
					tieneReglas = True
			if tieneReglas:
				messages.error(request, u'Imposible eliminar el factor de ajuste "%s" porque sus valores tienen reglas asociadas.' %(self.object.descripcion), extra_tags='danger')
			else:
				cant = valores.count()
				map(lambda val: val.delete(), valores)
				descripcion = self.object.descripcion
				self.object.delete()
				messages.success(request, u'Factor de ajuste "%s" eliminado' %descripcion)
				messages.info(request, u'Los %d valores del factor de ajuste %s también fueron eliminados' %(cant, descripcion))
		else:
			descripcion = self.object.descripcion
			self.object.delete()
			messages.success(request, u'Factor de ajuste "%s" eliminado' %descripcion)
		return HttpResponseRedirect(self.get_success_url())


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(es_directivo, redirect_field_name=reverse_lazy('home')), name='dispatch')
class FDPCCreateView(SuccessMessageMixin, CreateView):
	model = FactorDePreCategorizacion
	form_class = FDPCForm
	template_name = 'fdpc.html'
	success_message = u'Factor de pre categorización "%(descripcion)s" creado'
	success_url = reverse_lazy('rules')

	def get_context_data(self, **kwargs):
		context = super(FDPCCreateView, self).get_context_data(**kwargs)
		context['form_title'] = u'Nuevo factor de pre categorización'
		context['btn_confirm_lbl'] = 'Crear'
		context['cancel_url'] = reverse_lazy('rules')
		return context


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(es_directivo, redirect_field_name=reverse_lazy('home')), name='dispatch')
class FDPCUpdateView(SuccessMessageMixin, UpdateView):
	model = FactorDePreCategorizacion
	form_class = FDPCForm
	template_name = 'fdpc.html'
	success_message = u'Factor de pre categorización "%(descripcion)s" modificado'
	success_url = reverse_lazy('rules')

	def get_context_data(self, **kwargs):
		context = super(FDPCUpdateView, self).get_context_data(**kwargs)
		context['form_title'] = u'Modificar factor de pre categorización'
		context['btn_confirm_lbl'] = 'Modificar'
		context['cancel_url'] = reverse_lazy('rules')
		return context


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(es_directivo, redirect_field_name=reverse_lazy('home')), name='dispatch')
class FDPCDeleteView(DeleteView):
	model = FactorDePreCategorizacion
	template_name = 'confirmDeletion.html'
	success_url = reverse_lazy('rules')
	context_object_name = 'instance'

	def get_context_data(self, **kwargs):
		context = super(FDPCDeleteView, self).get_context_data(**kwargs)
		context['form_title'] = u'Anular factor de pre categorización'
		context['btn_confirm_lbl'] = 'Anular'
		context['cancel_url'] = reverse_lazy('rules')
		return context

	def delete(self, request, *args, **kwargs):
		# No elimina factores de precategorización con valores de pre categorización  que tengas reglas de pre categorización asociadas
		self.object = self.get_object()
		if ValorDeFactorDePreCategorizacion.objects.filter(factorDePreCategorizacion=self.object).exists():
			tieneReglas = False
			valores = ValorDeFactorDePreCategorizacion.objects.filter(factorDePreCategorizacion=self.object)
			for valor in valores:
				if ReglaDePreCategorizacion.objects.filter(condicion=valor):
					tieneReglas = True
			if tieneReglas:
				messages.error(request, u'Imposible eliminar el factor de pre-categorización "%s" porque sus valores tienen reglas asociadas.' %(self.object.descripcion), extra_tags='danger')
			else:
				cant = valores.count()
				map(lambda val: val.delete(), valores)
				descripcion = self.object.descripcion
				self.object.delete()
				messages.success(request, u'Factor de pre categorización "%s" eliminado' %descripcion)
				messages.info(request, u'Los %d valores del factor de pre categorización %s también fueron eliminados' %(cant, descripcion))
		else:
			descripcion = self.object.descripcion
			self.object.delete()
			messages.success(request, u'Factor de pre categorización "%s" eliminado' %descripcion)
		return HttpResponseRedirect(self.get_success_url())


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(es_directivo, redirect_field_name=reverse_lazy('home')), name='dispatch')
class VDFDACreateView(SuccessMessageMixin, CreateView):
	model = ValorDeFactorDeAjuste
	form_class = VDFDAForm
	template_name = 'vdfda.html'
	success_message = u'Valor de factor de ajuste "%(descripcion)s" creado'
	success_url = reverse_lazy('rules')

	def get_context_data(self, **kwargs):
		context = super(VDFDACreateView, self).get_context_data(**kwargs)
		context['form_title'] = u'Nuevo valor de factor de ajuste'
		context['btn_confirm_lbl'] = 'Crear'
		context['cancel_url'] = reverse_lazy('rules')
		return context


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(es_directivo, redirect_field_name=reverse_lazy('home')), name='dispatch')
class VDFDAUpdateView(SuccessMessageMixin, UpdateView):
	model = ValorDeFactorDeAjuste
	form_class = VDFDAForm
	template_name = 'vdfda.html'
	success_message = u'Valor de factor de ajuste "%(descripcion)s" modificado'
	success_url = reverse_lazy('rules')

	def get_context_data(self, **kwargs):
		context = super(VDFDAUpdateView, self).get_context_data(**kwargs)
		context['form_title'] = u'Modificar valor de factor de ajuste'
		context['btn_confirm_lbl'] = 'Modificar'
		context['cancel_url'] = reverse_lazy('rules')
		return context


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(es_directivo, redirect_field_name=reverse_lazy('home')), name='dispatch')
class VDFDADeleteView(DeleteView):
	model = ValorDeFactorDeAjuste
	template_name = 'confirmDeletion.html'
	success_url = reverse_lazy('rules')
	context_object_name = 'instance'

	def get_context_data(self, **kwargs):
		context = super(VDFDADeleteView, self).get_context_data(**kwargs)
		context['form_title'] = u'Anular valor de factor de ajuste'
		context['btn_confirm_lbl'] = 'Anular'
		context['cancel_url'] = reverse_lazy('rules')
		return context

	def delete(self, request, *args, **kwargs):
		# No elimina VDFDA con reglas de ajuste asociadas
		self.object = self.get_object()
		if ReglaDeAjuste.objects.filter(condicion=self.object).exists():
			messages.error(request, u'Imposible eliminar el valor de factor de ajuste "%d" porque tiene reglas de ajuste asociadas.' %(self.object.id), extra_tags='danger')
		else:
			descripcion = self.object.descripcion
			self.object.delete()
			messages.success(request, u'Valor de factor de ajuste "%s" eliminado' %descripcion)
		return HttpResponseRedirect(self.get_success_url())


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(es_directivo, redirect_field_name=reverse_lazy('home')), name='dispatch')
class VDFDPCCreateView(SuccessMessageMixin, CreateView):
	model = ValorDeFactorDePreCategorizacion
	form_class = VDFDPCForm
	template_name = 'vdfdpc.html'
	success_message = u'Valor de factor de pre-categorización "%(descripcion)s" creado'
	success_url = reverse_lazy('rules')

	def get_context_data(self, **kwargs):
		context = super(VDFDPCCreateView, self).get_context_data(**kwargs)
		context['form_title'] = u'Nuevo valor de factor de pre-categorización'
		context['btn_confirm_lbl'] = 'Crear'
		context['cancel_url'] = reverse_lazy('rules')
		return context


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(es_directivo, redirect_field_name=reverse_lazy('home')), name='dispatch')
class VDFDPCUpdateView(SuccessMessageMixin, UpdateView):
	model = ValorDeFactorDePreCategorizacion
	form_class = VDFDPCForm
	template_name = 'vdfdpc.html'
	success_message = u'Valor de factor de pre-categorización "%(descripcion)s" modificado'
	success_url = reverse_lazy('rules')

	def get_context_data(self, **kwargs):
		context = super(VDFDPCUpdateView, self).get_context_data(**kwargs)
		context['form_title'] = u'Modificar valor de factor de pre-categorización'
		context['btn_confirm_lbl'] = 'Modificar'
		context['cancel_url'] = reverse_lazy('rules')
		return context


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(es_directivo, redirect_field_name=reverse_lazy('home')), name='dispatch')
class VDFDPCDeleteView(DeleteView):
	model = ValorDeFactorDePreCategorizacion
	template_name = 'confirmDeletion.html'
	success_url = reverse_lazy('rules')
	context_object_name = 'instance'

	def get_context_data(self, **kwargs):
		context = super(VDFDPCDeleteView, self).get_context_data(**kwargs)
		context['form_title'] = u'Anular valor de factor de pre-categorización'
		context['btn_confirm_lbl'] = 'Anular'
		context['cancel_url'] = reverse_lazy('rules')
		return context

	def delete(self, request, *args, **kwargs):
		# No elimina VDFDPC con reglas de pre-categorización asociadas
		self.object = self.get_object()
		if ReglaDePreCategorizacion.objects.filter(condicion=self.object).exists():
			messages.error(request, u'Imposible eliminar el valor de factor de pre-categorización "%s" porque tiene reglas de pre-categorización asociadas.' %(self.object.descripcion), extra_tags='danger')
		else:
			descripcion = self.object.descripcion
			self.object.delete()
			messages.success(request, u'Valor de factor de pre-categorización "%s" eliminado' %descripcion)
		return HttpResponseRedirect(self.get_success_url())


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(es_directivo, redirect_field_name=reverse_lazy('home')), name='dispatch')
class RDACreateView(SuccessMessageMixin, CreateView):
	model = ReglaDeAjuste
	form_class = RDAForm
	template_name = 'rda.html'
	success_message = u'Regla de ajuste "%(resultado)s" creada'
	success_url = reverse_lazy('rules')

	def get_context_data(self, **kwargs):
		context = super(RDACreateView, self).get_context_data(**kwargs)
		context['form_title'] = u'Nueva regla de ajuste'
		context['btn_confirm_lbl'] = 'Crear'
		context['cancel_url'] = reverse_lazy('rules')
		return context


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(es_directivo, redirect_field_name=reverse_lazy('home')), name='dispatch')
class RDAUpdateView(SuccessMessageMixin, UpdateView):
	model = ReglaDeAjuste
	form_class = RDAForm
	template_name = 'rda.html'
	success_message = u'Regla de ajuste "%(resultado)s" modificada'
	success_url = reverse_lazy('rules')

	def get_context_data(self, **kwargs):
		context = super(RDAUpdateView, self).get_context_data(**kwargs)
		context['form_title'] = u'Modificar regla de ajuste'
		context['btn_confirm_lbl'] = 'Modificar'
		context['cancel_url'] = reverse_lazy('rules')
		return context


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(es_directivo, redirect_field_name=reverse_lazy('home')), name='dispatch')
class RDADeleteView(DeleteView):
	model = ReglaDeAjuste
	template_name = 'confirmDeletion.html'
	success_url = reverse_lazy('rules')
	context_object_name = 'instance'

	def get_context_data(self, **kwargs):
		context = super(RDADeleteView, self).get_context_data(**kwargs)
		context['form_title'] = u'Anular regla de ajuste'
		context['btn_confirm_lbl'] = 'Anular'
		context['cancel_url'] = reverse_lazy('rules')
		return context

	def delete(self, request, *args, **kwargs):
		self.object = self.get_object()
		id = self.object.id
		self.object.delete()
		messages.success(request, u'Regla de ajuste "%s" eliminada' %id)
		return HttpResponseRedirect(self.get_success_url())


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(es_directivo, redirect_field_name=reverse_lazy('home')), name='dispatch')
class RDPCCreateView(SuccessMessageMixin, CreateView):
	model = ReglaDePreCategorizacion
	form_class = RDPCForm
	template_name = 'rdpc.html'
	success_message = u'Regla de pre-categorización "%(resultado)s" creada'
	success_url = reverse_lazy('rules')

	def get_context_data(self, **kwargs):
		context = super(RDPCCreateView, self).get_context_data(**kwargs)
		context['form_title'] = u'Nueva regla de pre-categorización'
		context['btn_confirm_lbl'] = 'Crear'
		context['cancel_url'] = reverse_lazy('rules')
		return context


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(es_directivo, redirect_field_name=reverse_lazy('home')), name='dispatch')
class RDPCUpdateView(SuccessMessageMixin, UpdateView):
	model = ReglaDePreCategorizacion
	form_class = RDPCForm
	template_name = 'rdpc.html'
	success_message = u'Regla de pre-categorización "%(resultado)s" modificada'
	success_url = reverse_lazy('rules')

	def get_context_data(self, **kwargs):
		context = super(RDPCUpdateView, self).get_context_data(**kwargs)
		context['form_title'] = u'Modificar regla de pre-categorización'
		context['btn_confirm_lbl'] = 'Modificar'
		context['cancel_url'] = reverse_lazy('rules')
		return context


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(es_directivo, redirect_field_name=reverse_lazy('home')), name='dispatch')
class RDPCDeleteView(DeleteView):
	model = ReglaDePreCategorizacion
	template_name = 'confirmDeletion.html'
	success_url = reverse_lazy('rules')
	context_object_name = 'instance'

	def get_context_data(self, **kwargs):
		context = super(RDPCDeleteView, self).get_context_data(**kwargs)
		context['form_title'] = u'Anular regla de pre-categorización'
		context['btn_confirm_lbl'] = 'Anular'
		context['cancel_url'] = reverse_lazy('rules')
		return context

	def delete(self, request, *args, **kwargs):
		self.object = self.get_object()
		id = self.object.id
		self.object.delete()
		messages.success(request, u'Regla de pre-categorización "%s" eliminada' %id)
		return HttpResponseRedirect(self.get_success_url())