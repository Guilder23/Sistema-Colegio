from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import CreateView
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from .models import Materia, Contenido, ProfesorProfile
from django.contrib.auth import authenticate, login
from django.contrib import messages
import json

# Vistas de la app core
class IndexView(TemplateView):
    """Vista para la página de inicio"""
    template_name = 'secciones_estaticas/inicio.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['show_sidebar'] = False
        return context


class DashboardView(LoginRequiredMixin, TemplateView):
    """Vista para el panel de control"""
    template_name = 'dashboard.html'
    login_url = 'core:login'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['show_sidebar'] = True
        
        # Obtener o crear el perfil del profesor
        profesor_profile, _ = ProfesorProfile.objects.get_or_create(
            user=self.request.user,
            defaults={'activo': True}
        )
        
        # Obtener materias y contenidos del usuario
        context['materias'] = Materia.objects.filter(profesor=profesor_profile).order_by('-fecha_creacion')
        context['contenidos'] = Contenido.objects.filter(materia__profesor=profesor_profile).order_by('-fecha_creacion')
        
        return context


class HistoriaView(TemplateView):
    """Vista de la historia"""
    template_name = 'secciones_estaticas/historia.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['show_sidebar'] = False
        return context


class MisionVisionView(TemplateView):
    """Vista de misión y visión"""
    template_name = 'secciones_estaticas/mision.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['show_sidebar'] = False
        return context


class AutoridadesView(TemplateView):
    """Vista de autoridades"""
    template_name = 'secciones_estaticas/autoridades.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['show_sidebar'] = False
        return context


class ContactoView(TemplateView):
    """Vista de contacto"""
    template_name = 'secciones_estaticas/contacto.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['show_sidebar'] = False
        return context


class MateriasListView(TemplateView):
    """Vista para listar materias públicas"""
    template_name = 'materias/lista.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['show_sidebar'] = False
        context['materias'] = Materia.objects.filter(estado_publicacion='publicada').select_related('profesor')
        return context


class MateriasGestionView(LoginRequiredMixin, TemplateView):
    """Vista para gestionar materias del usuario"""
    template_name = 'materias/lista.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['show_sidebar'] = True
        profesor_profile, _ = ProfesorProfile.objects.get_or_create(
            user=self.request.user,
            defaults={'activo': True}
        )
        context['materias'] = Materia.objects.filter(profesor=profesor_profile)
        return context


class ContenidosGestionView(LoginRequiredMixin, TemplateView):
    """Vista para gestionar contenidos"""
    template_name = 'contenidos/lista.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['show_sidebar'] = True
        profesor_profile, _ = ProfesorProfile.objects.get_or_create(
            user=self.request.user,
            defaults={'activo': True}
        )
        context['contenidos'] = Contenido.objects.filter(materia__profesor=profesor_profile).select_related('materia')
        context['materias'] = Materia.objects.filter(profesor=profesor_profile)
        return context


class CustomLoginView(LoginView):
    """Vista personalizada de login"""
    template_name = 'secciones_estaticas/inicio.html'
    next_page = 'core:dashboard'
    redirect_authenticated_user = True


class CustomLogoutView(LogoutView):
    """Vista personalizada de logout"""
    next_page = 'core:index'


class RegistroView(CreateView):
    """Vista para registro de usuarios"""
    model = User
    fields = ['username', 'first_name', 'email', 'password']
    template_name = 'secciones_estaticas/inicio.html'
    success_url = reverse_lazy('core:dashboard')
    
    def form_valid(self, form):
        password = form.cleaned_data.get('password')
        password_confirm = self.request.POST.get('password_confirm')
        if password_confirm != password:
            form.add_error('password', 'Las contraseñas no coinciden')
            return self.form_invalid(form)
        user = form.save(commit=False)
        user.set_password(password)
        user.save()
        user = authenticate(self.request, username=user.username, password=password)
        if user:
            login(self.request, user)
            messages.success(self.request, 'Registro exitoso. Bienvenido!')
        return super().form_valid(form)


# ==================== VISTAS CRUD MATERIAS ====================

