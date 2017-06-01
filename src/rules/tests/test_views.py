import pytest
from django.test import RequestFactory

from .. import views


# Create your test here.
class TestHomeView:
    def test_anonymous(self):
        request = RequestFactory().get('/')
        response = views.HomeView.as_view()(request)
        assert response.status_code == 200, 'Should be callable by anyone'