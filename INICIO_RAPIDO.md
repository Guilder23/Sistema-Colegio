# 🚀 Guía de Inicio Rápido - Sistema de Colegio

## Primer Inicio

1. **Abrir terminal en el directorio del proyecto**
   ```
   cd C:\Users\GUILDER\Desktop\PTRABAJO\SistemaColegio
   ```

2. **Iniciar el servidor de desarrollo**
   ```
   python manage.py runserver
   ```

3. **Acceder a la aplicación**
   - Sitio público: http://localhost:8000/
   - Panel admin: http://localhost:8000/admin/

## 🔑 Credenciales por Defecto

| Campo | Valor |
|-------|-------|
| Usuario | admin |
| Contraseña | admin123 |

## 📋 Checklist de Configuración Inicial

### En Django Admin (http://localhost:8000/admin/)

1. ✅ Inicia sesión con admin/admin123

2. ✅ **Crea Información del Colegio**
   - Ve a "Información del Colegio"
   - Completa campos como:
     - Nombre del colegio
     - Dirección
     - Teléfono y correo
     - Coordenadas para Google Maps (Ej: -12.123456, -76.123456)
     - Enlaces a redes sociales

3. ✅ **Crea Misión y Visión**
   - Ve a "Misiones" y "Visiones"
   - Agrega contenido para cada una

4. ✅ **Crea Autoridades**
   - Ve a "Autoridades"
   - Crea directores, coordinadores, etc.

5. ✅ **Crea Profesores Públicos**
   - Ve a "Profesores Públicos"
   - Agrega presentación de los profesores

6. ✅ **Crea un Profesor (Usuario con Login)**
   - Ve a "Perfiles Profesores"
   - Crea un nuevo usuario primero en "Usuarios"
   - Luego crea su ProfesorProfile

## 🎓 Crear Primer Profesor y Materia

### Opción 1: Por Django Admin

1. Ve a "Usuarios" → "Agregar Usuario"
   - Username: profesor1
   - Password: profesor123
   - First name: Juan
   - Last name: García

2. Ve a "Perfiles Profesores" → "Agregar Perfil Profesor"
   - Selecciona al usuario
   - Completa especialidad (Ej: Matemáticas)

3. Ve a "Materias" → "Agregar Materia"
   - Nombre: Álgebra
   - Descripción: Curso de álgebra básica
   - Curso: 1° Secundaria
   - Paralelo: A
   - Sube imagen de portada
   - Selecciona el profesor
   - Estado: Borrador

4. Publícalo cambiando el estado a "Publicada"

### Opción 2: Por Panel del Profesor

1. Accede a http://localhost:8000/ sin estar logeado
2. Haz clic en "Iniciar Sesión"
3. Selecciona "Regístrate aquí"
4. Completa el formulario de registro
5. Inicia sesión
6. Ve a tu Dashboard
7. Crea materias y contenidos

## 📸 Crear Contenido con Imágenes

1. En el Dashboard → "Crear Contenido"
2. Selecciona una materia
3. Completa los campos
4. Sube imagen principal (opcional)
5. Puedes agregar:
   - Enlace de video (YouTube)
   - Archivo PDF
   - Archivo de video

6. En Django Admin → Ve a "Imágenes Contenido" para agregar galerías

## 🔍 Rutas Principales

| Ruta | Descripción |
|------|-------------|
| / | Página principal |
| /materias/ | Listado de materias |
| /materia/1/ | Detalle de materia |
| /contenido/1/ | Detalle de contenido |
| /historia/ | Historia del colegio |
| /mision-vision/ | Misión y Visión |
| /autoridades/ | Autoridades |
| /profesores/ | Profesores públicos |
| /login/ | Iniciar sesión (modal) |
| /dashboard/ | Panel del profesor |
| /materias-gestion/ | Gestionar materias |
| /contenidos-gestion/ | Gestionar contenidos |
| /admin/ | Panel administrador Django |

## 🎨 Personalización Rápida

### Cambiar Colores
Edita `static/css/style.css`:
```css
:root {
    --primary-color: #667eea;      /* Azul */
    --secondary-color: #764ba2;    /* Púrpura */
    /* ... */
}
```

### Cambiar Logo
- Sube el logo en Django Admin → Información del Colegio

### Cambiar Redes Sociales
- Edita los URLs en Django Admin → Información del Colegio

## 🐛 Si Algo No Funciona

### Error de migraciones
```bash
python manage.py migrate --run-syncdb
```

### Borrar base de datos y empezar de nuevo
```bash
# Eliminar db.sqlite3
# Luego:
python manage.py migrate
python manage.py createsuperuser
```

### Las imágenes no se ven
1. Verifica DEBUG=True en settings.py
2. Recarga con Ctrl+F5
3. Verifica que la carpeta media/ existe

## 📞 Soporte

Para preguntas sobre Django:
- https://docs.djangoproject.com/
- https://stackoverflow.com/questions/tagged/django

---

**¡Listo!** Tu sistema de colegio está configurado. 🎉
