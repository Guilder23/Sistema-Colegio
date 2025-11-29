from django.contrib import admin
from django.utils.html import format_html
from .models import (
    ProfesorProfile, Historia, Mision, Vision, Autoridad,
    ProfesorPublico, Estudiante, Materia, Contenido, ImagenContenido,
    InformacionColegio, Noticia, GaleriaImagenes
)

# ==================== PROFESOR PROFILE ====================

@admin.register(ProfesorProfile)
class ProfesorProfileAdmin(admin.ModelAdmin):
    list_display = ('nombre_profesor', 'especialidad', 'activo', 'fecha_registro')
    list_filter = ('activo', 'fecha_registro', 'especialidad')
    search_fields = ('user__first_name', 'user__last_name', 'especialidad')
    readonly_fields = ('fecha_registro',)
    fieldsets = (
        ('Usuario', {'fields': ('user',)}),
        ('Información Profesional', {'fields': ('especialidad', 'biografia', 'foto')}),
        ('Contacto', {'fields': ('telefono',)}),
        ('Estado', {'fields': ('activo', 'fecha_registro')}),
    )

    def nombre_profesor(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"
    nombre_profesor.short_description = "Profesor"


# ==================== INFORMACIÓN INSTITUCIONAL ====================

@admin.register(Historia)
class HistoriaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'activo', 'fecha_publicacion')
    list_filter = ('activo', 'fecha_publicacion')
    search_fields = ('titulo', 'contenido')
    readonly_fields = ('fecha_publicacion', 'fecha_actualizacion')
    fieldsets = (
        ('Contenido', {'fields': ('titulo', 'contenido', 'imagen_principal')}),
        ('Fecha', {'fields': ('fecha_publicacion', 'fecha_actualizacion')}),
        ('Estado', {'fields': ('activo',)}),
    )


@admin.register(Mision)
class MisionAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Contenido', {'fields': ('contenido', 'imagen_opcional')}),
        ('Fecha', {'fields': ('fecha_actualizacion',)}),
    )
    readonly_fields = ('fecha_actualizacion',)


@admin.register(Vision)
class VisionAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Contenido', {'fields': ('contenido', 'imagen_opcional')}),
        ('Fecha', {'fields': ('fecha_actualizacion',)}),
    )
    readonly_fields = ('fecha_actualizacion',)


@admin.register(Autoridad)
class AutoridadAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'cargo', 'activo', 'orden')
    list_filter = ('activo', 'cargo')
    search_fields = ('nombre', 'cargo')
    ordering = ('orden',)
    fieldsets = (
        ('Información', {'fields': ('nombre', 'cargo', 'foto', 'descripcion_opcional')}),
        ('Contacto', {'fields': ('facebook_link', 'instagram_link', 'correo_contacto')}),
        ('Orden', {'fields': ('orden',)}),
        ('Estado', {'fields': ('activo',)}),
    )


# ==================== PROFESORES PÚBLICOS ====================

@admin.register(ProfesorPublico)
class ProfesorPublicoAdmin(admin.ModelAdmin):
    list_display = ('nombre_completo', 'especialidad', 'activo', 'orden')
    list_filter = ('activo', 'especialidad')
    search_fields = ('nombres', 'apellidos', 'especialidad')
    ordering = ('orden',)
    fieldsets = (
        ('Información Personal', {'fields': ('nombres', 'apellidos', 'especialidad', 'foto')}),
        ('Descripción', {'fields': ('descripcion_corta',)}),
        ('Orden', {'fields': ('orden',)}),
        ('Estado', {'fields': ('activo',)}),
    )

    def nombre_completo(self, obj):
        return f"{obj.nombres} {obj.apellidos}"
    nombre_completo.short_description = "Nombre"


# ==================== ESTUDIANTES ====================

@admin.register(Estudiante)
class EstudianteAdmin(admin.ModelAdmin):
    list_display = ('nombre_completo', 'curso', 'paralelo', 'activo')
    list_filter = ('activo', 'curso', 'paralelo')
    search_fields = ('nombres', 'apellidos')
    fieldsets = (
        ('Información Personal', {'fields': ('nombres', 'apellidos', 'foto')}),
        ('Académico', {'fields': ('curso', 'paralelo')}),
        ('Descripción', {'fields': ('descripcion',)}),
        ('Estado', {'fields': ('activo',)}),
    )

    def nombre_completo(self, obj):
        return f"{obj.nombres} {obj.apellidos}"
    nombre_completo.short_description = "Nombre"


# ==================== MATERIAS ====================

class ContenidoInline(admin.TabularInline):
    model = Contenido
    extra = 1
    fields = ('titulo', 'estado_publicacion', 'orden')


