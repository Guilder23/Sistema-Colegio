import json
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.conf import settings
from django.core.paginator import Paginator
from .models import ProfesorProfile, Materia, Contenido, ImagenContenido


# ==================== VISTAS PÚBLICAS ====================

class HomeView(View):
    """Página principal del sitio público"""
    def get(self, request):
        # Cargar datos estáticos
        try:
            with open(settings.STATIC_ROOT / 'data' / 'escuela.json', 'r', encoding='utf-8') as f:
                escuela = json.load(f)
        except:
            escuela = {'nombre': 'Colegio Tecnológico', 'contacto': {}}
        
        materias_publicadas = Materia.objects.filter(
            estado_publicacion='publicada',
            activo=True
        ).order_by('-fecha_publicacion')[:6]
        
        contexto = {
            'escuela': escuela,
            'materias_destacadas': materias_publicadas,
        }
        return render(request, 'core/home.html', contexto)


class HistoriaView(View):
    """Página de historia del colegio (estática)"""
    def get(self, request):
        try:
            with open(settings.STATIC_ROOT / 'data' / 'historia.json', 'r', encoding='utf-8') as f:
                historia = json.load(f)
        except:
            historia = {}
        
        return render(request, 'core/historia.html', {'historia': historia})


class MisionVisionView(View):
    """Página de misión y visión (estática)"""
    def get(self, request):
        try:
            with open(settings.STATIC_ROOT / 'data' / 'mision_vision.json', 'r', encoding='utf-8') as f:
                datos = json.load(f)
        except:
            datos = {}
        
        return render(request, 'core/mision_vision.html', datos)


class AutoridadesView(View):
    """Página de autoridades (estática)"""
    def get(self, request):
        try:
            with open(settings.STATIC_ROOT / 'data' / 'autoridades.json', 'r', encoding='utf-8') as f:
                datos = json.load(f)
        except:
            datos = {'autoridades': []}
        
        return render(request, 'core/autoridades.html', datos)


class MateriasPublicasView(ListView):
    """Listado de materias publicadas"""
    model = Materia
    template_name = 'core/materias.html'
    context_object_name = 'materias'
    paginate_by = 12
    
    def get_queryset(self):
        return Materia.objects.filter(
            estado_publicacion='publicada',
            activo=True
        ).select_related('profesor').order_by('-fecha_publicacion')


class MateriaDetailView(DetailView):
    """Detalle de una materia con sus contenidos"""
    model = Materia
    template_name = 'core/materia_detail.html'
    context_object_name = 'materia'
    
    def get_queryset(self):
        return Materia.objects.filter(
            estado_publicacion='publicada',
            activo=True
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contenidos'] = self.object.contenidos.filter(
            estado_publicacion='publico',
            activo=True
        ).order_by('orden')
        return context


