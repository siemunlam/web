from django.conf.urls import url

from .views import UserCreateAPIView


urlpatterns = [
    url(r'^register/$', UserCreateAPIView.as_view(), name='register')
]