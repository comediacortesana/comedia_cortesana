from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages
from .models import SesionUsuario
import logging

logger = logging.getLogger(__name__)


class AutenticacionMiddleware(MiddlewareMixin):
    """
    Middleware personalizado para manejar autenticación y sesiones
    """
    
    def process_request(self, request):
        """
        Procesa cada request para verificar autenticación
        """
        # Rutas que no requieren autenticación
        rutas_publicas = [
            '/',
            '/usuarios/login/',
            '/usuarios/registro/',
            '/admin/',
            '/api/usuarios/registro/',
            '/api/usuarios/login/',
        ]
        
        # Rutas de API que requieren autenticación
        rutas_api_protegidas = [
            '/api/obras/',
            '/api/autores/',
            '/api/lugares/',
            '/api/representaciones/',
            '/api/bibliografia/',
        ]
        
        # Verificar si la ruta actual requiere autenticación
        ruta_actual = request.path_info
        
        # Si es una ruta pública, permitir acceso
        if any(ruta_actual.startswith(ruta) for ruta in rutas_publicas):
            return None
        
        # Si es una ruta de API protegida, verificar autenticación
        if any(ruta_actual.startswith(ruta) for ruta in rutas_api_protegidas):
            if not request.user.is_authenticated:
                # Para API, devolver JSON error
                if request.path_info.startswith('/api/'):
                    from django.http import JsonResponse
                    return JsonResponse({
                        'error': 'Autenticación requerida',
                        'detail': 'Debe iniciar sesión para acceder a este recurso'
                    }, status=401)
                else:
                    # Para vistas web, redirigir al login
                    return redirect(f"{reverse('usuarios:login')}?next={ruta_actual}")
        
        # Para otras rutas, verificar autenticación básica
        if not request.user.is_authenticated and not ruta_actual.startswith('/static/'):
            return redirect(f"{reverse('usuarios:login')}?next={ruta_actual}")
        
        return None
    
    def process_response(self, request, response):
        """
        Procesa la respuesta para registrar actividad de sesión
        """
        if request.user.is_authenticated:
            try:
                # Actualizar última actividad de sesión
                sesion = SesionUsuario.objects.filter(
                    usuario=request.user,
                    activa=True
                ).first()
                
                if sesion:
                    sesion.save()  # Esto actualiza fecha_ultima_actividad
                    
            except Exception as e:
                logger.error(f"Error actualizando sesión: {e}")
        
        return response


class SesionMiddleware(MiddlewareMixin):
    """
    Middleware para manejar sesiones de usuario
    """
    
    def process_request(self, request):
        """
        Registra nueva sesión si el usuario está autenticado
        """
        if request.user.is_authenticated:
            try:
                # Verificar si ya existe una sesión activa
                sesion_existente = SesionUsuario.objects.filter(
                    usuario=request.user,
                    ip_address=self._get_client_ip(request),
                    activa=True
                ).first()
                
                if not sesion_existente:
                    # Crear nueva sesión
                    SesionUsuario.objects.create(
                        usuario=request.user,
                        ip_address=self._get_client_ip(request),
                        user_agent=request.META.get('HTTP_USER_AGENT', ''),
                    )
                    
            except Exception as e:
                logger.error(f"Error creando sesión: {e}")
    
    def _get_client_ip(self, request):
        """
        Obtiene la IP del cliente
        """
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class TimeoutMiddleware(MiddlewareMixin):
    """
    Middleware para manejar timeout de sesiones
    """
    
    def process_request(self, request):
        """
        Verifica si la sesión ha expirado
        """
        if request.user.is_authenticated:
            try:
                # Marcar sesiones inactivas (más de 24 horas sin actividad)
                from django.utils import timezone
                from datetime import timedelta
                
                tiempo_limite = timezone.now() - timedelta(hours=24)
                
                SesionUsuario.objects.filter(
                    usuario=request.user,
                    fecha_ultima_actividad__lt=tiempo_limite,
                    activa=True
                ).update(activa=False)
                
                # Si no hay sesiones activas, cerrar sesión
                sesiones_activas = SesionUsuario.objects.filter(
                    usuario=request.user,
                    activa=True
                ).exists()
                
                if not sesiones_activas:
                    logout(request)
                    messages.warning(request, 'Su sesión ha expirado. Por favor, inicie sesión nuevamente.')
                    return redirect('usuarios:login')
                    
            except Exception as e:
                logger.error(f"Error verificando timeout de sesión: {e}")
        
        return None
