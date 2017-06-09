import pytest
from django.core.urlresolvers import reverse
from django.test import RequestFactory, mock
from mixer.backend.django import mixer

from .. import views

pytestmark = pytest.mark.django_db



# Create your test here.
class TestHomeView:
	def test_anonymous(self):
		request = RequestFactory().get(reverse('home'))
		response = views.HomeView.as_view()(request)
		assert response.status_code == 200, 'Should be callable by anyone'
	
	def test_post(self):
		pass # TODO: make test


class TestCategoryCreateView:
	def test_anonymous(self):
		request = RequestFactory().get(reverse('category_create'))
		response = views.HomeView.as_view()(request)
		assert response.status_code == 200, 'Should be callable by anyone'
	
	def test_get_context_data(self):
		pass # TODO: make test

	def test_form_valid(self):
		pass # TODO: make test


class TestCategoryUpdateView:
	def test_anonymous(self):
		categoria = mixer.blend('rules.Categoria')
		request = RequestFactory().get(reverse('category_update', kwargs={'pk': categoria.id}))
		response = views.HomeView.as_view()(request)
		assert response.status_code == 200, 'Should be callable by anyone'

	def test_get_context_data(self):
		pass # TODO: make test


class TestCategoryDeleteView:
	def test_anonymous(self):
		categoria = mixer.blend('rules.Categoria')
		request = RequestFactory().get(reverse('category_delete', kwargs={'pk': categoria.id}))
		response = views.HomeView.as_view()(request)
		assert response.status_code == 200, 'Should be callable by anyone'

	def test_get_context_data(self):
		pass # TODO: make test
	
	def test_delete(self):
		pass # TODO: make test


class TestFDACreateView:
	def test_anonymous(self):
		request = RequestFactory().get(reverse('fda_create'))
		response = views.HomeView.as_view()(request)
		assert response.status_code == 200, 'Should be callable by anyone'

	def test_get_context_data(self):
		pass # TODO: make test

	def test_form_valid(self):
		pass # TODO: make test


class TestFDAUpdateView:
	def test_anonymous(self):
		fda = mixer.blend('rules.FactorDeAjuste')
		request = RequestFactory().get(reverse('fda_update', kwargs={'pk':fda.id}))
		response = views.HomeView.as_view()(request)
		assert response.status_code == 200, 'Should be callable by anyone'

	def test_get_context_data(self):
		pass # TODO: make test


class TestFDADeleteView:
	def test_anonymous(self):
		fda = mixer.blend('rules.FactorDeAjuste')
		request = RequestFactory().get(reverse('fda_delete', kwargs={'pk':fda.id}))
		response = views.HomeView.as_view()(request)
		assert response.status_code == 200, 'Should be callable by anyone'

	def test_get_context_data(self):
		pass # TODO: make test
	
	def test_delete(self):
		pass # TODO: make test


class TestFDPCCreateView:
	def test_anonymous(self):
		request = RequestFactory().get(reverse('fdpc_create'))
		response = views.HomeView.as_view()(request)
		assert response.status_code == 200, 'Should be callable by anyone'

	def test_get_context_data(self):
		pass # TODO: make test

	def test_form_valid(self):
		pass # TODO: make test


class TestFDPCUpdateView:
	def test_anonymous(self):
		fdpc = mixer.blend('rules.FactorDePreCategorizacion')
		request = RequestFactory().get(reverse('fdpc_update', kwargs={'pk':fdpc.id}))
		response = views.HomeView.as_view()(request)
		assert response.status_code == 200, 'Should be callable by anyone'

	def test_get_context_data(self):
		pass # TODO: make test


class TestFDPCDeleteView:
	def test_anonymous(self):
		fdpc = mixer.blend('rules.FactorDePreCategorizacion')
		request = RequestFactory().get(reverse('fdpc_delete', kwargs={'pk':fdpc.id}))
		response = views.HomeView.as_view()(request)
		assert response.status_code == 200, 'Should be callable by anyone'

	def test_get_context_data(self):
		pass # TODO: make test
	
	def test_delete(self):
		pass # TODO: make test


class TestVDFDACreateView:
	def test_anonymous(self):
		request = RequestFactory().get(reverse('vdfda_create'))
		response = views.HomeView.as_view()(request)
		assert response.status_code == 200, 'Should be callable by anyone'

	def test_get_context_data(self):
		pass # TODO: make test

	def test_form_valid(self):
		pass # TODO: make test


