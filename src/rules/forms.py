# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _

import re

from .models import Categoria, FactorDeAjuste, FactorDePreCategorizacion, ValorDeFactorDeAjuste, ValorDeFactorDePreCategorizacion, ReglaDeAjuste, ReglaDePreCategorizacion

# Create your forms here.
class CategoriaForm(forms.ModelForm):
	class Meta:
		model = Categoria
		fields = ['descripcion', 'prioridad', 'color']
		widgets = {
			'descripcion': forms.TextInput(attrs={'autofocus': True}),
			'prioridad': forms.NumberInput(attrs={'min': 0}),
			'color': forms.TextInput(attrs={'type': 'color'})
		}
	
	def clean_color(self):
		pattern = re.compile('^#[A-Fa-f0-9]{6}$')
		color = self.cleaned_data['color']
		if not pattern.match(color):
			raise forms.ValidationError(_(u'El formato del color debe ser hexadecimal.'))
		return color


class FDAForm(forms.ModelForm):
	class Meta:
		model = FactorDeAjuste
		fields = ['descripcion']
		widgets = {
			'descripcion': forms.TextInput(attrs={'autofocus': True})
		}


class FDPCForm(forms.ModelForm):
	class Meta:
		model = FactorDePreCategorizacion
		fields = ['descripcion']
		widgets = {
			'descripcion': forms.TextInput(attrs={'autofocus': True})
		}


class VDFDAForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(VDFDAForm, self).__init__(*args, **kwargs)
		self.fields['factorDeAjuste'].queryset = FactorDeAjuste.objects.filter(fue_anulado = False)

	class Meta:
		model = ValorDeFactorDeAjuste
		fields = ['descripcion', 'factorDeAjuste']
		widgets = {
			'descripcion': forms.TextInput(attrs={'autofocus': True})
		}


class VDFDPCForm(forms.ModelForm):
	class Meta:
		model = ValorDeFactorDePreCategorizacion
		fields = ['descripcion', 'factorDePreCategorizacion']
		widgets = {
			'descripcion': forms.TextInput(attrs={'autofocus': True})
		}


class RDAForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(RDAForm, self).__init__(*args, **kwargs)
		self.fields['condicion'].queryset = ValorDeFactorDeAjuste.objects.filter(fue_anulado = False).order_by('factorDeAjuste')

	class Meta:
		model = ReglaDeAjuste
		fields = ['condicion', 'resultado', 'prioridad']
		widgets = {
			'condicion': forms.Select(attrs={'autofocus': True}),
			'prioridad': forms.NumberInput(attrs={'min': 0})
		}


class RDPCForm(forms.ModelForm):
	class Meta:
		model = ReglaDePreCategorizacion
		fields = ['condicion', 'resultado', 'prioridad']
		widgets = {
			'condicion': forms.Select(attrs={'autofocus': True}),
			'prioridad': forms.NumberInput(attrs={'min': 0})
		}