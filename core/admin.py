from django.contrib import admin
from .models import ProfesorProfile, Materia, Contenido, ImagenContenido


@admin.register(ProfesorProfile)
class ProfesorProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'especialidad', 'fecha_registro')
    search_fields = ('user__username', 'especialidad')
    list_filter = ('fecha_registro',)


@admin.register(Materia)
class MateriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'profesor', 'estado_publicacion', 'fecha_creacion')
    search_fields = ('nombre', 'profesor__user__username')
    list_filter = ('estado_publicacion', 'fecha_creacion')


@admin.register(Contenido)
class ContenidoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'materia', 'tipo', 'estado_publicacion', 'fecha_creacion')
    search_fields = ('titulo', 'materia__nombre')
    list_filter = ('tipo', 'estado_publicacion', 'fecha_creacion')


@admin.register(ImagenContenido)
class ImagenContenidoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'contenido', 'imagen')
    search_fields = ('titulo', 'contenido__titulo')