@admin.register(Materia)
class MateriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'profesor_nombre', 'curso_paralelo', 'estado_publicacion', 'fecha_creacion')
    list_filter = ('estado_publicacion', 'profesor', 'curso', 'fecha_creacion')
    search_fields = ('nombre', 'descripcion', 'profesor__user__first_name')
    readonly_fields = ('fecha_creacion', 'fecha_publicacion')
    inlines = [ContenidoInline]
    fieldsets = (
        ('Información', {'fields': ('nombre', 'descripcion', 'profesor')}),
        ('Académico', {'fields': ('curso', 'paralelo')}),
        ('Imagen y Estilo', {'fields': ('imagen_portada', 'color_portada', 'icono')}),
        ('Publicación', {'fields': ('estado_publicacion', 'fecha_creacion', 'fecha_publicacion')}),
        ('Estado', {'fields': ('activo',)}),
    )
    actions = ['publicar_materias', 'despublicar_materias']

    def profesor_nombre(self, obj):
        return f"{obj.profesor.user.first_name} {obj.profesor.user.last_name}"
    profesor_nombre.short_description = "Profesor"

    def curso_paralelo(self, obj):
        return f"{obj.curso} - {obj.paralelo}"
    curso_paralelo.short_description = "Curso - Paralelo"

    def publicar_materias(self, request, queryset):
        for materia in queryset:
            materia.publicar()
        self.message_user(request, f"{queryset.count()} materias publicadas")
    publicar_materias.short_description = "Publicar materias seleccionadas"

    def despublicar_materias(self, request, queryset):
        for materia in queryset:
            materia.despublicar()
        self.message_user(request, f"{queryset.count()} materias despublicadas")
    despublicar_materias.short_description = "Despublicar materias seleccionadas"


# ==================== CONTENIDOS ====================

class ImagenContenidoInline(admin.TabularInline):
    model = ImagenContenido
    extra = 1
    fields = ('imagen', 'titulo', 'orden')


@admin.register(Contenido)
class ContenidoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'materia', 'estado_publicacion', 'orden', 'fecha_creacion')
    list_filter = ('estado_publicacion', 'materia', 'fecha_creacion')
    search_fields = ('titulo', 'descripcion', 'materia__nombre')
    readonly_fields = ('fecha_creacion', 'fecha_publicacion')
    inlines = [ImagenContenidoInline]
    fieldsets = (
        ('Información', {'fields': ('materia', 'titulo', 'descripcion')}),
        ('Multimedia', {'fields': ('imagen_principal', 'archivo_pdf', 'archivo_video', 'link_video')}),
        ('Publicación', {'fields': ('estado_publicacion', 'orden', 'fecha_creacion', 'fecha_publicacion')}),
        ('Estado', {'fields': ('activo',)}),
    )
    actions = ['publicar_contenidos', 'despublicar_contenidos']

    def publicar_contenidos(self, request, queryset):
        for contenido in queryset:
            contenido.publicar()
        self.message_user(request, f"{queryset.count()} contenidos publicados")
    publicar_contenidos.short_description = "Publicar contenidos seleccionados"

    def despublicar_contenidos(self, request, queryset):
        for contenido in queryset:
            contenido.despublicar()
        self.message_user(request, f"{queryset.count()} contenidos despublicados")
    despublicar_contenidos.short_description = "Despublicar contenidos seleccionados"


@admin.register(ImagenContenido)
class ImagenContenidoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'contenido', 'orden')
    list_filter = ('contenido__materia', 'orden')
    search_fields = ('titulo', 'contenido__titulo')
    ordering = ('orden',)


# ==================== INFORMACIÓN GENERAL ====================

@admin.register(InformacionColegio)
class InformacionColegioAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Información General', {'fields': ('nombre', 'direccion', 'logo', 'favicon')}),
        ('Contacto', {'fields': ('correo_institucional', 'telefono_1', 'telefono_2')}),
        ('Horarios', {'fields': ('horario_inicio', 'horario_fin')}),
        ('Ubicación', {'fields': ('latitud', 'longitud')}),
        ('Redes Sociales', {'fields': ('facebook_url', 'instagram_url', 'tiktok_url')}),
    )


# ==================== NOTICIAS ====================

@admin.register(Noticia)
class NoticiaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'destacada', 'activo', 'fecha_creacion')
    list_filter = ('destacada', 'activo', 'fecha_creacion')
    search_fields = ('titulo', 'contenido')
    readonly_fields = ('fecha_creacion', 'fecha_actualizacion')
    fieldsets = (
        ('Contenido', {'fields': ('titulo', 'contenido', 'imagen')}),
        ('Detalles', {'fields': ('fecha_evento', 'destacada')}),
        ('Fecha', {'fields': ('fecha_creacion', 'fecha_actualizacion')}),
        ('Estado', {'fields': ('activo',)}),
    )


# ==================== GALERÍA ====================

@admin.register(GaleriaImagenes)
class GaleriaImagenesAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'categoria', 'activo', 'orden')
    list_filter = ('categoria', 'activo', 'orden')
    search_fields = ('titulo', 'categoria')
    ordering = ('orden',)
    fieldsets = (
        ('Información', {'fields': ('titulo', 'imagen', 'descripcion')}),
        ('Categoría', {'fields': ('categoria',)}),
        ('Orden', {'fields': ('orden',)}),
        ('Estado', {'fields': ('activo',)}),
    )
