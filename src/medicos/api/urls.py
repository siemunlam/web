from django.conf.urls import url

from .views import MedicoCreateAPIView, MedicoListAPIView, MedicosLogoutAPIView, MedicosRetrieveUpdateDestroyAPIView


urlpatterns = [
    url(r'^$', MedicoListAPIView.as_view(), name='list'),
    url(r'^register/$', MedicoCreateAPIView.as_view(), name='register'),
    url(r'^logout/$', MedicosLogoutAPIView.as_view(), name='logout'),
    url(r'^(?P<pk>\d+)$', MedicosRetrieveUpdateDestroyAPIView.as_view(), name='detail_update_destroy')    
]