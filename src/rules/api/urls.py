from django.conf.urls import url

from .views import MotivosAjustePIView, MotivosPCAPIView

urlpatterns = [
    url(r'^motivosajuste/$', MotivosAjustePIView.as_view(), name='motivos_ajuste'),
    url(r'^motivospc/$', MotivosPCAPIView.as_view(), name='motivos_pc'),
]