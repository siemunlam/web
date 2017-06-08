# -*- coding: utf-8 -*-
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import Ajuste, Categoria, FactorDeAjuste, FactorDePreCategorizacion, ValorDeFactorDeAjuste, ValorDeFactorDePreCategorizacion, ReglaDeAjuste, ReglaDePreCategorizacion
from .forms import CategoriaForm, FDAForm, FDPCForm, VDFDAForm, VDFDPCForm, RDAForm, RDPCForm
from .extra_func import calcAjustesResultantes, escribirReglasDeCategorizacion, MAX_REGLAS_CAT

import datetime


# Create your views here.
class HomeView(TemplateView):
	template_name = 'home.html'

	def get_context_data(self, **kwargs):
		context = super(HomeView, self).get_context_data(**kwargs)
		context['categorias'] = Categoria.objects.filter(fue_anulado = False).values('id', 'descripcion', 'prioridad', 'color')
		context['ajustes'] = Ajuste.objects.values('id', 'valor')
		context['fdas'] = FactorDeAjuste.objects.filter(fue_anulado = False).values('id', 'descripcion')
		context['fdpcs'] = FactorDePreCategorizacion.objects.filter(fue_anulado = False).values('id', 'descripcion')
		context['vdfdas'] = ValorDeFactorDeAjuste.objects.filter(fue_anulado = False).only('id', 'descripcion', 'factorDeAjuste')
		context['vdfdpcs'] = ValorDeFactorDePreCategorizacion.objects.filter(fue_anulado = False).only('id', 'descripcion', 'factorDePreCategorizacion')
		context['rdas'] = ReglaDeAjuste.objects.filter(fue_anulado = False).only('id', 'condicion', 'resultado', 'prioridad')
		context['rdpcs'] = ReglaDePreCategorizacion.objects.filter(fue_anulado = False).only('id', 'condicion', 'resultado', 'prioridad')
		return context
	
	def post(self, request, *args, **kwargs):
		if 'drools' in request.POST:
			rulesFile = 'package com.siem.unlam;\n'
			rulesFile += 'import com.siem.unlam.Persona;\n\n'
			
			rulesFile += ReglaDePreCategorizacion.escribirReglas(0)
			rulesFile += ReglaDeAjuste.escribirReglas(MAX_REGLAS_CAT * Categoria.objects.filter(fue_anulado=False).count() + 1)
			rulesFile += escribirReglasDeCategorizacion(Categoria.objects.filter(fue_anulado=False), Ajuste.objects.all())

			response = HttpResponse(rulesFile, content_type='text/plain; charset=utf8')
			response['Content-Disposition'] = u'attachment; filename="Rules.drl"'
			return response


class CategoryCreateView(SuccessMessageMixin, CreateView):
	model = Categoria
	form_class = CategoriaForm
	template_name = 'category.html'
	success_message = u'Categoría "%(descripcion)s" creada'
	success_url = reverse_lazy('home')

	def get_context_data(self, **kwargs):
		context = super(CategoryCreateView, self).get_context_data(**kwargs)
		context['form_title'] = u'Nueva categoría'
		context['btn_confirm_lbl'] = 'Crear'
		context['cancel_url'] = reverse_lazy('home')
		return context
	
	def form_valid(self, form):
		form.instance.save()
		print("cant categorias: " + str(Categoria.objects.filter(fue_anulado = False).count()))
		cantAjustesCreados = Ajuste.crearAjustes(self, calcAjustesResultantes(Categoria.objects.filter(fue_anulado = False).count()))
		if cantAjustesCreados > 0:
			messages.info(self.request, u'Fueron creados %s ajustes' %cantAjustesCreados)
		return super(CategoryCreateView, self).form_valid(form)


class CategoryUpdateView(SuccessMessageMixin, UpdateView):
	model = Categoria
	form_class = CategoriaForm
	template_name = 'category.html'
	success_message = u'Categoría "%(descripcion)s" modificada'
	success_url = reverse_lazy('home')

	def get_context_data(self, **kwargs):
		context = super(CategoryUpdateView, self).get_context_data(**kwargs)
		context['form_title'] = u'Modificar categoría'
		context['btn_confirm_lbl'] = 'Modificar'
		context['cancel_url'] = reverse_lazy('home')
		return context


