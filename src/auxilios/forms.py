# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import SolicitudDeAuxilio


# Create your forms here.
class SolicitudDeAuxilioForm(forms.ModelForm):
	class Meta:
		model = SolicitudDeAuxilio
		fields = ['contacto', 'nombre', 'sexo', 'cantidad_pacientes', 'ubicacion', 'ubicacion_especifica', 'ubicacion_coordenadas', 'observaciones']
		widgets = {
			'ubicacion': forms.TextInput(attrs={'autofocus': True, 'placeholder': 'Ingrese una calle y su altura'}),
			'ubicacion_especifica': forms.TextInput(attrs={'placeholder': "Frente a un kiosko // 3° 'A'"}),
			'cantidad_pacientes': forms.NumberInput(attrs={'min': 1}),
            'observaciones': forms.Textarea(attrs={'rows': 1})
		}
