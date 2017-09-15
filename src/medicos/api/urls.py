from django.conf.urls import url

from .views import MedicoActualizarFCMUpdateAPIView, MedicoActualizarGPSUpdateAPIView, MedicoCambioEstadoUpdateAPIView, MedicoCreateAPIView, MedicoListAPIView, MedicosLogoutAPIView, MedicosRetrieveDestroyAPIView, MedicoUpdateAPIView
from auxilios.api.views import AsignacionCambioEstadoAPIView, AsignacionDesvincularAPIView, AsignacionFinalizarAPIView

urlpatterns = [
    url(r'^$', MedicoListAPIView.as_view(), name='list'),
    url(r'^register/$', MedicoCreateAPIView.as_view(), name='register'),
    url(r'^logout/$', MedicosLogoutAPIView.as_view(), name='logout'),
    url(r'^estadoUpdate/$', MedicoCambioEstadoUpdateAPIView.as_view(), name='estado_update'),
    url(r'^estadoAsignacionUpdate/$', AsignacionCambioEstadoAPIView.as_view(), name='estado_asignacion_update'),
    url(r'^finalizarAsignacion/$', AsignacionFinalizarAPIView.as_view(), name='finalizar_asignacion'),
    url(r'^desvincularAsignacion/$', AsignacionDesvincularAPIView.as_view(), name='desvincular_asignacion'),
    url(r'^fcmUpdate/$', MedicoActualizarFCMUpdateAPIView.as_view(), name='fcb_update'),
    url(r'^ubicacionUpdate/$', MedicoActualizarGPSUpdateAPIView.as_view(), name='ubicacion_update'),
    url(r'^(?P<pk>\d+)/$', MedicosRetrieveDestroyAPIView.as_view(), name='detail_destroy'),
    url(r'^(?P<pk>\d+)/edit$', MedicoUpdateAPIView.as_view(), name='edit')
]