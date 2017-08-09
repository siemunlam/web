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
from rest_framework_jwt.views import obtain_jwt_token
from rules.views import (AyudaView, CategoryCreateView, CategoryDeleteView,
                         CategoryUpdateView, FDACreateView, FDADeleteView,
                         FDAUpdateView, FDPCCreateView, FDPCDeleteView,
                         FDPCUpdateView, HomeView, RDACreateView,
                         RDADeleteView, RDAUpdateView, RDPCCreateView,
                         RDPCDeleteView, RDPCUpdateView, VDFDACreateView,
                         VDFDADeleteView, VDFDAUpdateView, VDFDPCCreateView,
                         VDFDPCDeleteView, VDFDPCUpdateView)
from rules.api.views import CategoriaViewset, FactorDeAjusteViewSet, ValorDeFactorDeAjusteViewSet, FactorDePreCategorizacionViewSet, ValorDeFactorDePreCategorizacionViewSet, ReglaDeAjusteViewSet, ReglaDePreCategorizacionViewSet
from auxilios.views import AsignacionListView, AuxiliosListView
from auxilios.api import views
from medicos.views import MedicoListView
from analytics.views import (
    AnalyticsView, Report_1View, Report_2View, Report_3View, HeatMapView, 
#APIS
    Cat_Aux, Sol_Aux, Q_Aux_x_dia, Tiem_demora_ate, Tiem_espera_cola, Localizacion_aux)

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'solicitudes', views.SolicitudDeAuxilioViewSet, base_name='solicitudes')
router.register(r'auxilios', views.AuxilioViewSet, base_name='auxilios')
#router.register(r'moviles', views.MovilViewSet, base_name='moviles')
#router.register(r'medicos', views.MedicoViewSet, base_name='medicos')
router.register(r'asignaciones', views.AsignacionViewSet, base_name='asignaciones')
router.register(r'categoria', CategoriaViewset)
router.register(r'fda', FactorDeAjusteViewSet)
router.register(r'fdpc', FactorDePreCategorizacionViewSet)
router.register(r'vdfda', ValorDeFactorDeAjusteViewSet, base_name='vdfda')
router.register(r'vdfdpc', ValorDeFactorDePreCategorizacionViewSet, base_name='vdfdpc')
router.register(r'rda', ReglaDeAjusteViewSet)
router.register(r'rdpc', ReglaDePreCategorizacionViewSet)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    
    # Django Rest Framework API
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/', include(router.urls, namespace='api')),
    url(r'^docs/', include_docs_urls(title='SIEM API')),
    url(r'^api/auth/token/', obtain_jwt_token),
    url(r'^api/auxilios/', include('auxilios.api.urls', namespace='auxilios-api')),
	url(r'^api/users/', include('accounts.api.urls', namespace='users-api')),
	url(r'^api/medicos/', include('medicos.api.urls', namespace='medicos-api')),

    # Auxilios app
    url(r'^auxilios/$', AuxiliosListView.as_view(), name='auxilios'),

    # Moviles app
    #url(r'^moviles/$', MovilListView.as_view(), name='moviles'),

    # Asignacion app
    url(r'^asignaciones/$', AsignacionListView.as_view(), name='asignaciones'),

    # Medicos web app
	url(r'^medicos/$', MedicoListView.as_view(), name='medicos'),

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
    url(r'^heatmap/$', HeatMapView.as_view(), name='heatmap'),

    # Analytics App
    # Estas apis generan los datos de los gráficos en los reportes
    url(r'^api/analytics/data_cat_aux/$', Cat_Aux.as_view()), #Categoria de los auxilios (para el grafico de torta)
    url(r'^api/analytics/data_sol_aux/$', Sol_Aux.as_view()), #Origen de las solicitudes de los auxilios (para el grafico de barra)
    url(r'^api/analytics/data_Q_Aux_x_dia/$', Q_Aux_x_dia.as_view()), #Cantidad de auxilios por dia (para el grafico de linea)
    url(r'^api/analytics/data_Tiem_demora_ate/$', Tiem_demora_ate.as_view()), #Tiempos de demora en atencion
    url(r'^api/analytics/data_Tiem_espera_cola/$', Tiem_espera_cola.as_view()), #Tiempos de espera en cola
    url(r'^api/analytics/data_Localizacion_aux/$', Localizacion_aux.as_view()), #Tiempos de espera en cola
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
