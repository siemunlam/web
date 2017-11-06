from django.conf.urls import url

from .views import AuxilioCambioEstadoUpdateAPIView, DesuscribirseDeAuxilio, SuscriptoresDeAuxilio

urlpatterns = [
	url(r'^(?P<pk>\d+)/estadoUpdate/$', AuxilioCambioEstadoUpdateAPIView.as_view(), name='estado_update'),
	url(r'^(?P<codigo_suscripcion>\w+)/suscribirse/$', SuscriptoresDeAuxilio.as_view(), name='suscriptores'),
	url(r'^(?P<codigo_suscripcion>\w+)/desuscribirse/(?P<codigo_fbm>.+)$', DesuscribirseDeAuxilio.as_view(), name='desuscribirse')
]