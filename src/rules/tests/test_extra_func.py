import pytest
from mixer.backend.django import mixer
pytestmark = pytest.mark.django_db

from ..extra_func import calcAjustesResultantes


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