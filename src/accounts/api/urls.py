from django.conf.urls import url

from .views import UserCreateAPIView, UserListAPIView, UserLoginAPIView, UserRetrieveUpdateDestroyAPIView


urlpatterns = [
    url(r'^login/$', UserLoginAPIView.as_view(), name='login'),
    url(r'^register/$', UserCreateAPIView.as_view(), name='register'),
    url(r'^$', UserListAPIView.as_view(), name='list'),
    url(r'^(?P<username>.+)/$', UserRetrieveUpdateDestroyAPIView.as_view(), name='detail_edit_destroy')
]