# -*- coding: utf-8 -*-

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
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.documentation import include_docs_urls
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token
from rules.views import (AyudaView, CategoryCreateView, CategoryDeleteView,
						 CategoryUpdateView, FDACreateView, FDADeleteView,
						 FDAUpdateView, FDPCCreateView, FDPCDeleteView,
						 FDPCUpdateView, RulesView, RDACreateView,
						 RDADeleteView, RDAUpdateView, RDPCCreateView,
						 RDPCDeleteView, RDPCUpdateView, VDFDACreateView,
						 VDFDADeleteView, VDFDAUpdateView, VDFDPCCreateView,
						 VDFDPCDeleteView, VDFDPCUpdateView, FDPCDetailView)
from rules.api.views import AjusteViewSet, CategoriaViewset, FactorDeAjusteViewSet, ValorDeFactorDeAjusteViewSet, FactorDePreCategorizacionViewSet, ValorDeFactorDePreCategorizacionViewSet, ReglaDeAjusteViewSet, ReglaDePreCategorizacionViewSet
from auxilios.views import AsignacionListView, AuxiliosListView, AuxiliosMovilesMapaView, HomeView
from auxilios.api.views import AsignacionViewSet, AuxilioUbicacionGPSListAPIView, AuxilioViewSet, FormularioFinalizacionRetrieveAPIView, SolicitudDeAuxilioDetailsListAPIView
from accounts.views import LoginView, LogoutView, UsersView
from medicos.views import MedicoListView
from analytics.views import (AnalyticsView, Report_1View, Report_2View, Report_3View, Report_4View, HeatMapView)

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'ajuste', AjusteViewSet)
router.register(r'auxilios', AuxilioViewSet, base_name='auxilios')
#router.register(r'moviles', views.MovilViewSet, base_name='moviles')
router.register(r'asignaciones', AsignacionViewSet, base_name='asignaciones')
router.register(r'categoria', CategoriaViewset)
router.register(r'fda', FactorDeAjusteViewSet, base_name='fda')
router.register(r'fdpc', FactorDePreCategorizacionViewSet, base_name='fdpc')
router.register(r'vdfda', ValorDeFactorDeAjusteViewSet, base_name='vdfda')
router.register(r'vdfdpc', ValorDeFactorDePreCategorizacionViewSet, base_name='vdfdpc')
router.register(r'rda', ReglaDeAjusteViewSet, base_name='rda')
router.register(r'rdpc', ReglaDePreCategorizacionViewSet, base_name='rdpc')

urlpatterns = [
	url(r'^admin/', admin.site.urls),
	
	# Django Rest Framework API
	url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
	url(r'^api/', include(router.urls, namespace='api')),
	url(r'^docs/', include_docs_urls(title='SIEM API')),
	url(r'^api/auth/token/', obtain_jwt_token),
	url(r'^api/auth/token/refresh/', refresh_jwt_token),
	url(r'^api/auxilios/', include('auxilios.api.urls', namespace='auxilios-api')),
	url(r'^api/formularioFinalizacion/(?P<pk>\d+)/$', FormularioFinalizacionRetrieveAPIView.as_view(), name='form_finalizacion_get'),
	url(r'^api/medicos/', include('medicos.api.urls', namespace='medicos-api')),
	url(r'^api/rules/', include('rules.api.urls', namespace='rules-api')),
	url(r'^api/solicitudes/$', SolicitudDeAuxilioDetailsListAPIView.as_view(), name='solicitudes_list'),
	url(r'^api/users/', include('accounts.api.urls', namespace='users-api')),
	url(r'^api/mapa/auxilios/$', AuxilioUbicacionGPSListAPIView.as_view(), name='aux_ubicaciones_list'),


	# Accounts web app
	url(r'^login/$', LoginView.as_view(), name='login'),
	url(r'^logout/$', LogoutView.as_view(), name='logout'),
	url(r'^users/$', UsersView.as_view(), name='users'),

	# Auxilios web app
	url(r'^$', HomeView.as_view(), name='home'),
	url(r'^auxilios/$', AuxiliosListView.as_view(), name='auxilios'),

	# Auxilios móviles mapa app
	url(r'^auxilios-moviles-mapa/$', AuxiliosMovilesMapaView.as_view(), name='auxilios-moviles-mapa'),

	# Moviles app
	#url(r'^moviles/$', MovilListView.as_view(), name='moviles'),

	# Asignacion app
	url(r'^asignaciones/$', AsignacionListView.as_view(), name='asignaciones'),

	# Medicos web app
	url(r'^medicos/$', MedicoListView.as_view(), name='medicos'),

	# Rules app
	url(r'^rules/$', RulesView.as_view(), name='rules'),
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
	url(r'^rules/fdpc/(?P<pk>\d+)/detail/$', FDPCDetailView.as_view(), name='fdpc_detail'),
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
	
	# Analytics Home
	# Pagina principal con los reportes
	url(r'^analytics/$', AnalyticsView.as_view(), name='analytics'),
	# Reporte 1
	url(r'^report_1/$', Report_1View.as_view(), name='report_1'),
	# Reporte 2
	url(r'^report_2/$', Report_2View.as_view(), name='report_2'),
	# Reporte 3
	url(r'^report_3/$', Report_3View.as_view(), name='report_3'),
	# Reporte 4
	url(r'^report_4/$', Report_4View.as_view(), name='report_4'),
	# Reporte Mapa de calor
	url(r'^heatmap/$', HeatMapView.as_view(), name='heatmap'),
]

if settings.DEBUG:
	import debug_toolbar
	urlpatterns = [
		url(r'^__debug__/', include(debug_toolbar.urls)),
	] + urlpatterns

if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
