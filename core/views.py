from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.db.models import Q
from django.urls import reverse_lazy
from django.http import JsonResponse
from .models import (
    ProfesorProfile, Historia, Mision, Vision, Autoridad,
    ProfesorPublico, Materia, Contenido, ImagenContenido,
    InformacionColegio, Noticia, GaleriaImagenes
)

# ==================== VISTAS PÚBLICAS ====================

class HomeView(View):
    """Página principal del sitio público"""
    def get(self, request):
        try:
            info_colegio = InformacionColegio.objects.first()
        except:
            info_colegio = None
        
        materias_publicadas = Materia.objects.filter(
            estado_publicacion='publicada',
            activo=True
        )
        noticias = Noticia.objects.filter(activo=True).order_by('-fecha_creacion')[:5]
        galeria = GaleriaImagenes.objects.filter(activo=True).order_by('orden')[:6]
        
        context = {
            'info_colegio': info_colegio,
            'materias': materias_publicadas,
            'noticias': noticias,
            'galeria': galeria,
        }
        return render(request, 'core/home.html', context)


class HistoriaView(View):
    """Página de Historia del colegio"""
    def get(self, request):
        historias = Historia.objects.filter(activo=True).order_by('-fecha_publicacion')
        context = {'historias': historias}
        return render(request, 'core/historia.html', context)


class MisionVisionView(View):
    """Página de Misión y Visión"""
    def get(self, request):
        try:
            mision = Mision.objects.first()
        except:
            mision = None
        try:
            vision = Vision.objects.first()
        except:
            vision = None
        
        context = {'mision': mision, 'vision': vision}
        return render(request, 'core/mision_vision.html', context)


class ProfesoresView(ListView):
    """Lista de Profesores públicos"""
    model = ProfesorPublico
    template_name = 'core/profesores.html'
    context_object_name = 'profesores'
    paginate_by = 12

    def get_queryset(self):
        return ProfesorPublico.objects.filter(activo=True).order_by('orden')


class AutoridadesView(View):
    """Página de Autoridades del colegio"""
    def get(self, request):
        autoridades = Autoridad.objects.filter(activo=True).order_by('orden')
        context = {'autoridades': autoridades}
        return render(request, 'core/autoridades.html', context)


class MateriasPublicasView(ListView):
    """Lista de Materias publicadas"""
    model = Materia
    template_name = 'core/materias.html'
    context_object_name = 'materias'
    paginate_by = 12

    def get_queryset(self):
        return Materia.objects.filter(
            estado_publicacion='publicada',
            activo=True
        ).order_by('-fecha_publicacion')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cursos'] = Materia.objects.filter(
            estado_publicacion='publicada',
            activo=True
        ).values_list('curso', flat=True).distinct()
        return context


class MateriaDetailView(DetailView):
    """Detalle de una Materia"""
    model = Materia
    template_name = 'core/materia_detail.html'
    context_object_name = 'materia'
    slug_field = 'id'
    slug_url_kwarg = 'pk'

    def get_queryset(self):
        return Materia.objects.filter(estado_publicacion='publicada', activo=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contenidos'] = Contenido.objects.filter(
            materia=self.object,
            estado_publicacion='publico',
            activo=True
        ).order_by('orden')
        return context


class ContenidoDetailView(DetailView):
    """Detalle de un Contenido"""
    model = Contenido
    template_name = 'core/contenido_detail.html'
    context_object_name = 'contenido'
    slug_field = 'id'
    slug_url_kwarg = 'pk'

    def get_queryset(self):
        return Contenido.objects.filter(estado_publicacion='publico', activo=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['imagenes'] = ImagenContenido.objects.filter(
            contenido=self.object
        ).order_by('orden')
        return context


# ==================== AUTENTICACIÓN ====================

class LoginView(View):
    """Vista de login del profesor"""
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Verificar si es profesor
            if hasattr(user, 'profesor_profile'):
                login(request, user)
                messages.success(request, f"¡Bienvenido {user.first_name}!")
                return redirect('dashboard')
            else:
                messages.error(request, "Usuario no es profesor registrado")
        else:
            messages.error(request, "Usuario o contraseña incorrectos")
        
        return redirect('home')


class LogoutView(View):
    """Vista de logout"""
    def get(self, request):
        logout(request)
        messages.success(request, "Sesión cerrada correctamente")
        return redirect('home')


class RegistroView(View):
    """Vista de registro de nuevo profesor"""
    def post(self, request):
        nombres = request.POST.get('nombres')
        apellidos = request.POST.get('apellidos')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        especialidad = request.POST.get('especialidad')
        
        # Validaciones
        if password != password_confirm:
            messages.error(request, "Las contraseñas no coinciden")
            return redirect('home')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "El usuario ya existe")
            return redirect('home')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "El email ya está registrado")
            return redirect('home')
        
        # Crear usuario
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=nombres,
            last_name=apellidos
        )
        
        # Crear perfil de profesor
        ProfesorProfile.objects.create(
            user=user,
            especialidad=especialidad
        )
        
        messages.success(request, "Registro exitoso. Por favor, inicia sesión")
        return redirect('home')


# ==================== PANEL DEL PROFESOR ====================

