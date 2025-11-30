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
from django.db.models import Count
from django.contrib.auth import authenticate, login, logout
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
        profesor_profile, _ = ProfesorProfile.objects.get_or_create(user=self.request.user)
        
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
        context['director'] = {
            'nombre': 'Dr. Juan Pérez García',
            'cargo': 'Rector',
            'email': 'rector@colegio.edu',
            'telefono': '5551234567'
        }
        context['secretaria'] = {
            'nombre': 'Lic. María Rodríguez López',
            'cargo': 'Secretaría Académica',
            'email': 'secretaria@colegio.edu',
            'telefono': '5559876543'
        }
        context['profesores'] = (
            ProfesorProfile.objects
            .annotate(materias_count=Count('materia'))
            .select_related('user')
            .order_by('-materias_count', 'user__first_name')
        )
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
    template_name = 'secciones_estaticas/materias_publicas.html'
    
    def get_context_data(self, **kwargs):
        import json
        from datetime import datetime
        
        context = super().get_context_data(**kwargs)
        context['show_sidebar'] = False
        materias = Materia.objects.filter(estado_publicacion='publicada').select_related('profesor')
        context['materias'] = materias
        
        # Preparar contenidos para cada materia
        contenidos_por_materia = {}
        for materia in materias:
            contenidos = Contenido.objects.filter(
                materia=materia,
                estado_publicacion='publico'
            ).order_by('-fecha_creacion')
            
            contenidos_por_materia[materia.id] = json.dumps([{
                'titulo': contenido.titulo,
                'descripcion': contenido.descripcion[:150] + '...' if len(contenido.descripcion) > 150 else contenido.descripcion,
                'tipo': contenido.tipo,
                'fecha': contenido.fecha_creacion.strftime('%d/%m/%Y'),
                'tiene_archivo': bool(contenido.archivo),
                'archivo_url': contenido.archivo.url if contenido.archivo else '#'
            } for contenido in contenidos])
        
        context['contenidos_por_materia'] = contenidos_por_materia
        return context


class MateriasGestionView(LoginRequiredMixin, TemplateView):
    """Vista para gestionar materias del usuario"""
    template_name = 'materias/lista.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['show_sidebar'] = True
        profesor_profile, _ = ProfesorProfile.objects.get_or_create(user=self.request.user)
        context['materias'] = Materia.objects.filter(profesor=profesor_profile)
        return context


class ContenidosGestionView(LoginRequiredMixin, TemplateView):
    """Vista para gestionar contenidos"""
    template_name = 'contenidos/lista.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['show_sidebar'] = True
        profesor_profile, _ = ProfesorProfile.objects.get_or_create(user=self.request.user)
        context['contenidos'] = Contenido.objects.filter(materia__profesor=profesor_profile).select_related('materia')
        context['materias'] = Materia.objects.filter(profesor=profesor_profile)
        return context


class CustomLoginView(LoginView):
    """Vista personalizada de login"""
    template_name = 'secciones_estaticas/inicio.html'
    next_page = 'core:dashboard'
    redirect_authenticated_user = True
    
    def form_valid(self, form):
        messages.success(self.request, f'✓ Bienvenido {form.get_user().first_name or form.get_user().username}!')
        response = super().form_valid(form)
        # Usar redirect para evitar el modal de confirmación de reenvío de formulario
        return redirect(self.next_page)
    
    def form_invalid(self, form):
        """Mostrar mensaje de error cuando las credenciales son incorrectas"""
        messages.error(self.request, 'Usuario o contraseña incorrectos. Verifique sus datos e intente de nuevo.')
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        """Agregar el form al contexto para mostrar en el modal"""
        context = super().get_context_data(**kwargs)
        context['show_sidebar'] = False
        return context


class CustomLogoutView(LogoutView):
    """Vista personalizada de logout"""
    next_page = 'core:index'
    template_name = 'registration/logged_out.html'
    http_method_names = ['get', 'post', 'options']
    
    def get(self, request, *args, **kwargs):
        """Permite logout mediante GET"""
        messages.success(request, '✓ Sesión cerrada exitosamente')
        logout(request)
        return redirect(self.next_page)


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
            # Usar redirect para evitar el modal de confirmación de reenvío de formulario
            return redirect(self.success_url)
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
            if 'foto' in request.FILES:
                materia.foto = request.FILES['foto']
                materia.save()
            messages.success(request, f'✓ Materia "{materia.nombre}" creada exitosamente')
            return JsonResponse({'id': materia.id, 'success': True})
        except Exception as e:
            messages.error(request, f'✗ Error al crear materia: {str(e)}')
            return JsonResponse({'error': str(e)}, status=400)


class MateriaUpdateView(LoginRequiredMixin, View):
    """Vista para actualizar materias"""
    login_url = 'core:login'
    
    def post(self, request, pk):
        try:
            materia = Materia.objects.get(pk=pk)
            nombre_anterior = materia.nombre
            materia.nombre = request.POST.get('nombre', materia.nombre)
            materia.descripcion = request.POST.get('descripcion', materia.descripcion)
            materia.estado_publicacion = request.POST.get('estado_publicacion', materia.estado_publicacion)
            if 'foto' in request.FILES:
                materia.foto = request.FILES['foto']
            materia.save()
            messages.success(request, f'✓ Materia "{materia.nombre}" actualizada exitosamente')
            return JsonResponse({'success': True})
        except Exception as e:
            messages.error(request, f'✗ Error al actualizar materia: {str(e)}')
            return JsonResponse({'error': str(e)}, status=400)


class MateriaDeleteView(LoginRequiredMixin, View):
    """Vista para eliminar materias"""
    login_url = 'core:login'
    
    def post(self, request, pk):
        try:
            materia = Materia.objects.get(pk=pk)
            nombre_materia = materia.nombre
            materia.delete()
            messages.success(request, f'✓ Materia "{nombre_materia}" eliminada exitosamente')
            return JsonResponse({'success': True})
        except Exception as e:
            messages.error(request, f'✗ Error al eliminar materia: {str(e)}')
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
                'estado_publicacion': materia.estado_publicacion,
                'foto_url': materia.foto.url if materia.foto else None
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
            messages.success(request, f'✓ Contenido "{contenido.titulo}" creado exitosamente')
            return JsonResponse({'id': contenido.id, 'success': True})
        except Exception as e:
            messages.error(request, f'✗ Error al crear contenido: {str(e)}')
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
            messages.success(request, f'✓ Contenido "{contenido.titulo}" actualizado exitosamente')
            return JsonResponse({'success': True})
        except Exception as e:
            messages.error(request, f'✗ Error al actualizar contenido: {str(e)}')
            return JsonResponse({'error': str(e)}, status=400)


class ContenidoDeleteView(LoginRequiredMixin, View):
    """Vista para eliminar contenidos"""
    login_url = 'core:login'
    
    def post(self, request, pk):
        try:
            contenido = Contenido.objects.get(pk=pk)
            titulo_contenido = contenido.titulo
            contenido.delete()
            messages.success(request, f'✓ Contenido "{titulo_contenido}" eliminado exitosamente')
            return JsonResponse({'success': True})
        except Exception as e:
            messages.error(request, f'✗ Error al eliminar contenido: {str(e)}')
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
