from django.db import models
from django.contrib.auth.models import User


# ==================== PROFESOR ====================

class ProfesorProfile(models.Model):
    """Perfil del profesor"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profesor_profile')
    especialidad = models.CharField(max_length=100, blank=True)
    biografia = models.TextField(blank=True)
    foto = models.ImageField(upload_to='profesores/', blank=True, null=True)
    activo = models.BooleanField(default=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.username

    class Meta:
        verbose_name = "Perfil Profesor"
        verbose_name_plural = "Perfiles Profesores"


# ==================== MATERIA ====================

class Materia(models.Model):
    """Materias/Asignaturas"""
    ESTADO_CHOICES = [
        ('borrador', 'Borrador'),
        ('publicada', 'Publicada'),
    ]

    profesor = models.ForeignKey(ProfesorProfile, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    estado_publicacion = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='borrador')
    foto = models.ImageField(upload_to='materias/fotos/', blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ['-fecha_creacion']


# ==================== CONTENIDO ====================

class Contenido(models.Model):
    """Contenidos de una materia"""
    TIPO_CHOICES = [
        ('texto', 'Texto'),
        ('video', 'Video'),
        ('documento', 'Documento'),
        ('imagen', 'Imagen'),
        ('multimedia', 'Multimedia'),
    ]
    
    ESTADO_CHOICES = [
        ('privado', 'Privado'),
        ('publico', 'Público'),
    ]

    materia = models.ForeignKey(Materia, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='texto')
    archivo = models.FileField(upload_to='contenidos/', blank=True, null=True)
    estado_publicacion = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='privado')
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo

    class Meta:
        ordering = ['-fecha_creacion']


# ==================== IMAGEN CONTENIDO ====================

class ImagenContenido(models.Model):
    """Galerías de imágenes"""
    contenido = models.ForeignKey(Contenido, on_delete=models.CASCADE, related_name='imagenes')
    imagen = models.ImageField(upload_to='contenidos/imagenes/')
    titulo = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.titulo or f"Imagen - {self.contenido.titulo}"

    class Meta:
        verbose_name_plural = "Imágenes Contenido"

