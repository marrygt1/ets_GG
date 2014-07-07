# -*- encoding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.core.mail import send_mail, EmailMultiAlternatives
from django.core.urlresolvers import reverse
from django.contrib.auth import login, authenticate, logout
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta, date
from slugify import slugify
import json
from context_processors import *
from forms import *
from models import *

def inicio(request):
	globales = variables_globales(request)
	mensaje= False 
	formulario = LoginForm()
	if not request.user.is_anonymous():
		if globales['HOY'] > EXPIRA:
			mensaje="Periodo de sistema expirado"
			logout(request)
		else:			
			if request.user.perfil == 'Maestro':
				return HttpResponseRedirect(reverse('index'))
			else:
				return HttpResponseRedirect(reverse('index_alumno'))
	if request.method == "POST":
		formulario = LoginForm(request.POST)
		if formulario.is_valid():
			usuario = formulario.cleaned_data["usuario"]
			password = formulario.cleaned_data["password"]
			acceso = authenticate(username=str(usuario), password=str(password))
			if acceso is not None:			
				if acceso.is_active:
					login(request, acceso)
					return HttpResponseRedirect(reverse('inicio'))
				else:
					mensaje="Tu usuario esta desactivado"		
			else:
				mensaje="Usuario o contraseña incorrecta"
		else:
			mensaje="Usuario o contraseña incorrecta"
	return render(request, 'login.html',locals())

def salir(request):
        logout(request)
        return HttpResponseRedirect(reverse('inicio'))

def index(request):	
	return render(request, 'blank.html', locals())

def crear_grafica(request):
	grafica_form = GraficaForm()
	valoresForm = ValoresForm()
	if request.method == "POST":
		grafica_form = GraficaForm(request.POST)
		valoresForm = ValoresForm(request.POST)
		if grafica_form.is_valid():
			if valoresForm.is_valid():
				value = request.POST['value2']
				color = request.POST['color2']
				highlight = request.POST['highlight2']
				label = request.POST['label2']
				grafica = grafica_form.save()
				valores = valoresForm.save()
				valores.grafica = grafica
				valores.save()
				valor2 = Valores()
				valor2.value = float(value)
				valor2.color = color
				valor2.highlight = highlight
				valor2.label = label
				valor2.grafica = grafica
				valor2.save()
				return HttpResponseRedirect(reverse('vista_previa', args=[grafica.id] ))
	return render(request, 'crear_grafica.html', locals())

def vista_previa(request, id):
	grafica = Graficas.objects.filter(id=id)[0]
	valoresForm = ValoresForm()
	valores = Valores.objects.filter(grafica = grafica)
	labels = []
	data = []
	for valor in valores:
		labels.append(valor.label)
		data.append(valor.value)
	return render(request, 'vista_previa.html', locals())

def actualizar(request):
	value = request.POST['value']
	color = request.POST['color']
	highlight = request.POST['highlight']
	label = request.POST['label']
	id = request.POST['grafica']
	grafica = Graficas.objects.filter(id=id)[0]
	valores = Valores()
	valores.value = value
	valores.color = color
	valores.highlight = highlight
	valores.label = label
	valores.grafica = grafica
	valores.save()
	#marcas = serializers.serialize("json", Marca.objects.filter(tienda__id = request.POST['tienda']).distinct(),fields=('nombre',))
	data = {'value':valores.value,'color':valores.color,'highlight':valores.highlight,'label':valores.label,'tipo':grafica.tipo}
	return HttpResponse(json.dumps(data),mimetype='application/json')

def index_alumno(request):
	graficas = Graficas.objects.all()
	return render(request, 'index_alumno.html', locals())

def vista(request, id):
	grafica = Graficas.objects.filter(id=id)[0]
	comentarios = Comentarios.objects.filter(grafica=grafica).order_by('-calificacion')
	comentariosForm = ComentariosForm
	if request.method == "POST":
		comentariosForm = ComentariosForm(request.POST)
		if comentariosForm.is_valid():
			coment = comentariosForm.save()
			coment.usuario = request.user
			coment.grafica = grafica
			coment.save()
	valores = Valores.objects.filter(grafica = grafica)
	labels = []
	data = []
	for valor in valores:
		labels.append(valor.label)
		data.append(valor.value)
	return render(request, 'vista.html', locals())
