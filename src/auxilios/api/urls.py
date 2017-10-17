from django.conf.urls import url

from .views import AuxilioCambioEstadoUpdateAPIView, AuxilioUbicacionGPSListAPIView, SuscriptoresDeAuxilio

urlpatterns = [
	url(r'^(?P<pk>\d+)/estadoUpdate/$', AuxilioCambioEstadoUpdateAPIView.as_view(), name='estado_update'),
	url(r'^(?P<pk>\d+)/suscriptores/$', SuscriptoresDeAuxilio.as_view(), name='suscriptores'),
	url(r'^ubicacionesGPS/$', AuxilioUbicacionGPSListAPIView.as_view(), name='ubicaciones_list'),
]
