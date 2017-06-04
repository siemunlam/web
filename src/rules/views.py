# -*- coding: utf-8 -*-
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import Categoria
from .forms import CategoriaForm


# Create your views here.
class HomeView(TemplateView):
	template_name = 'home.html'

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
	permission_required = 'kiosko.change_categoria'

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
		context['form_title'] = u'Eliminar categoría'
		context['btn_confirm_lbl'] = 'Eliminar'
		context['cancel_url'] = reverse_lazy('home')
		return context

	def delete(self, request, *args, **kwargs):
		self.object = self.get_object()
		descripcion = self.object.descripcion
		self.object.delete()
		messages.success(request, u'Categoría "%s" eliminada' %descripcion)
		return HttpResponseRedirect(self.get_success_url())