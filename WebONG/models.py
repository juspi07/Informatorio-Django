from django.db import models
from image_cropping import ImageRatioField
from datetime import *
from django.contrib.auth.models import User

# Create your models here.

class Categoria(models.Model):
	Nombre = models.CharField(max_length=30, primary_key=True)

	def __str__(self):
		return self.Nombre 


class Blog(models.Model):
	ID = models.AutoField(primary_key=True)
	Titulo = models.TextField(max_length=150)
	Desc1 = models.TextField('Descripcion', help_text="Desc./subtit. debajo del titulo principal")
	SubT2 = models.TextField('Sub-Titulo 2', default='', help_text="Frase clave a recalcar entre parrafos (en negrita)")
	Desc2 = models.TextField('Descripcion 2', default='', help_text="Siguiente parrafo luego de la frase recalcada.")
	SubT3 = models.TextField('Sub-Titulo 3', default='', help_text="Nuevamente otra frase a recalcar si es necesario.")
	Desc3 = models.TextField('Descripcion 2', default='', help_text="Siguiente parrafo luego de la frase")
	Categoria = models.ForeignKey('Categoria',on_delete=models.CASCADE)
	Fecha_alta = models.DateField('Fecha de Alta', auto_now_add=True)
	
	Img1 = models.ImageField('Imagen Principal:', upload_to='img_productos/', 
		default='', 
		blank=True,
		null=True)
	Recorte1 = ImageRatioField('Img1', '700x435')
	Img2 = models.ImageField('Imagen 2:', upload_to='img_productos/',
		default='', 
		blank=True,
		null=True)
	Recorte2 = ImageRatioField('Img2', '800x500')
	Img3 = models.ImageField('Imagen 3:', upload_to='img_productos/',
		default='', 
		blank=True,
		null=True)
	Recorte3 = ImageRatioField('Img3', '800x500')

	def __str__(self):
		return str(self.ID)


class Comentario(models.Model):
	ID = models.AutoField(primary_key=True)
	Blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
	Usuario = models.ForeignKey(User, on_delete=models.CASCADE)
	Fecha_alta = models.DateField('Fecha de Creación', auto_now_add=True)
	Mensaje = models.TextField(max_length=100)


class Contacto(models.Model):
	nombre = models.TextField('Nombre', blank=False, max_length=100, editable=False)
	email = models.TextField('Email', blank=True, max_length=100, editable=False)
	asunto = models.TextField('Asunto', blank=True, max_length=100, editable=False)
	mensaje = models.TextField('Mensaje', blank=False, max_length=400, editable=False)
	fecha = models.DateField('Fecha', auto_now_add=True) 

	def __str__(self):
		return self.nombre

class UsuarioExtra(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    cumple = models.CharField(max_length=20,blank=True,null=True)
    tel = models.CharField(max_length=20,blank=True,null=True)
    direccion = models.CharField(max_length=30,blank=True,null=True)