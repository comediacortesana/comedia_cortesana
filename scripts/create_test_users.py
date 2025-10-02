#!/usr/bin/env python
"""
Script para crear usuarios de prueba con contraseñas simples
"""
import os
import sys
import django

# Configurar Django
sys.path.append('/Users/ivansimo/Documents/2025/ITEM/DELIA_DJANGO')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'teatro_espanol.settings')
django.setup()

from django.contrib.auth import get_user_model
from apps.usuarios.models import PerfilUsuario

def create_test_users():
    """
    Crea usuarios de prueba con contraseñas simples
    """
    print("👥 Creando usuarios de prueba...")
    
    Usuario = get_user_model()
    
    usuarios_prueba = [
        {
            'username': 'test1',
            'email': 'test1@test.com',
            'password': '123',
            'first_name': 'Usuario',
            'last_name': 'Prueba 1',
            'es_investigador': False,
            'institucion': 'Universidad de Prueba',
            'biografia': 'Usuario de prueba para desarrollo',
            'perfil': {
                'especialidades': 'Pruebas de sistema',
                'intereses': 'Desarrollo, testing',
                'publicaciones': '',
                'perfil_publico': True
            }
        },
        {
            'username': 'investigador',
            'email': 'investigador@test.com',
            'password': 'abc',
            'first_name': 'Investigador',
            'last_name': 'Prueba',
            'es_investigador': True,
            'institucion': 'Centro de Investigación',
            'biografia': 'Investigador de prueba',
            'perfil': {
                'especialidades': 'Teatro del Siglo de Oro',
                'intereses': 'Literatura española, Historia del teatro',
                'publicaciones': 'Artículos de prueba sobre teatro',
                'perfil_publico': True
            }
        },
        {
            'username': 'admin',
            'email': 'admin@test.com',
            'password': 'admin',
            'first_name': 'Admin',
            'last_name': 'Prueba',
            'es_investigador': True,
            'institucion': 'Administración',
            'biografia': 'Administrador de prueba',
            'perfil': {
                'especialidades': 'Administración del sistema',
                'intereses': 'Gestión, administración',
                'publicaciones': '',
                'perfil_publico': True
            }
        },
        {
            'username': 'demo',
            'email': 'demo@test.com',
            'password': 'demo',
            'first_name': 'Demo',
            'last_name': 'Usuario',
            'es_investigador': False,
            'institucion': 'Demo University',
            'biografia': 'Usuario de demostración',
            'perfil': {
                'especialidades': 'Demostración',
                'intereses': 'Explorar el sistema',
                'publicaciones': '',
                'perfil_publico': True
            }
        }
    ]
    
    for user_data in usuarios_prueba:
        try:
            perfil_data = user_data.pop('perfil')
            
            # Verificar si el usuario ya existe
            if Usuario.objects.filter(username=user_data['username']).exists():
                print(f"⚠️ Usuario {user_data['username']} ya existe, saltando...")
                continue
            
            # Crear usuario
            usuario = Usuario.objects.create_user(**user_data)
            
            # Crear perfil
            PerfilUsuario.objects.create(usuario=usuario, **perfil_data)
            
            print(f"✅ Usuario creado: {usuario.username} / {user_data['password']}")
            
        except Exception as e:
            print(f"❌ Error creando usuario {user_data['username']}: {e}")
    
    print("\n🎉 Usuarios de prueba creados!")
    print("\n📋 Credenciales de prueba:")
    print("   test1 / 123")
    print("   investigador / abc")
    print("   admin / admin")
    print("   demo / demo")
    print("\n🔗 Acceso: http://127.0.0.1:8001/usuarios/login/")

if __name__ == '__main__':
    create_test_users()
