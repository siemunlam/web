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

class TestFactorDeAjusteForm:
    def test_empty_form(self):
        form = forms.FactorDeAjusteForm(data={})
        assert form.is_valid() is False, 'Should be invalid if no data is submitted'
    
    def test_valid_form(self):
        form = forms.FactorDeAjusteForm(data={'descripcion': 'a'})
        assert form.is_valid() is True, 'Should be a valid form'

class TestFactorDePreCategorizacionForm:
    def test_empty_form(self):
        form = forms.FactorDePreCategorizacionForm(data={})
        assert form.is_valid() is False, 'Should be invalid if no data is submitted'
    
    def test_valid_form(self):
        form = forms.FactorDePreCategorizacionForm(data={'descripcion': 'a'})
        assert form.is_valid() is True, 'Should be a valid form'

class TestValorDeFactorDeAjusteForm:
    def test_empty_form(self):
        form = forms.ValorDeFactorDeAjusteForm(data={})
        assert form.is_valid() is False, 'Should be invalid if no data is submitted'
    
    def test_valid_form(self):
        factorDeAjuste = mixer.blend('rules.FactorDeAjuste')
        form = forms.ValorDeFactorDeAjusteForm(data={'descripcion': 'a', 'factorDeAjuste': factorDeAjuste.id})
        assert form.is_valid() is True, 'Should be a valid form'

class TestValorDeFactorDePreCategorizacionForm:
    def test_empty_form(self):
        form = forms.ValorDeFactorDePreCategorizacionForm(data={})
        assert form.is_valid() is False, 'Should be invalid if no data is submitted'
    
    def test_valid_form(self):
        factorDePreCategorizacion = mixer.blend('rules.FactorDePreCategorizacion')
        form = forms.ValorDeFactorDePreCategorizacionForm(data={'descripcion': 'a', 'factorDePreCategorizacion': factorDePreCategorizacion.id})
        assert form.is_valid() is True, 'Should be a valid form'

class TestReglaDeAjusteForm:
    def test_empty_form(self):
        form = forms.ReglaDeAjusteForm(data={})
        assert form.is_valid() is False, 'Should be invalid if no data is submitted'
    
    def test_valid_form(self):
        ajuste = mixer.blend('rules.Ajuste')
        valorDeFactorDeAjuste = mixer.blend('rules.ValorDeFactorDeAjuste')
        form = forms.ReglaDeAjusteForm(data={'condicion': valorDeFactorDeAjuste.id, 'resultado': ajuste.id, 'prioridad': 1})
        assert form.is_valid() is True, 'Should be a valid form'

class TestReglaDePreCategorizacionForm:
    def test_empty_form(self):
        form = forms.ReglaDePreCategorizacionForm(data={})
        assert form.is_valid() is False, 'Should be invalid if no data is submitted'
    
    def test_valid_form(self):
        categoria = mixer.blend('rules.Categoria')
        valorDeFactorDePreCategorizacion = mixer.blend('rules.ValorDeFactorDePreCategorizacion')
        form = forms.ReglaDePreCategorizacionForm(data={'condicion': valorDeFactorDePreCategorizacion.id, 'resultado': categoria.id, 'prioridad': 1})
        assert form.is_valid() is True, 'Should be a valid form'