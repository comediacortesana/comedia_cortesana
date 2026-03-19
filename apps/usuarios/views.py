from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token

from .models import Usuario, PerfilUsuario, SesionUsuario
from .serializers import (
    UsuarioSerializer, PerfilUsuarioSerializer, 
    RegistroSerializer, LoginSerializer, CambioPasswordSerializer
)


class LoginView(TemplateView):
    """
    Vista para el login de usuarios
    """
    template_name = 'usuarios/login.html'
    
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return super().get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        login_field = request.POST.get('login_field')  # Puede ser email o username
        password = request.POST.get('password')
        
        if login_field and password:
            user = authenticate(
                request=request,
                username=login_field.strip(),
                password=password
            )
            
            if user and user.is_active:
                login(request, user)
                
                # Registrar sesión
                self._registrar_sesion(request, user)
                
                # Redirigir según el parámetro next
                next_url = request.GET.get('next', 'home')
                return redirect(next_url)
            else:
                messages.error(request, 'Credenciales inválidas o cuenta desactivada.')
        else:
            messages.error(request, 'Debe proporcionar usuario/email y contraseña.')
        
        return render(request, self.template_name)
    
    def _registrar_sesion(self, request, user):
        """Registra la sesión del usuario"""
        try:
            SesionUsuario.objects.create(
                usuario=user,
                ip_address=self._get_client_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT', ''),
            )
        except Exception:
            pass  # No fallar si no se puede registrar la sesión
    
    def _get_client_ip(self, request):
        """Obtiene la IP del cliente"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class RegistroView(TemplateView):
    """
    Vista para el registro de nuevos usuarios
    """
    template_name = 'usuarios/registro.html'
    
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return super().get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        serializer = RegistroSerializer(data=request.POST)
        
        if serializer.is_valid():
            usuario = serializer.save()
            messages.success(request, 'Usuario registrado exitosamente. Ya puede iniciar sesión.')
            return redirect('usuarios:login')
        else:
            # Mostrar errores del serializer
            for field, errors in serializer.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
        
        return render(request, self.template_name)


@login_required
def logout_view(request):
    """
    Vista para cerrar sesión
    """
    # Marcar sesiones como inactivas
    SesionUsuario.objects.filter(
        usuario=request.user,
        activa=True
    ).update(activa=False)
    
    logout(request)
    messages.success(request, 'Sesión cerrada exitosamente.')
    return redirect('home')


@login_required
def perfil_view(request):
    """
    Vista para mostrar y editar el perfil del usuario
    """
    usuario = request.user
    perfil, created = PerfilUsuario.objects.get_or_create(usuario=usuario)
    
    if request.method == 'POST':
        # Actualizar datos del usuario
        usuario.first_name = request.POST.get('first_name', usuario.first_name)
        usuario.last_name = request.POST.get('last_name', usuario.last_name)
        usuario.email = request.POST.get('email', usuario.email)
        usuario.institucion = request.POST.get('institucion', usuario.institucion)
        usuario.biografia = request.POST.get('biografia', usuario.biografia)
        usuario.save()
        
        # Actualizar perfil
        perfil.especialidades = request.POST.get('especialidades', perfil.especialidades)
        perfil.intereses = request.POST.get('intereses', perfil.intereses)
        perfil.publicaciones = request.POST.get('publicaciones', perfil.publicaciones)
        perfil.perfil_publico = request.POST.get('perfil_publico') == 'on'
        perfil.mostrar_email = request.POST.get('mostrar_email') == 'on'
        perfil.mostrar_institucion = request.POST.get('mostrar_institucion') == 'on'
        perfil.save()
        
        messages.success(request, 'Perfil actualizado exitosamente.')
        return redirect('usuarios:perfil')
    
    context = {
        'usuario': usuario,
        'perfil': perfil,
    }
    return render(request, 'usuarios/perfil.html', context)


# API Views
@api_view(['POST'])
@permission_classes([AllowAny])
def api_registro(request):
    """
    API endpoint para registro de usuarios
    """
    serializer = RegistroSerializer(data=request.data)
    if serializer.is_valid():
        usuario = serializer.save()
        token, created = Token.objects.get_or_create(user=usuario)
        return Response({
            'usuario': UsuarioSerializer(usuario).data,
            'token': token.key,
            'message': 'Usuario registrado exitosamente'
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def api_login(request):
    """
    API endpoint para login de usuarios
    """
    serializer = LoginSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        
        # Registrar sesión
        try:
            SesionUsuario.objects.create(
                usuario=user,
                ip_address=request.META.get('REMOTE_ADDR', ''),
                user_agent=request.META.get('HTTP_USER_AGENT', ''),
            )
        except Exception:
            pass
        
        return Response({
            'usuario': UsuarioSerializer(user).data,
            'token': token.key,
            'message': 'Login exitoso'
        }, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_logout(request):
    """
    API endpoint para logout de usuarios
    """
    # Marcar sesiones como inactivas
    SesionUsuario.objects.filter(
        usuario=request.user,
        activa=True
    ).update(activa=False)
    
    # Eliminar token
    try:
        request.user.auth_token.delete()
    except:
        pass
    
    return Response({'message': 'Logout exitoso'}, status=status.HTTP_200_OK)


@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def api_perfil(request):
    """
    API endpoint para obtener y actualizar perfil de usuario
    """
    if request.method == 'GET':
        serializer = UsuarioSerializer(request.user)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = UsuarioSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_cambio_password(request):
    """
    API endpoint para cambio de contraseña
    """
    serializer = CambioPasswordSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        user = request.user
        user.set_password(serializer.validated_data['password_nueva'])
        user.save()
        return Response({'message': 'Contraseña actualizada exitosamente'})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_sesiones(request):
    """
    API endpoint para obtener sesiones del usuario
    """
    sesiones = SesionUsuario.objects.filter(usuario=request.user).order_by('-fecha_inicio')[:10]
    data = []
    for sesion in sesiones:
        data.append({
            'ip_address': sesion.ip_address,
            'fecha_inicio': sesion.fecha_inicio,
            'fecha_ultima_actividad': sesion.fecha_ultima_actividad,
            'activa': sesion.activa,
        })
    return Response(data)


@csrf_exempt
@require_http_methods(["POST"])
def api_login_session(request):
    """
    Login por sesión Django para el frontend (UI estilo index.html).
    Acepta `login_field` (username o email) y `password`.
    """
    try:
        payload = json.loads(request.body.decode("utf-8"))
    except Exception:
        payload = request.POST

    login_field = (payload.get("login_field") or "").strip()
    password = payload.get("password") or ""
    if not login_field or not password:
        return JsonResponse({"ok": False, "error": "Faltan credenciales"}, status=400)

    user = authenticate(request=request, username=login_field, password=password)
    if not user or not user.is_active:
        return JsonResponse({"ok": False, "error": "Credenciales inválidas"}, status=401)

    login(request, user)

    return JsonResponse({
        "ok": True,
        "usuario": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "nombre": user.get_full_name() or user.username,
            "is_admin": user.is_superuser,
            "is_staff": user.is_staff,
        }
    })


@csrf_exempt
@require_http_methods(["POST"])
def api_logout_session(request):
    """Logout por sesión Django para el frontend (UI estilo index.html)."""
    if request.user.is_authenticated:
        SesionUsuario.objects.filter(
            usuario=request.user,
            activa=True,
        ).update(activa=False)
    logout(request)
    return JsonResponse({"ok": True})


@require_http_methods(["GET"])
def api_session_user(request):
    """Devuelve el usuario autenticado por sesión Django (UI estilo index.html)."""
    if not request.user.is_authenticated:
        return JsonResponse({"authenticated": False})

    user = request.user
    return JsonResponse({
        "authenticated": True,
        "usuario": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "nombre": user.get_full_name() or user.username,
            "is_admin": user.is_superuser,
            "is_staff": user.is_staff,
        }
    })


