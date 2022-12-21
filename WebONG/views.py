from django.shortcuts import render
from datetime import datetime
from django.db.utils import OperationalError
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from .models import *
from .forms import *
from django.db.models import Count
import locale
import logging
import time

locale.setlocale(locale.LC_TIME, '')
date = datetime.now().strftime('%A, %B %d, %Y')
tags = Categoria.objects.all()

########################################################################################################################
#                                               Funciones para vistas                                                  #
########################################################################################################################

def home(request):
	newnews = Blog.objects.order_by('Fecha_alta')[:12]
	NumComent = (Comentario.objects.values('Blog',).annotate(total=Count('Mensaje'),).order_by('-total'))

	context = {
		'date' : date,
		'newnews' : newnews,
		'NumComent' : NumComent,
		'tags' : tags, 
		}

	return render(request, 'index.html', {'context' : context})


def categorias(request, Nombre):
	blog = Blog.objects.all().filter(Categoria=Nombre)
	NumComent = (Comentario.objects
		.values('Blog',).annotate(total=Count('Mensaje'),).order_by())

	paginator = Paginator(blog, 8)
	page = request.GET.get('page')
	
	try:
		page_obj = paginator.page(page)
	except PageNotAnInteger:
		page_obj = paginator.page(1)
	except EmptyPage:
		page_obj = paginator.page(paginator.num_pages)

	context = {
		'date' : date,
		'tags' : tags,
		'blogs' : blog,
		'page_obj':page_obj,
		'NumComent':NumComent
		}
	
	return render(request, 'category.html', {'Nombre':Nombre, 'context' : context})


def noticia(request, Nombre, ID):
	noticia = Blog.objects.all().filter(ID = ID).get()
	Com = Comentario.objects.filter(Blog = ID)
	NumComent = (Comentario.objects.values('Blog',).annotate(total=Count('Mensaje'),).order_by('-total'))

	context = {
		'date' : date,
		'Nombre': Nombre,
		'noticia': noticia,
		'tags':tags,
		'Com':Com,
		'NumComent':NumComent
	}

	if request.method == 'POST':
		mensaje = request.POST.get('mensaje')
		item = Comentario(Blog=noticia, Usuario=request.user, Mensaje=mensaje)
		item.save()
		messages.warning(request, "Comentario guardado correctamente" )
	
	return render(request, 'single.html', {'context' : context})


def contacto(request):
	context ={
		'date' : date,
	}

	if request.method == 'POST':
		nombre = request.POST.get('nombre')
		email = request.POST.get('email')
		asunto = request.POST.get('asunto')
		mensaje = request.POST.get('mensaje')
		item = Contacto(nombre=nombre, asunto=asunto, email=email, mensaje=mensaje)
		item.save()
		messages.warning(request, "Recibimos tu mensaje. Gracias" )
	
	return render(request, 'contact.html', {'context' : context})

@login_required
def usuario(request):
	userextra = UsuarioExtra.objects.get(usuario = request.user)
	
	if request.method == 'POST':
		if User.username != request.POST.get('inputUsername'):
			if User.objects.filter(username = request.POST.get('inputUsername')).first():
				messages.error(request, "Usuario ya ocupado")
				return redirect('user')
		request.user.first_name = request.POST.get('inputFirstName')
		request.user.last_name = request.POST.get('inputLastName')
		request.user.email = request.POST.get('inputEmailAddress')
		userextra.direccion = request.POST.get('inputLocation')
		userextra.cumple = request.POST.get('inputBirthday')
		userextra.tel = request.POST.get('inputPhone')
		userextra.save()
		if request.POST.get('inputOrgName') != '' and not request.user.check_password(request.POST.get('inputOrgName')):
			request.user.set_password(request.POST.get('inputOrgName'))
			request.user.save()
			messages.warning(request, "Ingrese nuevamente")
			return redirect('home')
		request.user.save()
		messages.success(request, "Datos guardados correctamente")

	context ={
		'date' : date,
		'userextra' : userextra,
	}

	return render(request, 'user.html', {'context' : context})

########################################################################################################################
#                                               Log in y log out                                                       #
########################################################################################################################

def Auth_login(request):
	F_Log = Login(request.POST or None)

	if request.method == 'POST':
		if '_singin' in request.POST:
			if F_Log.is_valid():
				user = authenticate(username=F_Log.cleaned_data['username'], password=F_Log.cleaned_data['password'])
				if user is not None:
					login(request, user)
					return redirect('home')
				else:
					messages.warning(request, "Credenciales inválidas." )
					return redirect('login')
		else:
			if F_Log.is_valid():
				if User.objects.filter(username = F_Log.cleaned_data['username']).first():
					messages.error(request, "Usuario ya ocupado")
					return redirect('login')
				user = User.objects.create_user(F_Log.cleaned_data['username'], '', F_Log.cleaned_data['password'])
				user.save()
				login(request, user)
				UserExt, created = UsuarioExtra.objects.get_or_create(usuario=request.user)
				return redirect('home')

	return render(request, 'login.html', {'F_Log':F_Log})

@login_required
def log_user_out(request):
	logout(request)
	return redirect('home')