import pytest

from .. import forms


# Create your test here.
class TestCategoriaForm():
    def test_form(self):
        form = forms.CategoriaForm(data={})
        assert form.is_valid() is False, 'Should be invalid if no data is submitted'