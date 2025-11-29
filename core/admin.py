from django.contrib import admin
from .models import ProfesorProfile, Materia, Contenido, ImagenContenido


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


# ==================== IMAGEN CONTENIDO INLINE ====================

class ImagenContenidoInline(admin.TabularInline):
    model = ImagenContenido
    extra = 1
    fields = ('imagen', 'titulo', 'descripcion', 'orden')
    ordering = ('orden',)


# ==================== CONTENIDO INLINE ====================

class ContenidoInline(admin.StackedInline):
    model = Contenido
    extra = 1
    fields = ('titulo', 'descripcion', 'imagen_principal', 'archivo_pdf', 'link_video', 'estado_publicacion', 'orden')
    ordering = ('orden',)


# ==================== MATERIAS ====================

@admin.register(Materia)
class MateriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'curso_paralelo', 'profesor', 'estado_badge', 'fecha_creacion')
    list_filter = ('estado_publicacion', 'curso', 'fecha_creacion', 'profesor')
    search_fields = ('nombre', 'descripcion', 'profesor__user__first_name')
    readonly_fields = ('fecha_creacion', 'fecha_publicacion')
    inlines = [ContenidoInline]
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('nombre', 'descripcion', 'curso', 'paralelo')
        }),
        ('Presentación', {
            'fields': ('imagen_portada', 'color_portada', 'icono')
        }),
        ('Profesor', {
            'fields': ('profesor',)
        }),
        ('Publicación', {
            'fields': ('estado_publicacion', 'fecha_publicacion')
        }),
        ('Administración', {
            'fields': ('activo', 'fecha_creacion')
        }),
    )
    
    actions = ['publicar_materias', 'despublicar_materias']
    
    def curso_paralelo(self, obj):
        return f"{obj.curso} {obj.paralelo}"
    curso_paralelo.short_description = "Curso"
    
    def estado_badge(self, obj):
        colors = {
            'borrador': '#FFC107',
            'publicada': '#28A745'
        }
        return f'<span style="background-color: {colors.get(obj.estado_publicacion, "#6C757D")}; color: white; padding: 3px 10px; border-radius: 3px;">{obj.get_estado_publicacion_display()}</span>'
    estado_badge.allow_tags = True
    estado_badge.short_description = "Estado"
    
    def publicar_materias(self, request, queryset):
        updated = queryset.update(estado_publicacion='publicada')
        self.message_user(request, f'{updated} materia(s) publicada(s).')
    publicar_materias.short_description = "Publicar materias seleccionadas"
    
    def despublicar_materias(self, request, queryset):
        updated = queryset.update(estado_publicacion='borrador')
        self.message_user(request, f'{updated} materia(s) despublicada(s).')
    despublicar_materias.short_description = "Despublicar materias seleccionadas"


# ==================== CONTENIDOS ====================

@admin.register(Contenido)
class ContenidoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'materia', 'estado_badge', 'orden', 'fecha_creacion')
    list_filter = ('estado_publicacion', 'materia', 'fecha_creacion')
    search_fields = ('titulo', 'descripcion', 'materia__nombre')
    readonly_fields = ('fecha_creacion', 'fecha_publicacion')
    inlines = [ImagenContenidoInline]
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('materia', 'titulo', 'descripcion', 'orden')
        }),
        ('Multimedia', {
            'fields': ('imagen_principal', 'archivo_pdf', 'archivo_video', 'link_video')
        }),
        ('Publicación', {
            'fields': ('estado_publicacion', 'fecha_publicacion')
        }),
        ('Administración', {
            'fields': ('activo', 'fecha_creacion')
        }),
    )
    
    actions = ['publicar_contenidos', 'despublicar_contenidos']
    
    def estado_badge(self, obj):
        colors = {
            'privado': '#DC3545',
            'publico': '#28A745'
        }
        return f'<span style="background-color: {colors.get(obj.estado_publicacion, "#6C757D")}; color: white; padding: 3px 10px; border-radius: 3px;">{obj.get_estado_publicacion_display()}</span>'
    estado_badge.allow_tags = True
    estado_badge.short_description = "Estado"
    
    def publicar_contenidos(self, request, queryset):
        updated = queryset.update(estado_publicacion='publico')
        self.message_user(request, f'{updated} contenido(s) publicado(s).')
    publicar_contenidos.short_description = "Publicar contenidos seleccionados"
    
    def despublicar_contenidos(self, request, queryset):
        updated = queryset.update(estado_publicacion='privado')
        self.message_user(request, f'{updated} contenido(s) despublicado(s).')
    despublicar_contenidos.short_description = "Despublicar contenidos seleccionados"


# ==================== IMAGENES CONTENIDO ====================

@admin.register(ImagenContenido)
class ImagenContenidoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'contenido', 'orden')
    list_filter = ('contenido', 'fecha_creacion')
    search_fields = ('titulo', 'contenido__titulo')
    readonly_fields = ('fecha_creacion',)
    fieldsets = (
        ('Información', {
            'fields': ('contenido', 'imagen', 'titulo', 'descripcion')
        }),
        ('Organización', {
            'fields': ('orden',)
        }),
        ('Administración', {
            'fields': ('fecha_creacion',)
        }),
    )
    ordering = ('orden',)

