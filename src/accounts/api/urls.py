from django.conf.urls import url

from .views import UserCreateAPIView, UserListAPIView, UserLoginAPIView, UserRetrieveUpdateDestroyAPIView, UserPwdUpdateAPIView


urlpatterns = [
    url(r'^login/$', UserLoginAPIView.as_view(), name='login'),
    url(r'^register/$', UserCreateAPIView.as_view(), name='register'),
    url(r'^$', UserListAPIView.as_view(), name='list'),
    url(r'^(?P<username>\w+)/$', UserRetrieveUpdateDestroyAPIView.as_view(), name='detail_edit_destroy'),
    url(r'^pwd_update$', UserPwdUpdateAPIView.as_view(), name='pwd_update')
]