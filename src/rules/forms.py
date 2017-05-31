# -*- coding: utf-8 -*-
from django import forms

from .models import Categoria

# Create your forms here.
class CategoriaForm(forms.ModelForm):
	class Meta:
		model = Categoria
		fields = ['descripcion', 'prioridad', 'color']
		widgets = {
			'descripcion': forms.TextInput(attrs={'autofocus': True}),
			'prioridad': forms.NumberInput(attrs={'min': 0})
		}