class DashboardView(LoginRequiredMixin, View):
    """Dashboard principal del profesor"""
    login_url = 'home'
    
    def get(self, request):
        try:
            profesor = request.user.profesor_profile
        except:
            return redirect('home')
        
        materias = Materia.objects.filter(profesor=profesor)
        materias_publicadas = materias.filter(estado_publicacion='publicada').count()
        materias_borradores = materias.filter(estado_publicacion='borrador').count()
        total_contenidos = Contenido.objects.filter(materia__profesor=profesor).count()
        
        context = {
            'profesor': profesor,
            'materias': materias,
            'materias_publicadas': materias_publicadas,
            'materias_borradores': materias_borradores,
            'total_contenidos': total_contenidos,
        }
        return render(request, 'dashboard/dashboard.html', context)


class MateriasGestionView(LoginRequiredMixin, ListView):
    """Gestión de materias del profesor"""
    model = Materia
    template_name = 'dashboard/materias_gestion.html'
    context_object_name = 'materias'
    login_url = 'home'

    def get_queryset(self):
        profesor = self.request.user.profesor_profile
        return Materia.objects.filter(profesor=profesor)


class MateriaCreateView(LoginRequiredMixin, CreateView):
    """Crear nueva materia"""
    model = Materia
    template_name = 'dashboard/materia_form.html'
    fields = ['nombre', 'descripcion', 'curso', 'paralelo', 'imagen_portada', 'color_portada', 'icono']
    login_url = 'home'
    success_url = reverse_lazy('materias_gestion')

    def form_valid(self, form):
        form.instance.profesor = self.request.user.profesor_profile
        messages.success(self.request, "Materia creada exitosamente")
        return super().form_valid(form)


class MateriaUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Editar materia"""
    model = Materia
    template_name = 'dashboard/materia_form.html'
    fields = ['nombre', 'descripcion', 'curso', 'paralelo', 'imagen_portada', 'color_portada', 'icono', 'estado_publicacion']
    login_url = 'home'
    success_url = reverse_lazy('materias_gestion')

    def test_func(self):
        materia = self.get_object()
        return self.request.user.profesor_profile == materia.profesor

    def form_valid(self, form):
        messages.success(self.request, "Materia actualizada exitosamente")
        return super().form_valid(form)


class MateriaDeleteView(LoginRequiredMixin, UserPassesTestMixin, View):
    """Desactivar materia"""
    login_url = 'home'

    def test_func(self):
        materia = get_object_or_404(Materia, pk=self.kwargs['pk'])
        return self.request.user.profesor_profile == materia.profesor

    def post(self, request, pk):
        materia = get_object_or_404(Materia, pk=pk)
        if self.test_func():
            materia.activo = False
            materia.save()
            messages.success(request, "Materia desactivada")
            return redirect('materias_gestion')
        return redirect('home')


class ContenidosGestionView(LoginRequiredMixin, ListView):
    """Gestión de contenidos del profesor"""
    model = Contenido
    template_name = 'dashboard/contenidos_gestion.html'
    context_object_name = 'contenidos'
    login_url = 'home'
    paginate_by = 20

    def get_queryset(self):
        profesor = self.request.user.profesor_profile
        return Contenido.objects.filter(materia__profesor=profesor).order_by('-fecha_creacion')


class ContenidoCreateView(LoginRequiredMixin, CreateView):
    """Crear nuevo contenido"""
    model = Contenido
    template_name = 'dashboard/contenido_form.html'
    fields = ['materia', 'titulo', 'descripcion', 'imagen_principal', 'archivo_pdf', 'link_video', 'orden']
    login_url = 'home'
    success_url = reverse_lazy('contenidos_gestion')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        profesor = self.request.user.profesor_profile
        form.fields['materia'].queryset = Materia.objects.filter(profesor=profesor)
        return form

    def form_valid(self, form):
        messages.success(self.request, "Contenido creado exitosamente")
        return super().form_valid(form)


class ContenidoUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Editar contenido"""
    model = Contenido
    template_name = 'dashboard/contenido_form.html'
    fields = ['materia', 'titulo', 'descripcion', 'imagen_principal', 'archivo_pdf', 'link_video', 'estado_publicacion', 'orden']
    login_url = 'home'
    success_url = reverse_lazy('contenidos_gestion')

    def test_func(self):
        contenido = self.get_object()
        return self.request.user.profesor_profile == contenido.materia.profesor

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        profesor = self.request.user.profesor_profile
        form.fields['materia'].queryset = Materia.objects.filter(profesor=profesor)
        return form

    def form_valid(self, form):
        messages.success(self.request, "Contenido actualizado exitosamente")
        return super().form_valid(form)


class ContenidoDeleteView(LoginRequiredMixin, UserPassesTestMixin, View):
    """Desactivar contenido"""
    login_url = 'home'

    def test_func(self):
        contenido = get_object_or_404(Contenido, pk=self.kwargs['pk'])
        return self.request.user.profesor_profile == contenido.materia.profesor

    def post(self, request, pk):
        contenido = get_object_or_404(Contenido, pk=pk)
        if self.test_func():
            contenido.activo = False
            contenido.save()
            messages.success(request, "Contenido desactivado")
            return redirect('contenidos_gestion')
        return redirect('home')
