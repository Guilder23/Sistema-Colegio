from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # Páginas públicas
    path('', views.IndexView.as_view(), name='index'),
    path('home/', views.IndexView.as_view(), name='home'),
    path('historia/', views.HistoriaView.as_view(), name='historia'),
    path('mision-vision/', views.MisionVisionView.as_view(), name='mision_vision'),
    path('autoridades/', views.AutoridadesView.as_view(), name='autoridades'),
    path('contacto/', views.ContactoView.as_view(), name='contacto'),
    path('materias/', views.MateriasListView.as_view(), name='materias'),
    
    # Autenticación
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('registro/', views.RegistroView.as_view(), name='registro'),
    
    # Panel de usuario
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('materias-gestion/', views.MateriasGestionView.as_view(), name='materias_gestion'),
    path('contenidos-gestion/', views.ContenidosGestionView.as_view(), name='contenidos_gestion'),
    
    # CRUD Materias
    path('materia/crear/', views.MateriaCreateView.as_view(), name='materia_create'),
    path('materia/<int:pk>/editar/', views.MateriaUpdateView.as_view(), name='materia_update'),
    path('materia/<int:pk>/eliminar/', views.MateriaDeleteView.as_view(), name='materia_delete'),
    path('materia/<int:pk>/detalle/', views.MateriaDetailView.as_view(), name='materia_detail'),
    
    # CRUD Contenidos
    path('contenido/crear/', views.ContenidoCreateView.as_view(), name='contenido_create'),
    path('contenido/<int:pk>/editar/', views.ContenidoUpdateView.as_view(), name='contenido_update'),
    path('contenido/<int:pk>/eliminar/', views.ContenidoDeleteView.as_view(), name='contenido_delete'),
    path('contenido/<int:pk>/detalle/', views.ContenidoDetailView.as_view(), name='contenido_detail'),
]