class CategoryDeleteView(DeleteView):
	model = Categoria
	template_name = 'confirmDeletion.html'
	success_url = reverse_lazy('home')
	context_object_name = 'instance'

	def get_context_data(self, **kwargs):
		context = super(CategoryDeleteView, self).get_context_data(**kwargs)
		context['form_title'] = u'Anular categoría'
		context['btn_confirm_lbl'] = 'Anular'
		context['cancel_url'] = reverse_lazy('home')
		return context

	def delete(self, request, *args, **kwargs):
		# No elimina categorías con reglas de precategorización asociadas
		# o categorías que provocarían la eliminación de ajustes con reglas de ajuste asociadas
		self.object = self.get_object()
		self.object.fue_anulado = True
		self.object.save()
		cantAjustesBorrados = Ajuste.borrarAjustes(self, calcAjustesResultantes(Categoria.objects.filter(fue_anulado = False).count()))
		messages.success(request, u'Categoría "%s" anulada' %self.object.descripcion)
		if cantAjustesBorrados > 0:
			messages.info(self.request, u'Fueron borrados %s ajustes' %cantAjustesBorrados)
		return HttpResponseRedirect(self.get_success_url())


class FDACreateView(SuccessMessageMixin, CreateView):
	model = FactorDeAjuste
	form_class = FDAForm
	template_name = 'fda.html'
	success_message = u'Factor de ajuste "%(descripcion)s" creado'
	success_url = reverse_lazy('home')

	def get_context_data(self, **kwargs):
		context = super(FDACreateView, self).get_context_data(**kwargs)
		context['form_title'] = u'Nuevo factor de ajuste'
		context['btn_confirm_lbl'] = 'Crear'
		context['cancel_url'] = reverse_lazy('home')
		return context


class FDAUpdateView(SuccessMessageMixin, UpdateView):
	model = FactorDeAjuste
	form_class = FDAForm
	template_name = 'fda.html'
	success_message = u'Factor de ajuste "%(descripcion)s" modificado'
	success_url = reverse_lazy('home')

	def get_context_data(self, **kwargs):
		context = super(FDAUpdateView, self).get_context_data(**kwargs)
		context['form_title'] = u'Modificar factor de ajuste'
		context['btn_confirm_lbl'] = 'Modificar'
		context['cancel_url'] = reverse_lazy('home')
		return context


class FDADeleteView(DeleteView):
	model = FactorDeAjuste
	template_name = 'confirmDeletion.html'
	success_url = reverse_lazy('home')
	context_object_name = 'instance'

	def get_context_data(self, **kwargs):
		context = super(FDADeleteView, self).get_context_data(**kwargs)
		context['form_title'] = u'Anular factor de ajuste'
		context['btn_confirm_lbl'] = 'Anular'
		context['cancel_url'] = reverse_lazy('home')
		return context

	def delete(self, request, *args, **kwargs):
		# No elimina FDA con VDFDA asociados
		self.object = self.get_object()
		self.object.fue_anulado = True
		self.object.save()
		messages.success(request, u'Factor de ajuste "%s" anulado' %self.object.descripcion)
		return HttpResponseRedirect(self.get_success_url())


class FDPCCreateView(SuccessMessageMixin, CreateView):
	model = FactorDePreCategorizacion
	form_class = FDPCForm
	template_name = 'fdpc.html'
	success_message = u'Factor de pre categorización "%(descripcion)s" creado'
	success_url = reverse_lazy('home')

	def get_context_data(self, **kwargs):
		context = super(FDPCCreateView, self).get_context_data(**kwargs)
		context['form_title'] = u'Nuevo factor de pre categorización'
		context['btn_confirm_lbl'] = 'Crear'
		context['cancel_url'] = reverse_lazy('home')
		return context


class FDPCUpdateView(SuccessMessageMixin, UpdateView):
	model = FactorDePreCategorizacion
	form_class = FDPCForm
	template_name = 'fdpc.html'
	success_message = u'Factor de pre categorización "%(descripcion)s" modificado'
	success_url = reverse_lazy('home')

	def get_context_data(self, **kwargs):
		context = super(FDPCUpdateView, self).get_context_data(**kwargs)
		context['form_title'] = u'Modificar factor de pre categorización'
		context['btn_confirm_lbl'] = 'Modificar'
		context['cancel_url'] = reverse_lazy('home')
		return context


