from django.conf.urls import url

from .views import MedicoCreateAPIView, MedicoListAPIView, MedicosLogoutAPIView, MedicosRetrieveDestroyAPIView, MedicoUpdateAPIView


urlpatterns = [
    url(r'^$', MedicoListAPIView.as_view(), name='list'),
    url(r'^register/$', MedicoCreateAPIView.as_view(), name='register'),
    url(r'^logout/$', MedicosLogoutAPIView.as_view(), name='logout'),
    url(r'^(?P<pk>\d+)$', MedicosRetrieveDestroyAPIView.as_view(), name='detail_destroy'),
    url(r'^(?P<pk>\d+)/edit$', MedicoUpdateAPIView.as_view(), name='edit'),
]