from django.conf.urls import url

from .views import AuxilioCambioEstadoUpdateAPIView


urlpatterns = [
    url(r'^(?P<pk>\d+)/estadoUpdate/$', AuxilioCambioEstadoUpdateAPIView.as_view(), name='estado_update'),
]