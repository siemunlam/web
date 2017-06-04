import pytest
from django.core.urlresolvers import reverse
from django.test import RequestFactory, mock

from mixer.backend.django import mixer

from .. import views


# Create your test here.
class TestHomeView:
	def test_anonymous(self):
		request = RequestFactory().get(reverse('home'))
		response = views.HomeView.as_view()(request)
		assert response.status_code == 200, 'Should be callable by anyone'