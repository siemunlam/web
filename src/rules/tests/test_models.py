import pytest
from mixer.backend.django import mixer
pytestmark = pytest.mark.django_db

# Create your test here.
class TestCategoria:
    def test__str__(self):
        obj = mixer.blend('rules.Categoria')
        assert str(obj) == obj.descripcion, 'Should print obj.descripcion'


class TestAjuste:
    def test__str__(self):
        obj = mixer.blend('rules.Ajuste')
        assert str(obj) == str(obj.valor), 'Should print obj.valor'


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
        assert str(obj) == str(obj.factorDePreCategorizacion.descripcion) +" > "+ str(obj.descripcion), 'Should print parentObj.descripcion > obj.descripcion'


class TestValorDeFactorDeAjuste:
    def test__str__(self):
        obj = mixer.blend('rules.ValorDeFactorDeAjuste')
        assert str(obj) == str(obj.factorDeAjuste.descripcion) +" > "+ str(obj.descripcion), 'Should print parentObj.descripcion > obj.descripcion'


class TestReglaDePreCategorizacion:
    def test__str__(self):
        obj = mixer.blend('rules.ReglaDePreCategorizacion')
        assert str(obj) == "Regla "+ str(obj.id) +": if "+ str(obj.condicion.factorDePreCategorizacion) +" == " + obj.condicion.descripcion +" => precategorizacion = "+ str(obj.resultado), 'Should print "Regla obj.id: if obj.condicion.factorDePreCategorizacion == obj.condicion.descripcion => precategorizacion = obj.resultado"'


class TestReglaDeAjuste:
    def test__str__(self):
        obj = mixer.blend('rules.ReglaDeAjuste')
        assert str(obj) == "Regla "+ str(obj.id) +": if "+ str(obj.condicion.factorDeAjuste) +" == " + obj.condicion.descripcion +" => ajuste = "+ str(obj.resultado), 'Should print "Regla obj.id: if obj.condicion.factorDeAjuste == obj.condicion.descripcion => ajuste = obj.resultado"'