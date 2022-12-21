"""DjangoProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.urls import *
from django.conf.urls import url


from WebONG import views

urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('login/', views.Auth_login, name='login'),
    path('logout/', views.log_user_out, name='logout'),
    path('contacto/', views.contacto, name='contacto'),
    path('user/', views.usuario, name='user'),
    path('<str:Nombre>/', views.categorias, name='categoria'),
    path('<str:Nombre>/<str:ID>', views.noticia, name='noticia'),
    path('avatar/', include('avatar.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
