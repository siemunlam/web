import pytest
from mixer.backend.django import mixer
pytestmark = pytest.mark.django_db

from .. import forms


# Create your test here.
class TestCategoriaForm:
	def test_empty_form(self):
		form = forms.CategoriaForm(data={})
		assert form.is_valid() is False, 'Should be invalid if no data is submitted'
	
	def test_invalid_color_form(self):
		form = forms.CategoriaForm(data={'descripcion': 'a', 'prioridad': 2, 'color':'#fkme'})
		assert form.is_valid() is False, 'Should be invalid if incorrect color is submitted'
		form = forms.CategoriaForm(data={'descripcion': 'a', 'prioridad': 2, 'color':'#fkmeE3'})
		assert form.is_valid() is False, 'Should be invalid if incorrect color is submitted'
		form = forms.CategoriaForm(data={'descripcion': 'a', 'prioridad': 2, 'color':'fFeeE3'})
		assert form.is_valid() is False, 'Should be invalid if incorrect color is submitted'
		form = forms.CategoriaForm(data={'descripcion': 'a', 'prioridad': 2, 'color':'#feeE3'})
		assert form.is_valid() is False, 'Should be invalid if incorrect color is submitted'
	
	def test_valid_form(self):
		form = forms.CategoriaForm(data={'descripcion': 'a', 'prioridad': 2, 'color': '#f4D23C'})
		assert form.is_valid() is True, 'Should be a valid form since correst color hex was submitted'

class TestFDAForm:
	def test_empty_form(self):
		form = forms.FDAForm(data={})
		assert form.is_valid() is False, 'Should be invalid if no data is submitted'
	
	def test_valid_form(self):
		form = forms.FDAForm(data={'descripcion': 'a'})
		assert form.is_valid() is True, 'Should be a valid form'

class TestFDPCForm:
	def test_empty_form(self):
		form = forms.FDPCForm(data={})
		assert form.is_valid() is False, 'Should be invalid if no data is submitted'
	
	def test_valid_form(self):
		form = forms.FDPCForm(data={'descripcion': 'a'})
		assert form.is_valid() is True, 'Should be a valid form'

class TestVDFDAForm:
	def test_empty_form(self):
		form = forms.VDFDAForm(data={})
		assert form.is_valid() is False, 'Should be invalid if no data is submitted'
	
	def test_valid_form(self):
		factorDeAjuste = mixer.blend('rules.FactorDeAjuste')
		form = forms.VDFDAForm(data={'descripcion': 'a', 'factorDeAjuste': factorDeAjuste.id})
		assert form.is_valid() is True, 'Should be a valid form'

class TestVDFDPCForm:
	def test_empty_form(self):
		form = forms.VDFDPCForm(data={})
		assert form.is_valid() is False, 'Should be invalid if no data is submitted'
	
	def test_valid_form(self):
		factorDePreCategorizacion = mixer.blend('rules.FactorDePreCategorizacion')
		form = forms.VDFDPCForm(data={'descripcion': 'a', 'factorDePreCategorizacion': factorDePreCategorizacion.id})
		assert form.is_valid() is True, 'Should be a valid form'

class TestRDAForm:
	def test_empty_form(self):
		form = forms.RDAForm(data={})
		assert form.is_valid() is False, 'Should be invalid if no data is submitted'
	
	def test_valid_form(self):
		ajuste = mixer.blend('rules.Ajuste')
		valorDeFactorDeAjuste = mixer.blend('rules.ValorDeFactorDeAjuste')
		form = forms.RDAForm(data={'condicion': valorDeFactorDeAjuste.id, 'resultado': ajuste.id, 'prioridad': 1})
		assert form.is_valid() is True, 'Should be a valid form'

class TestRDPCForm:
	def test_empty_form(self):
		form = forms.RDPCForm(data={})
		assert form.is_valid() is False, 'Should be invalid if no data is submitted'
	
	def test_valid_form(self):
		categoria = mixer.blend('rules.Categoria')
		valorDeFactorDePreCategorizacion = mixer.blend('rules.ValorDeFactorDePreCategorizacion')
		form = forms.RDPCForm(data={'condicion': valorDeFactorDePreCategorizacion.id, 'resultado': categoria.id, 'prioridad': 1})
		assert form.is_valid() is True, 'Should be a valid form'