class FDPCDeleteView(DeleteView):
	model = FactorDePreCategorizacion
	template_name = 'confirmDeletion.html'
	success_url = reverse_lazy('home')
	context_object_name = 'instance'

	def get_context_data(self, **kwargs):
		context = super(FDPCDeleteView, self).get_context_data(**kwargs)
		context['form_title'] = u'Anular factor de pre categorización'
		context['btn_confirm_lbl'] = 'Anular'
		context['cancel_url'] = reverse_lazy('home')
		return context

	def delete(self, request, *args, **kwargs):
		# No elimina factores de precategorización con valores de pre categorización asociados
		self.object = self.get_object()
		self.object.fue_anulado = True
		self.object.save()
		messages.success(request, u'Factor de pre categorización "%s" anulado' %self.object.descripcion)
		return HttpResponseRedirect(self.get_success_url())


class VDFDACreateView(SuccessMessageMixin, CreateView):
	model = ValorDeFactorDeAjuste
	form_class = VDFDAForm
	template_name = 'vdfda.html'
	success_message = u'Valor de factor de ajuste "%(descripcion)s" creado'
	success_url = reverse_lazy('home')

	def get_context_data(self, **kwargs):
		context = super(VDFDACreateView, self).get_context_data(**kwargs)
		context['form_title'] = u'Nuevo valor de factor de ajuste'
		context['btn_confirm_lbl'] = 'Crear'
		context['cancel_url'] = reverse_lazy('home')
		return context


class VDFDAUpdateView(SuccessMessageMixin, UpdateView):
	model = ValorDeFactorDeAjuste
	form_class = VDFDAForm
	template_name = 'vdfda.html'
	success_message = u'Valor de factor de ajuste "%(descripcion)s" modificado'
	success_url = reverse_lazy('home')

	def get_context_data(self, **kwargs):
		context = super(VDFDAUpdateView, self).get_context_data(**kwargs)
		context['form_title'] = u'Modificar valor de factor de ajuste'
		context['btn_confirm_lbl'] = 'Modificar'
		context['cancel_url'] = reverse_lazy('home')
		return context


class VDFDADeleteView(DeleteView):
	model = ValorDeFactorDeAjuste
	template_name = 'confirmDeletion.html'
	success_url = reverse_lazy('home')
	context_object_name = 'instance'

	def get_context_data(self, **kwargs):
		context = super(VDFDADeleteView, self).get_context_data(**kwargs)
		context['form_title'] = u'Anular valor de factor de ajuste'
		context['btn_confirm_lbl'] = 'Anular'
		context['cancel_url'] = reverse_lazy('home')
		return context

	def delete(self, request, *args, **kwargs):
		# No elimina VDFDA con reglas de ajuste asociadas
		self.object = self.get_object()
		self.object.fue_anulado = True
		self.object.save()
		messages.success(request, u'Valor de factor de ajuste "%s" anulado' %self.object.descripcion)
		return HttpResponseRedirect(self.get_success_url())


class VDFDPCCreateView(SuccessMessageMixin, CreateView):
	model = ValorDeFactorDePreCategorizacion
	form_class = VDFDPCForm
	template_name = 'vdfdpc.html'
	success_message = u'Valor de factor de pre-categorización "%(descripcion)s" creado'
	success_url = reverse_lazy('home')

	def get_context_data(self, **kwargs):
		context = super(VDFDPCCreateView, self).get_context_data(**kwargs)
		context['form_title'] = u'Nuevo valor de factor de pre-categorización'
		context['btn_confirm_lbl'] = 'Crear'
		context['cancel_url'] = reverse_lazy('home')
		return context


class VDFDPCUpdateView(SuccessMessageMixin, UpdateView):
	model = ValorDeFactorDePreCategorizacion
	form_class = VDFDPCForm
	template_name = 'vdfda.html'
	success_message = u'Valor de factor de pre-categorización "%(descripcion)s" modificado'
	success_url = reverse_lazy('home')

	def get_context_data(self, **kwargs):
		context = super(VDFDPCUpdateView, self).get_context_data(**kwargs)
		context['form_title'] = u'Modificar valor de factor de pre-categorización'
		context['btn_confirm_lbl'] = 'Modificar'
		context['cancel_url'] = reverse_lazy('home')
		return context


