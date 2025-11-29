from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# ==================== MODELOS DE USUARIO ====================

class ProfesorProfile(models.Model):
    """Perfil extendido del profesor para login"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profesor_profile')
    especialidad = models.CharField(max_length=100, blank=True, null=True)
    biografia = models.TextField(blank=True, null=True)
    foto = models.ImageField(upload_to='profesores/', blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

    class Meta:
        verbose_name = "Perfil Profesor"
        verbose_name_plural = "Perfiles Profesores"


# ==================== MODELOS INSTITUCIONALES ====================

class Historia(models.Model):
    """Historia del colegio"""
    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    imagen_principal = models.ImageField(upload_to='contenidos/')
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name_plural = "Historias"


class Mision(models.Model):
    """Misión del colegio"""
    contenido = models.TextField()
    imagen_opcional = models.ImageField(upload_to='contenidos/', blank=True, null=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Misión del Colegio"

    class Meta:
        verbose_name_plural = "Misiones"


class Vision(models.Model):
    """Visión del colegio"""
    contenido = models.TextField()
    imagen_opcional = models.ImageField(upload_to='contenidos/', blank=True, null=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Visión del Colegio"

    class Meta:
        verbose_name_plural = "Visiones"


class Autoridad(models.Model):
    """Autoridades del colegio (Director, Subdirector, etc.)"""
    nombre = models.CharField(max_length=100)
    cargo = models.CharField(max_length=100)
    foto = models.ImageField(upload_to='autoridades/')
    descripcion_opcional = models.TextField(blank=True, null=True)
    facebook_link = models.URLField(blank=True, null=True)
    instagram_link = models.URLField(blank=True, null=True)
    correo_contacto = models.EmailField(blank=True, null=True)
    orden = models.IntegerField(default=0, help_text="Orden de visualización")
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre} - {self.cargo}"

    class Meta:
        ordering = ['orden']
        verbose_name_plural = "Autoridades"


# ==================== PROFESORES PÚBLICOS ====================

class ProfesorPublico(models.Model):
    """Información pública del profesor (para mostrar en el sitio)"""
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    especialidad = models.CharField(max_length=100)
    foto = models.ImageField(upload_to='profesores/')
    descripcion_corta = models.TextField(blank=True, null=True)
    orden = models.IntegerField(default=0)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"

    class Meta:
        ordering = ['orden']
        verbose_name = "Profesor Público"
        verbose_name_plural = "Profesores Públicos"


# ==================== ESTUDIANTES ====================

class Estudiante(models.Model):
    """Estudiantes del colegio"""
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    curso = models.CharField(max_length=50)
    paralelo = models.CharField(max_length=10, blank=True, null=True)
    foto = models.ImageField(upload_to='estudiantes/', blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"

    class Meta:
        verbose_name_plural = "Estudiantes"


# ==================== MATERIAS ====================

class Materia(models.Model):
    """Materias/Asignaturas dictadas"""
    ESTADO_CHOICES = [
        ('borrador', 'Borrador'),
        ('publicada', 'Publicada'),
    ]

    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    curso = models.CharField(max_length=50, help_text="Ej: 1° Secundaria")
    paralelo = models.CharField(max_length=10, help_text="Ej: A, B, C")
    imagen_portada = models.ImageField(upload_to='materias/')
    profesor = models.ForeignKey(ProfesorProfile, on_delete=models.CASCADE, related_name='materias')
    estado_publicacion = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default='borrador'
    )
    color_portada = models.CharField(
        max_length=7,
        default='#3498db',
        help_text="Color hexadecimal para la tarjeta"
    )
    icono = models.CharField(max_length=50, blank=True, null=True, help_text="Ej: fa-calculator")
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_publicacion = models.DateTimeField(blank=True, null=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre} ({self.curso} - {self.paralelo})"

    class Meta:
        ordering = ['-fecha_creacion']
        verbose_name_plural = "Materias"

    def publicar(self):
        """Cambiar estado a publicada"""
        self.estado_publicacion = 'publicada'
        self.fecha_publicacion = timezone.now()
        self.save()

    def despublicar(self):
        """Cambiar estado a borrador"""
        self.estado_publicacion = 'borrador'
        self.save()


# ==================== CONTENIDOS ====================

class Contenido(models.Model):
    """Contenidos/Unidades dentro de una materia"""
    ESTADO_CHOICES = [
        ('privado', 'Privado'),
        ('publico', 'Público'),
    ]

    materia = models.ForeignKey(Materia, on_delete=models.CASCADE, related_name='contenidos')
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    imagen_principal = models.ImageField(upload_to='contenidos/', blank=True, null=True)
    archivo_pdf = models.FileField(upload_to='contenidos/pdf/', blank=True, null=True)
    archivo_video = models.FileField(upload_to='contenidos/videos/', blank=True, null=True)
    link_video = models.URLField(blank=True, null=True, help_text="Enlace de YouTube o similar")
    estado_publicacion = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default='privado'
    )
    orden = models.IntegerField(default=0)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_publicacion = models.DateTimeField(blank=True, null=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.titulo} - {self.materia.nombre}"

    class Meta:
        ordering = ['orden', 'fecha_creacion']
        verbose_name_plural = "Contenidos"

    def publicar(self):
        """Cambiar estado a público"""
        self.estado_publicacion = 'publico'
        self.fecha_publicacion = timezone.now()
        self.save()

    def despublicar(self):
        """Cambiar estado a privado"""
        self.estado_publicacion = 'privado'
        self.save()


class ImagenContenido(models.Model):
    """Galerías de imágenes para los contenidos"""
    contenido = models.ForeignKey(Contenido, on_delete=models.CASCADE, related_name='galeria')
    imagen = models.ImageField(upload_to='contenidos/galeria/')
    titulo = models.CharField(max_length=200, blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    orden = models.IntegerField(default=0)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Imagen - {self.contenido.titulo}"

    class Meta:
        ordering = ['orden']
        verbose_name = "Imagen Contenido"
        verbose_name_plural = "Imágenes Contenido"


# ==================== INFORMACIÓN GENERAL ====================

class InformacionColegio(models.Model):
    """Información de contacto del colegio"""
    nombre = models.CharField(max_length=200)
    direccion = models.CharField(max_length=300)
    correo_institucional = models.EmailField()
    telefono_1 = models.CharField(max_length=20)
    telefono_2 = models.CharField(max_length=20, blank=True, null=True)
    horario_inicio = models.TimeField()
    horario_fin = models.TimeField()
    latitud = models.FloatField(help_text="Para Google Maps")
    longitud = models.FloatField(help_text="Para Google Maps")
    facebook_url = models.URLField(blank=True, null=True)
    instagram_url = models.URLField(blank=True, null=True)
    tiktok_url = models.URLField(blank=True, null=True)
    logo = models.ImageField(upload_to='colegio/', blank=True, null=True)
    favicon = models.ImageField(upload_to='colegio/', blank=True, null=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Información del Colegio"
        verbose_name_plural = "Información del Colegio"


# ==================== NOTICIAS/AVISOS ====================

class Noticia(models.Model):
    """Noticias, eventos y avisos del colegio"""
    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    imagen = models.ImageField(upload_to='noticias/')
    fecha_evento = models.DateTimeField(blank=True, null=True)
    destacada = models.BooleanField(default=False)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.titulo

    class Meta:
        ordering = ['-fecha_creacion']
        verbose_name_plural = "Noticias"


# ==================== GALERÍA ====================

class GaleriaImagenes(models.Model):
    """Galería general de imágenes del colegio"""
    titulo = models.CharField(max_length=200)
    imagen = models.ImageField(upload_to='galeria/')
    descripcion = models.TextField(blank=True, null=True)
    categoria = models.CharField(
        max_length=50,
        default='general',
        help_text="Categoría para filtrar imágenes"
    )
    orden = models.IntegerField(default=0)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo

    class Meta:
        ordering = ['orden']
        verbose_name = "Imagen Galería"
        verbose_name_plural = "Imágenes Galería"