class MateriaCreateView(LoginRequiredMixin, View):
    """Vista para crear materias"""
    login_url = 'core:login'
    
    def post(self, request):
        try:
            # Obtener o crear el perfil del profesor
            profesor_profile, _ = ProfesorProfile.objects.get_or_create(
                user=request.user,
                defaults={'activo': True}
            )
            
            materia = Materia.objects.create(
                profesor=profesor_profile,
                nombre=request.POST.get('nombre'),
                descripcion=request.POST.get('descripcion', ''),
                estado_publicacion=request.POST.get('estado_publicacion', 'borrador')
            )
            return JsonResponse({'id': materia.id, 'success': True})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)


class MateriaUpdateView(LoginRequiredMixin, View):
    """Vista para actualizar materias"""
    login_url = 'core:login'
    
    def post(self, request, pk):
        try:
            materia = Materia.objects.get(pk=pk)
            materia.nombre = request.POST.get('nombre', materia.nombre)
            materia.descripcion = request.POST.get('descripcion', materia.descripcion)
            materia.estado_publicacion = request.POST.get('estado_publicacion', materia.estado_publicacion)
            materia.save()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)


class MateriaDeleteView(LoginRequiredMixin, View):
    """Vista para eliminar materias"""
    login_url = 'core:login'
    
    def post(self, request, pk):
        try:
            materia = Materia.objects.get(pk=pk)
            materia.delete()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)


class MateriaDetailView(LoginRequiredMixin, View):
    """Vista para obtener detalles de una materia"""
    login_url = 'core:login'
    
    def get(self, request, pk):
        try:
            materia = Materia.objects.get(pk=pk)
            data = {
                'id': materia.id,
                'nombre': materia.nombre,
                'descripcion': materia.descripcion,
                'estado_publicacion': materia.estado_publicacion
            }
            return JsonResponse(data)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)


# ==================== VISTAS CRUD CONTENIDOS ====================

class ContenidoCreateView(LoginRequiredMixin, View):
    """Vista para crear contenidos"""
    login_url = 'core:login'
    
    def post(self, request):
        try:
            contenido = Contenido.objects.create(
                materia_id=request.POST.get('materia'),
                titulo=request.POST.get('titulo'),
                descripcion=request.POST.get('descripcion', ''),
                tipo=request.POST.get('tipo', 'texto'),
                archivo=request.FILES.get('archivo', None),
                estado_publicacion=request.POST.get('estado_publicacion', 'privado')
            )
            return JsonResponse({'id': contenido.id, 'success': True})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)


class ContenidoUpdateView(LoginRequiredMixin, View):
    """Vista para actualizar contenidos"""
    login_url = 'core:login'
    
    def post(self, request, pk):
        try:
            contenido = Contenido.objects.get(pk=pk)
            contenido.titulo = request.POST.get('titulo', contenido.titulo)
            contenido.descripcion = request.POST.get('descripcion', contenido.descripcion)
            contenido.tipo = request.POST.get('tipo', contenido.tipo)
            contenido.estado_publicacion = request.POST.get('estado_publicacion', contenido.estado_publicacion)
            if 'archivo' in request.FILES:
                contenido.archivo = request.FILES['archivo']
            contenido.save()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)


class ContenidoDeleteView(LoginRequiredMixin, View):
    """Vista para eliminar contenidos"""
    login_url = 'core:login'
    
    def post(self, request, pk):
        try:
            contenido = Contenido.objects.get(pk=pk)
            contenido.delete()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)


class ContenidoDetailView(LoginRequiredMixin, View):
    """Vista para obtener detalles de un contenido"""
    login_url = 'core:login'
    
    def get(self, request, pk):
        try:
            contenido = Contenido.objects.get(pk=pk)
            data = {
                'id': contenido.id,
                'titulo': contenido.titulo,
                'descripcion': contenido.descripcion,
                'tipo': contenido.tipo,
                'estado_publicacion': contenido.estado_publicacion,
                'materia': contenido.materia.id
            }
            return JsonResponse(data)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
