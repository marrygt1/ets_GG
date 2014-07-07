# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.conf import settings
from app.views import *
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^$', inicio, name='inicio'),
	url(r'^salir/$', salir, name='salir'),
	url(r'^index/$', index, name='index'),
	url(r'^index-alumno/$', index_alumno, name='index_alumno'),
	url(r'^crear-grafica/$', crear_grafica, name='crear_grafica'),
	url(r'^vista-previa/(.+)/$', vista_previa, name='vista_previa'),
	url(r'^vista/(.+)/$', vista, name='vista'),
	url(r'^actualizar/$', actualizar, name='actualizar'),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
)
