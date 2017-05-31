import pytest
from mixer.backend.django import mixer
pytestmark = pytest.mark.django_db

# Create your test here.
class TestCategoria():
    def test_init(self):
        obj = mixer.blend('rules.Categoria')
        assert obj.pk == 1, 'Should create a Categoria instance'