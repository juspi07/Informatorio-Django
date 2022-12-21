from django.contrib import admin
from image_cropping import ImageCroppingMixin

from .models import *


admin.site.site_header = 'Entre Nosotras - Administracion'
admin.site.index_title = 'Panel de control del sitio web'
admin.site.site_title = 'Entre Nosotras - Administracion'


# Register your models here.

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
	list_display = ('Nombre',)


@admin.register(Blog)
class BlogAdmin(ImageCroppingMixin, admin.ModelAdmin):
	list_display = ('ID','Titulo', 'Fecha_alta')
	
	list_filter = ('Categoria','Fecha_alta')
	
	readonly_fields=('Fecha_alta',)

@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('get_Title','Usuario','Mensaje', 'Fecha_alta')

    readonly_fields=('get_Title','Usuario','Mensaje', 'Fecha_alta')
    
    def get_Title(self, obj):
        return obj.Blog.Titulo
	
@admin.register(Contacto)
class BlogAdmin(admin.ModelAdmin):
	list_display = ('nombre','email', 'asunto', 'mensaje', 'fecha')

	readonly_fields=('nombre','email', 'asunto', 'mensaje', 'fecha')


@admin.register(UsuarioExtra)
class UsuarioExtra(admin.ModelAdmin):
	list_display = ('usuario',)