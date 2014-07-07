# -*- encoding: utf-8 -*-
from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import AbstractBaseUser, _user_has_perm, PermissionsMixin, _user_has_module_perms
from managers import UsuarioManager
from django.db.models.signals import *
from django.dispatch import receiver
from django.core.validators import RegexValidator
from datetime import datetime
from choices import *
try:
	from django.contrib.contenttypes.fields import GenericForeignKey
except ImportError:
	from django.contrib.contenttypes.generic import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
import reversion
from django.db.models.signals import pre_delete, post_save
from django.contrib.admin.models import LogEntry, DELETION, ADDITION, CHANGE
from django.utils.encoding import force_text
import inspect
from django.core.handlers.wsgi import WSGIRequest
from reversion.admin import VersionAdmin
from reversion.models import Version, Revision
import json
from django.utils.html import *

class Usuario(AbstractBaseUser, PermissionsMixin):
	usuario = models.CharField(max_length=35, unique=True, db_index=True)
	perfil  = models.CharField(max_length=25, choices=Perfiles)
	email = models.EmailField(max_length=50, unique=True)
	activo = models.BooleanField(default=True, help_text='Activa un usuario para poder entrar en el sistema')
	administrador = models.BooleanField(default=False, help_text='Que usuarios se les permite entrar al administrador')
	objects = UsuarioManager()
	USERNAME_FIELD = 'usuario'
	def get_full_name(self):
		return self.usuario + ' ' + self.perfil
	def get_short_name(self):
		return self.usuario
	def __unicode__(self):
		return self.usuario
	def has_perm(self, perm, obj=None):
		if self.is_superuser:
			return True
		return _user_has_perm(self, perm, obj=obj)
	def has_module_perms(self, app_label):
		return True
	@property
	def is_staff(self):
		return self.administrador
	@property
	def is_active(self):
		return self.activo
	def __unicode__(self) :
	    return '%s' % (self.usuario)

class Curso(models.Model):
	nombre = models.CharField(max_length=40, unique=True, db_index=True)
	def __unicode__(self) :
	    return '%s' % (self.nombre)
	class Meta:
		verbose_name_plural = u'Cursos'
		verbose_name=u'Curso'

class Graficas(models.Model):
	nombre = models.CharField(max_length=40, unique=True, db_index=True)
	tipo = models.CharField(max_length=40, choices=Graficas )
	curso = models.ForeignKey('Curso')
	def Modificar(self):
		return mark_safe("<a href='%s' >Modificar</a>" % reverse('vista_previa', args=[self.id])) 
	def __unicode__(self) :
	    return '%s' % (self.nombre)
	class Meta:
		verbose_name_plural = u'Graficas'
		verbose_name=u'Grafica'

class Valores(models.Model):
	value = models.FloatField(max_length=40)
	color = models.CharField(max_length=40, default='0')
	highlight = models.CharField(max_length=40, default='0')
	label = models.CharField(max_length=40)
	grafica = models.ForeignKey('Graficas', null=True)
	def __unicode__(self) :
	    return '%s' % (self.id)
	class Meta:
		verbose_name_plural = u'Valores'
		verbose_name=u'Valor'

class Comentarios(models.Model):
	usuario = models.ForeignKey('Usuario', null=True)
	grafica = models.ForeignKey('Graficas', null=True)
	comentario = models.CharField(max_length=244,)
	calificacion = models.IntegerField(default=0)
	def __unicode__(self) :
	    return '%s' % (self.id)
	class Meta:
		verbose_name_plural = u'Comentarios'
		verbose_name=u'Comentario'
