# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import models


# Create your models here.
class SolicitudDeAuxilio(models.Model):
	fecha = models.DateTimeField(auto_now_add=True)
	ubicacion = models.CharField(verbose_name=u'ubicación', max_length=120)
	contacto_solicitante = models.CharField(verbose_name=u'contacto del solicitante', max_length=120, blank=True)
	motivo = models.TextField()
	observaciones = models.CharField(max_length=120, blank=True)
	generador = models.ForeignKey(settings.AUTH_USER_MODEL)
	
	def __str__(self):
		return self.id

	class Meta:
		ordering = ['-id']
		verbose_name = 'Solicitud de auxilio'
		verbose_name_plural = 'Solicitudes de auxilio'