class VDFDPCDeleteView(DeleteView):
	model = ValorDeFactorDePreCategorizacion
	template_name = 'confirmDeletion.html'
	success_url = reverse_lazy('home')
	context_object_name = 'instance'

	def get_context_data(self, **kwargs):
		context = super(VDFDPCDeleteView, self).get_context_data(**kwargs)
		context['form_title'] = u'Anular valor de factor de pre-categorización'
		context['btn_confirm_lbl'] = 'Anular'
		context['cancel_url'] = reverse_lazy('home')
		return context

	def delete(self, request, *args, **kwargs):
		# No elimina VDFDPC con reglas de pre-categorización asociadas
		self.object = self.get_object()
		self.object.fue_anulado = True
		self.object.save()
		messages.success(request, u'Valor de factor de pre-categorización "%s" anulado' %self.object.descripcion)
		return HttpResponseRedirect(self.get_success_url())


class RDACreateView(SuccessMessageMixin, CreateView):
	model = ReglaDeAjuste
	form_class = RDAForm
	template_name = 'rda.html'
	success_message = u'Regla de ajuste "%(resultado)s" creada'
	success_url = reverse_lazy('home')

	def get_context_data(self, **kwargs):
		context = super(RDACreateView, self).get_context_data(**kwargs)
		context['form_title'] = u'Nueva regla de ajuste'
		context['btn_confirm_lbl'] = 'Crear'
		context['cancel_url'] = reverse_lazy('home')
		return context


class RDAUpdateView(SuccessMessageMixin, UpdateView):
	model = ReglaDeAjuste
	form_class = RDAForm
	template_name = 'rda.html'
	success_message = u'Regla de ajuste "%(resultado)s" modificada'
	success_url = reverse_lazy('home')

	def get_context_data(self, **kwargs):
		context = super(RDAUpdateView, self).get_context_data(**kwargs)
		context['form_title'] = u'Modificar regla de ajuste'
		context['btn_confirm_lbl'] = 'Modificar'
		context['cancel_url'] = reverse_lazy('home')
		return context


class RDADeleteView(DeleteView):
	model = ReglaDeAjuste
	template_name = 'confirmDeletion.html'
	success_url = reverse_lazy('home')
	context_object_name = 'instance'

	def get_context_data(self, **kwargs):
		context = super(RDADeleteView, self).get_context_data(**kwargs)
		context['form_title'] = u'Anular regla de ajuste'
		context['btn_confirm_lbl'] = 'Anular'
		context['cancel_url'] = reverse_lazy('home')
		return context

	def delete(self, request, *args, **kwargs):
		self.object = self.get_object()
		self.object.fue_anulado = True
		self.object.save()
		messages.success(request, u'Regla de ajuste "%s" anulada' %self.object.id)
		return HttpResponseRedirect(self.get_success_url())


class RDPCCreateView(SuccessMessageMixin, CreateView):
	model = ReglaDePreCategorizacion
	form_class = RDPCForm
	template_name = 'rdpc.html'
	success_message = u'Regla de pre-categorización "%(resultado)s" creada'
	success_url = reverse_lazy('home')

	def get_context_data(self, **kwargs):
		context = super(RDPCCreateView, self).get_context_data(**kwargs)
		context['form_title'] = u'Nueva regla de pre-categorización'
		context['btn_confirm_lbl'] = 'Crear'
		context['cancel_url'] = reverse_lazy('home')
		return context


class RDPCUpdateView(SuccessMessageMixin, UpdateView):
	model = ReglaDePreCategorizacion
	form_class = RDPCForm
	template_name = 'rdpc.html'
	success_message = u'Regla de pre-categorización "%(resultado)s" modificada'
	success_url = reverse_lazy('home')

	def get_context_data(self, **kwargs):
		context = super(RDPCUpdateView, self).get_context_data(**kwargs)
		context['form_title'] = u'Modificar regla de pre-categorización'
		context['btn_confirm_lbl'] = 'Modificar'
		context['cancel_url'] = reverse_lazy('home')
		return context


class RDPCDeleteView(DeleteView):
	model = ReglaDePreCategorizacion
	template_name = 'confirmDeletion.html'
	success_url = reverse_lazy('home')
	context_object_name = 'instance'

	def get_context_data(self, **kwargs):
		context = super(RDPCDeleteView, self).get_context_data(**kwargs)
		context['form_title'] = u'Anular regla de pre-categorización'
		context['btn_confirm_lbl'] = 'Anular'
		context['cancel_url'] = reverse_lazy('home')
		return context

	def delete(self, request, *args, **kwargs):
		self.object = self.get_object()
		self.object.fue_anulado = True
		self.object.save()
		messages.success(request, u'Regla de pre-categorización "%s" anulada' %self.object.id)
		return HttpResponseRedirect(self.get_success_url())