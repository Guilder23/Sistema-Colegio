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

