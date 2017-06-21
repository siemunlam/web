"""siem_web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from rules.views import (AyudaView, CategoryCreateView, CategoryDeleteView,
                         CategoryUpdateView, FDACreateView, FDADeleteView,
                         FDAUpdateView, FDPCCreateView, FDPCDeleteView,
                         FDPCUpdateView, HomeView, RDACreateView,
                         RDADeleteView, RDAUpdateView, RDPCCreateView,
                         RDPCDeleteView, RDPCUpdateView, VDFDACreateView,
                         VDFDADeleteView, VDFDAUpdateView, VDFDPCCreateView,
                         VDFDPCDeleteView, VDFDPCUpdateView)

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    # Rules app
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^ayuda/$', AyudaView.as_view(), name='ayuda'),
    url(r'^rules/categories/create/$', CategoryCreateView.as_view(), name='category_create'),
	url(r'^rules/categories/(?P<pk>\d+)/edit/$', CategoryUpdateView.as_view(), name='category_update'),
	url(r'^rules/categories/(?P<pk>\d+)/delete/$', CategoryDeleteView.as_view(), name='category_delete'),
    url(r'^rules/fda/create/$', FDACreateView.as_view(), name='fda_create'),
	url(r'^rules/fda/(?P<pk>\d+)/edit/$', FDAUpdateView.as_view(), name='fda_update'),
	url(r'^rules/fda/(?P<pk>\d+)/delete/$', FDADeleteView.as_view(), name='fda_delete'),
    url(r'^rules/fdpc/create/$', FDPCCreateView.as_view(), name='fdpc_create'),
	url(r'^rules/fdpc/(?P<pk>\d+)/edit/$', FDPCUpdateView.as_view(), name='fdpc_update'),
	url(r'^rules/fdpc/(?P<pk>\d+)/delete/$', FDPCDeleteView.as_view(), name='fdpc_delete'),
    url(r'^rules/vdfda/create/$', VDFDACreateView.as_view(), name='vdfda_create'),
	url(r'^rules/vdfda/(?P<pk>\d+)/edit/$', VDFDAUpdateView.as_view(), name='vdfda_update'),
	url(r'^rules/vdfda/(?P<pk>\d+)/delete/$', VDFDADeleteView.as_view(), name='vdfda_delete'),
    url(r'^rules/vdfdpc/create/$', VDFDPCCreateView.as_view(), name='vdfdpc_create'),
	url(r'^rules/vdfdpc/(?P<pk>\d+)/edit/$', VDFDPCUpdateView.as_view(), name='vdfdpc_update'),
	url(r'^rules/vdfdpc/(?P<pk>\d+)/delete/$', VDFDPCDeleteView.as_view(), name='vdfdpc_delete'),
    url(r'^rules/rda/create/$', RDACreateView.as_view(), name='rda_create'),
	url(r'^rules/rda/(?P<pk>\d+)/edit/$', RDAUpdateView.as_view(), name='rda_update'),
	url(r'^rules/rda/(?P<pk>\d+)/delete/$', RDADeleteView.as_view(), name='rda_delete'),
    url(r'^rules/rdpc/create/$', RDPCCreateView.as_view(), name='rdpc_create'),
	url(r'^rules/rdpc/(?P<pk>\d+)/edit/$', RDPCUpdateView.as_view(), name='rdpc_update'),
	url(r'^rules/rdpc/(?P<pk>\d+)/delete/$', RDPCDeleteView.as_view(), name='rdpc_delete'),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