class TestVDFDAUpdateView:
	def test_anonymous(self):
		vdfda = mixer.blend('rules.ValorDeFactorDeAjuste')
		request = RequestFactory().get(reverse('vdfda_update', kwargs={'pk':vdfda.id}))
		response = views.HomeView.as_view()(request)
		assert response.status_code == 200, 'Should be callable by anyone'

	def test_get_context_data(self):
		pass # TODO: make test


class TestVDFDADeleteView:
	def test_anonymous(self):
		vdfda = mixer.blend('rules.ValorDeFactorDeAjuste')
		request = RequestFactory().get(reverse('vdfda_delete', kwargs={'pk':vdfda.id}))
		response = views.HomeView.as_view()(request)
		assert response.status_code == 200, 'Should be callable by anyone'

	def test_get_context_data(self):
		pass # TODO: make test
	
	def test_delete(self):
		pass # TODO: make test


class TestVDFDPCCreateView:
	def test_anonymous(self):
		request = RequestFactory().get(reverse('vdfdpc_create'))
		response = views.HomeView.as_view()(request)
		assert response.status_code == 200, 'Should be callable by anyone'

	def test_get_context_data(self):
		pass # TODO: make test

	def test_form_valid(self):
		pass # TODO: make test


class TestVDFDPCUpdateView:
	def test_anonymous(self):
		vdfdpc = mixer.blend('rules.ValorDeFactorDePreCategorizacion')
		request = RequestFactory().get(reverse('vdfdpc_update', kwargs={'pk':vdfdpc.id}))
		response = views.HomeView.as_view()(request)
		assert response.status_code == 200, 'Should be callable by anyone'

	def test_get_context_data(self):
		pass # TODO: make test


class TestVDFDPCDeleteView:
	def test_anonymous(self):
		vdfdpc = mixer.blend('rules.ValorDeFactorDePreCategorizacion')
		request = RequestFactory().get(reverse('vdfdpc_delete', kwargs={'pk':vdfdpc.id}))
		response = views.HomeView.as_view()(request)
		assert response.status_code == 200, 'Should be callable by anyone'

	def test_get_context_data(self):
		pass # TODO: make test
	
	def test_delete(self):
		pass # TODO: make test


class TestRDACreateView:
	def test_anonymous(self):
		request = RequestFactory().get(reverse('rda_create'))
		response = views.HomeView.as_view()(request)
		assert response.status_code == 200, 'Should be callable by anyone'

	def test_get_context_data(self):
		pass # TODO: make test

	def test_form_valid(self):
		pass # TODO: make test


class TestRDAUpdateView:
	def test_anonymous(self):
		regla = mixer.blend('rules.ReglaDeAjuste')
		request = RequestFactory().get(reverse('rda_update', kwargs={'pk':regla.id}))
		response = views.HomeView.as_view()(request)
		assert response.status_code == 200, 'Should be callable by anyone'

	def test_get_context_data(self):
		pass # TODO: make test


class TestRDADeleteView:
	def test_anonymous(self):
		regla = mixer.blend('rules.ReglaDeAjuste')
		request = RequestFactory().get(reverse('rda_delete', kwargs={'pk':regla.id}))
		response = views.HomeView.as_view()(request)
		assert response.status_code == 200, 'Should be callable by anyone'

	def test_get_context_data(self):
		pass # TODO: make test
	
	def test_delete(self):
		pass # TODO: make test


class TestRDPCCreateView:
	def test_anonymous(self):
		request = RequestFactory().get(reverse('rdpc_create'))
		response = views.HomeView.as_view()(request)
		assert response.status_code == 200, 'Should be callable by anyone'

	def test_get_context_data(self):
		pass # TODO: make test

	def test_form_valid(self):
		pass # TODO: make test


class TestRDPCUpdateView:
	def test_anonymous(self):
		regla = mixer.blend('rules.ReglaDePreCategorizacion')
		request = RequestFactory().get(reverse('rdpc_update', kwargs={'pk':regla.id}))
		response = views.HomeView.as_view()(request)
		assert response.status_code == 200, 'Should be callable by anyone'

	def test_get_context_data(self):
		pass # TODO: make test


class TestRDPCDeleteView:
	def test_anonymous(self):
		regla = mixer.blend('rules.ReglaDePreCategorizacion')
		request = RequestFactory().get(reverse('rdpc_delete', kwargs={'pk':regla.id}))
		response = views.HomeView.as_view()(request)
		assert response.status_code == 200, 'Should be callable by anyone'

	def test_get_context_data(self):
		pass # TODO: make test
	
	def test_delete(self):
		pass # TODO: make test
