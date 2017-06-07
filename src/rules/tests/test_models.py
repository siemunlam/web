import pytest
from mixer.backend.django import mixer
pytestmark = pytest.mark.django_db

from .. import models


# Create your test here.
class TestCategoria:
	def test__str__(self):
		obj = mixer.blend('rules.Categoria')
		assert str(obj) == obj.descripcion, 'Should print obj.descripcion'


class TestAjuste:
	def test__str__(self):
		obj = mixer.blend('rules.Ajuste')
		assert str(obj) == str(obj.valor), 'Should print obj.valor'
	
	def test_crearAjustes_0(self):
		models.Ajuste.crearAjustes(self, 0)
		assert models.Ajuste.objects.count() == 0, 'Should not create ajustes'
	
	def test_crearAjustes_2(self):
		aj = mixer.blend('rules.Ajuste')
		models.Ajuste.crearAjustes(self, 2)
		assert models.Ajuste.objects.count() - 1 == 2, 'Should create 2 ajustes'
	
	def test_crearAjustes_3(self):
		models.Ajuste.crearAjustes(self, 3)
		assert models.Ajuste.objects.count() == 3, 'Should create 3 ajustes'

	def test_borrarAjustes_0_1(self):
		assert models.Ajuste.objects.count() == 0
		assert models.Ajuste.borrarAjustes(self, 0) == 0
		assert models.Ajuste.objects.count() == 0, 'Should not delete ajustes'
	
	def test_borrarAjustes_0_2(self):
		ajustes = mixer.cycle(3).blend('rules.Ajuste', valor = (num for num in range(-1, 2, 1)))
		assert models.Ajuste.objects.count() == 3
		assert models.Ajuste.borrarAjustes(self, 0) == 3
		assert models.Ajuste.objects.count() == 0, 'Should delete 3 ajustes'

	def test_borrarAjustes_3(self):
		ajustes = mixer.cycle(7).blend('rules.Ajuste', valor = (num for num in range(-3, 4, 1)))
		assert models.Ajuste.objects.count() == 7
		assert models.Ajuste.borrarAjustes(self, 5) == 2
		assert models.Ajuste.objects.count() == 5, 'Should delete 2 ajustes'


class TestFactorDePreCategorizacion:
	def test__str__(self):
		obj = mixer.blend('rules.FactorDePreCategorizacion')
		assert str(obj) == obj.descripcion, 'Should print obj.descripcion'


class TestFactorDeAjuste:
	def test__str__(self):
		obj = mixer.blend('rules.FactorDeAjuste')
		assert str(obj) == obj.descripcion, 'Should print obj.descripcion'


class TestValorDeFactorDePreCategorizacion:
	def test__str__(self):
		obj = mixer.blend('rules.ValorDeFactorDePreCategorizacion')
		assert str(obj) == str(obj.factorDePreCategorizacion.descripcion) +" es "+ str(obj.descripcion), 'Should print parentObj.descripcion > obj.descripcion'


class TestValorDeFactorDeAjuste:
	def test__str__(self):
		obj = mixer.blend('rules.ValorDeFactorDeAjuste')
		assert str(obj) == str(obj.factorDeAjuste.descripcion) +" es "+ str(obj.descripcion), 'Should print parentObj.descripcion > obj.descripcion'


class TestReglaDePreCategorizacion:
	def test__str__(self):
		obj = mixer.blend('rules.ReglaDePreCategorizacion')
		assert str(obj) == "Regla "+ str(obj.id) +": if "+ str(obj.condicion.factorDePreCategorizacion) +" == " + obj.condicion.descripcion +" => precategorizacion = "+ str(obj.resultado), 'Should print "Regla obj.id: if obj.condicion.factorDePreCategorizacion == obj.condicion.descripcion => precategorizacion = obj.resultado"'


class TestReglaDeAjuste:
	def test__str__(self):
		obj = mixer.blend('rules.ReglaDeAjuste')
		assert str(obj) == "Regla "+ str(obj.id) +": if "+ str(obj.condicion.factorDeAjuste) +" == " + obj.condicion.descripcion +" => ajuste = "+ str(obj.resultado), 'Should print "Regla obj.id: if obj.condicion.factorDeAjuste == obj.condicion.descripcion => ajuste = obj.resultado"'