class ContenidoDetailView(DetailView):
    """Detalle de un contenido con galerías"""
    model = Contenido
    template_name = 'core/contenido_detail.html'
    context_object_name = 'contenido'
    
    def get_queryset(self):
        return Contenido.objects.filter(
            estado_publicacion='publico',
            activo=True
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['galeria'] = self.object.galeria.all().order_by('orden')
        return context


# ==================== AUTENTICACIÓN ====================

class LoginView(View):
    """Login de profesores"""
    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(email=email)
            user = authenticate(request, username=user.username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'¡Bienvenido {user.first_name}!')
                return redirect('dashboard')
            else:
                messages.error(request, 'Contraseña incorrecta')
        except User.DoesNotExist:
            messages.error(request, 'Usuario no encontrado')
        
        return redirect('home')


class LogoutView(View):
    """Logout de profesores"""
    def get(self, request):
        logout(request)
        messages.success(request, 'Sesión cerrada correctamente')
        return redirect('home')


class RegistroView(View):
    """Registro de nuevos profesores"""
    def post(self, request):
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        especialidad = request.POST.get('especialidad', '')
        
        try:
            if User.objects.filter(email=email).exists():
                messages.error(request, 'El correo ya está registrado')
            elif User.objects.filter(username=email).exists():
                messages.error(request, 'El usuario ya existe')
            else:
                user = User.objects.create_user(
                    username=email,
                    email=email,
                    password=password,
                    first_name=first_name,
                    last_name=last_name
                )
                ProfesorProfile.objects.create(
                    user=user,
                    especialidad=especialidad
                )
                login(request, user)
                messages.success(request, '¡Registro exitoso! Bienvenido')
                return redirect('dashboard')
        except Exception as e:
            messages.error(request, f'Error en el registro: {str(e)}')
        
        return redirect('home')


# ==================== DASHBOARD ====================

class DashboardView(LoginRequiredMixin, View):
    """Panel principal del profesor"""
    def get(self, request):
        try:
            profesor = request.user.profesor_profile
        except:
            profesor = None
        
        if not profesor:
            messages.error(request, 'Debes completar tu perfil de profesor')
            return redirect('home')
        
        materias = profesor.materias.all()
        total_contenidos = Contenido.objects.filter(materia__profesor=profesor).count()
        
        contexto = {
            'profesor': profesor,
            'materias': materias,
            'total_materias': materias.count(),
            'total_contenidos': total_contenidos,
            'materias_publicadas': materias.filter(estado_publicacion='publicada').count(),
        }
        return render(request, 'dashboard/dashboard.html', contexto)


# ==================== MATERIAS - CRUD ====================

class MateriasGestionView(LoginRequiredMixin, View):
    """Listado de materias del profesor para gestionar"""
    def get(self, request):
        profesor = get_object_or_404(ProfesorProfile, user=request.user)
        materias = profesor.materias.all().order_by('-fecha_creacion')
        
        paginator = Paginator(materias, 10)
        page_number = request.GET.get('page')
        materias = paginator.get_page(page_number)
        
        return render(request, 'dashboard/materias_gestion.html', {'materias': materias})


class MateriaCreateView(LoginRequiredMixin, CreateView):
    """Crear nueva materia"""
    model = Materia
    template_name = 'dashboard/materia_form.html'
    fields = ['nombre', 'descripcion', 'curso', 'paralelo', 'imagen_portada', 'color_portada', 'icono']
    success_url = reverse_lazy('materias_gestion')
    
    def form_valid(self, form):
        profesor = get_object_or_404(ProfesorProfile, user=self.request.user)
        form.instance.profesor = profesor
        messages.success(self.request, 'Materia creada exitosamente')
        return super().form_valid(form)


class MateriaUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Editar materia"""
    model = Materia
    template_name = 'dashboard/materia_form.html'
    fields = ['nombre', 'descripcion', 'curso', 'paralelo', 'imagen_portada', 'color_portada', 'icono', 'estado_publicacion', 'activo']
    success_url = reverse_lazy('materias_gestion')
    
    def test_func(self):
        materia = self.get_object()
        return materia.profesor.user == self.request.user
    
    def form_valid(self, form):
        messages.success(self.request, 'Materia actualizada exitosamente')
        return super().form_valid(form)


class MateriaDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Eliminar (desactivar) materia"""
    model = Materia
    success_url = reverse_lazy('materias_gestion')
    
    def test_func(self):
        materia = self.get_object()
        return materia.profesor.user == self.request.user
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.activo = False
        self.object.save()
        messages.success(request, 'Materia desactivada')
        return redirect(self.success_url)


# ==================== CONTENIDOS - CRUD ====================

class ContenidosGestionView(LoginRequiredMixin, View):
    """Listado de contenidos para gestionar"""
    def get(self, request):
        profesor = get_object_or_404(ProfesorProfile, user=request.user)
        contenidos = Contenido.objects.filter(materia__profesor=profesor).order_by('-fecha_creacion')
        
        paginator = Paginator(contenidos, 10)
        page_number = request.GET.get('page')
        contenidos = paginator.get_page(page_number)
        
        return render(request, 'dashboard/contenidos_gestion.html', {'contenidos': contenidos})


class ContenidoCreateView(LoginRequiredMixin, CreateView):
    """Crear nuevo contenido"""
    model = Contenido
    template_name = 'dashboard/contenido_form.html'
    fields = ['materia', 'titulo', 'descripcion', 'imagen_principal', 'archivo_pdf', 'link_video', 'orden']
    success_url = reverse_lazy('contenidos_gestion')
    
    def form_valid(self, form):
        profesor = get_object_or_404(ProfesorProfile, user=self.request.user)
        materia = form.cleaned_data['materia']
        
        if materia.profesor.user != self.request.user:
            messages.error(self.request, 'No tienes permisos para agregar contenido a esta materia')
            return self.form_invalid(form)
        
        messages.success(self.request, 'Contenido creado exitosamente')
        return super().form_valid(form)


class ContenidoUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Editar contenido"""
    model = Contenido
    template_name = 'dashboard/contenido_form.html'
    fields = ['titulo', 'descripcion', 'imagen_principal', 'archivo_pdf', 'link_video', 'estado_publicacion', 'orden', 'activo']
    success_url = reverse_lazy('contenidos_gestion')
    
    def test_func(self):
        contenido = self.get_object()
        return contenido.materia.profesor.user == self.request.user
    
    def form_valid(self, form):
        messages.success(self.request, 'Contenido actualizado exitosamente')
        return super().form_valid(form)


class ContenidoDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Eliminar (desactivar) contenido"""
    model = Contenido
    success_url = reverse_lazy('contenidos_gestion')
    
    def test_func(self):
        contenido = self.get_object()
        return contenido.materia.profesor.user == self.request.user
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.activo = False
        self.object.save()
        messages.success(request, 'Contenido desactivado')
        return redirect(self.success_url)
