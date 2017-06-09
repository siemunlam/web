import pytest
from mixer.backend.django import mixer

from ..extra_func import (ajustarPC, calcAjustesResultantes,
                          escribirReglasDeCategorizacion)
from ..models import Ajuste, Categoria

pytestmark = pytest.mark.django_db


# Create your test here.
class TestCalcAjustesResultantes:
	def test_calcularCantidadDeAjustes_0(self):
		assert calcAjustesResultantes(0) == 0, 'Should create 0 ajustes for 0 categories'
	
	def test_calcularCantidadDeAjustes_1(self):
		assert calcAjustesResultantes(1) == 0, 'Should create 0 ajustes for 1 category'
	
	def test_calcularCantidadDeAjustes_2(self):
		assert calcAjustesResultantes(2) == 3, 'Should create 3 ajustes for 1 category'

	def test_calcularCantidadDeAjustes_multiple(self):
		assert calcAjustesResultantes(7) == 13, 'Should create 2 ajustes for more than 2 categories'
		assert calcAjustesResultantes(20) == 39, 'Should create 2 ajustes for more than 2 categories'


class TestEscribirReglasDeCategorizacion:
	def test_escribirReglasDeCategorizacion(self):
		mixer.cycle(5).blend('rules.Categoria')
		mixer.cycle(9).blend('rules.Ajuste', valor = (num for num in range(-4, 5, 1)))
		categorias = Categoria.objects.all()
		ajustes = Ajuste.objects.all()
		assert escribirReglasDeCategorizacion(categorias, ajustes).find('rule') >= 0, 'Should find rule'
		# TODO: MEJORAR TEST


class TestAjustarPC:
	def test_ajustarPC(self):
		mixer.cycle(5).blend('rules.Categoria')
		mixer.cycle(9).blend('rules.Ajuste', valor = (num for num in range(-4, 5, 1)))
		categorias = Categoria.objects.all()
		ajustes = Ajuste.objects.all()
		assert ajustarPC(categorias, ajustes, categorias.first(), ajustes.first()) == categorias.first().descripcion
		assert ajustarPC(categorias, ajustes, categorias.last(), ajustes.last()) == categorias.last().descripcion
		assert ajustarPC(categorias, ajustes, categorias.first(), ajustes.last()) == categorias.last().descripcion
		assert ajustarPC(categorias, ajustes, categorias.last(), ajustes.first()) == categorias.first().descripcion
