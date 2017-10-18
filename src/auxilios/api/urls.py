from django.conf.urls import url

from .views import AuxilioCambioEstadoUpdateAPIView, SuscriptoresDeAuxilio

urlpatterns = [
	url(r'^(?P<pk>\d+)/estadoUpdate/$', AuxilioCambioEstadoUpdateAPIView.as_view(), name='estado_update'),
	url(r'^(?P<pk>\d+)/suscriptores/$', SuscriptoresDeAuxilio.as_view(), name='suscriptores')	
]