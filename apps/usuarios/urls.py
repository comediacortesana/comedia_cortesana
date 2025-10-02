from django.urls import path
from . import views

app_name = 'usuarios'

urlpatterns = [
    # Vistas web
    path('login/', views.LoginView.as_view(), name='login'),
    path('registro/', views.RegistroView.as_view(), name='registro'),
    path('logout/', views.logout_view, name='logout'),
    path('perfil/', views.perfil_view, name='perfil'),
    
    # API endpoints
    path('api/registro/', views.api_registro, name='api_registro'),
    path('api/login/', views.api_login, name='api_login'),
    path('api/logout/', views.api_logout, name='api_logout'),
    path('api/perfil/', views.api_perfil, name='api_perfil'),
    path('api/cambio-password/', views.api_cambio_password, name='api_cambio_password'),
    path('api/sesiones/', views.api_sesiones, name='api_sesiones'),
]
