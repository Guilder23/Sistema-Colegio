from django.urls import path
from . import views

urlpatterns = [
    # ==================== PÚBLICAS ====================
    path('', views.HomeView.as_view(), name='home'),
    path('historia/', views.HistoriaView.as_view(), name='historia'),
    path('mision-vision/', views.MisionVisionView.as_view(), name='mision_vision'),
    path('autoridades/', views.AutoridadesView.as_view(), name='autoridades'),
    path('materias/', views.MateriasPublicasView.as_view(), name='materias'),
    path('materia/<int:pk>/', views.MateriaDetailView.as_view(), name='materia_detail'),
    path('contenido/<int:pk>/', views.ContenidoDetailView.as_view(), name='contenido_detail'),
    
    # ==================== AUTENTICACIÓN ====================
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('registro/', views.RegistroView.as_view(), name='registro'),
    
    # ==================== DASHBOARD ====================
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('materias-gestion/', views.MateriasGestionView.as_view(), name='materias_gestion'),
    path('materia/crear/', views.MateriaCreateView.as_view(), name='materia_create'),
    path('materia/<int:pk>/editar/', views.MateriaUpdateView.as_view(), name='materia_update'),
    path('materia/<int:pk>/eliminar/', views.MateriaDeleteView.as_view(), name='materia_delete'),
    
    path('contenidos-gestion/', views.ContenidosGestionView.as_view(), name='contenidos_gestion'),
    path('contenido/crear/', views.ContenidoCreateView.as_view(), name='contenido_create'),
    path('contenido/<int:pk>/editar/', views.ContenidoUpdateView.as_view(), name='contenido_update'),
    path('contenido/<int:pk>/eliminar/', views.ContenidoDeleteView.as_view(), name='contenido_delete'),
]
