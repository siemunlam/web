# -*- coding: utf-8 -*-
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import Ajuste, Categoria
from .forms import CategoriaForm


# Create your views here.
class HomeView(TemplateView):
	template_name = 'home.html'

	def get_context_data(self, **kwargs):
		context = super(HomeView, self).get_context_data(**kwargs)
		context['categorias'] = Categoria.objects.filter(fue_anulado = False).values('id', 'descripcion', 'prioridad', 'color')
		context['category_create_link'] = reverse_lazy('category_create')
		context['ajustes'] = Ajuste.objects.filter(fue_anulado = False).values('id', 'valor')
		return context


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
		self.object = self.get_object()
		self.object.fue_anulado = True
		self.object.save()
		messages.success(request, u'Categoría "%s" anulada' %self.object.descripcion)
		return HttpResponseRedirect(self.get_success_url())