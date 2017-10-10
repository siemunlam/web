from django.conf.urls import url

from .views import MotivosAjustePIView, MotivosPCAPIView, CategoriaUpdateAPIView

urlpatterns = [
    url(r'^motivosajuste/$', MotivosAjustePIView.as_view(), name='motivos_ajuste'),
    url(r'^motivospc/$', MotivosPCAPIView.as_view(), name='motivos_pc'),
    url(r'^categoria/(?P<pk>\d+)/$', CategoriaUpdateAPIView.as_view(), name='categoria')
]