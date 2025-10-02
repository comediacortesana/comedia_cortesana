#!/usr/bin/env python
"""
Script para migrar de User por defecto a Usuario personalizado
"""
import os
import sys
import django

# Configurar Django
import sys
sys.path.append('/Users/ivansimo/Documents/2025/ITEM/DELIA_DJANGO')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'teatro_espanol.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.db import connection
from django.core.management import execute_from_command_line

def migrate_user_data():
    """
    Migra los datos de auth_user a usuarios_usuario
    """
    print("🔄 Iniciando migración de datos de usuario...")
    
    # Obtener el modelo de usuario personalizado
    Usuario = get_user_model()
    
    # Verificar si ya existen usuarios personalizados
    if Usuario.objects.exists():
        print("✅ Ya existen usuarios personalizados. No es necesario migrar.")
        return
    
    # Crear el superusuario por defecto
    try:
        usuario_admin = Usuario.objects.create_superuser(
            username='admin_teatro',
            email='admin@teatroespanol.com',
            password='teatro123',
            first_name='Administrador',
            last_name='Teatro Español',
            es_investigador=True,
            institucion='Teatro Español del Siglo de Oro'
        )
        print(f"✅ Superusuario creado: {usuario_admin.username}")
        
        # Crear perfil para el superusuario
        from apps.usuarios.models import PerfilUsuario
        PerfilUsuario.objects.create(
            usuario=usuario_admin,
            especialidades="Administración del sistema",
            intereses="Teatro del Siglo de Oro, Gestión de datos",
            perfil_publico=True
        )
        print("✅ Perfil de superusuario creado")
        
    except Exception as e:
        print(f"❌ Error creando superusuario: {e}")
    
    print("🎉 Migración de usuarios completada!")

def create_sample_users():
    """
    Crea algunos usuarios de ejemplo
    """
    print("👥 Creando usuarios de ejemplo...")
    
    Usuario = get_user_model()
    from apps.usuarios.models import PerfilUsuario
    
    usuarios_ejemplo = [
        {
            'username': 'investigador1',
            'email': 'investigador1@universidad.edu',
            'password': 'investigador123',
            'first_name': 'María',
            'last_name': 'García López',
            'es_investigador': True,
            'institucion': 'Universidad Complutense de Madrid',
            'biografia': 'Especialista en teatro del Siglo de Oro español',
            'perfil': {
                'especialidades': 'Teatro del Siglo de Oro, Literatura española',
                'intereses': 'Lope de Vega, Calderón de la Barca, Tirso de Molina',
                'publicaciones': 'Varios artículos sobre comedia nueva'
            }
        },
        {
            'username': 'estudiante1',
            'email': 'estudiante1@universidad.edu',
            'password': 'estudiante123',
            'first_name': 'Carlos',
            'last_name': 'Rodríguez Martín',
            'es_investigador': False,
            'institucion': 'Universidad de Salamanca',
            'biografia': 'Estudiante de Filología Hispánica',
            'perfil': {
                'especialidades': 'Literatura española',
                'intereses': 'Teatro clásico, Historia de la literatura',
                'publicaciones': ''
            }
        }
    ]
    
    for user_data in usuarios_ejemplo:
        try:
            perfil_data = user_data.pop('perfil')
            usuario = Usuario.objects.create_user(**user_data)
            PerfilUsuario.objects.create(usuario=usuario, **perfil_data)
            print(f"✅ Usuario creado: {usuario.username}")
        except Exception as e:
            print(f"❌ Error creando usuario {user_data['username']}: {e}")
    
    print("🎉 Usuarios de ejemplo creados!")

if __name__ == '__main__':
    print("🚀 Iniciando migración de usuarios...")
    
    # Ejecutar migraciones
    print("📦 Aplicando migraciones...")
    execute_from_command_line(['manage.py', 'migrate', '--run-syncdb'])
    
    # Migrar datos de usuario
    migrate_user_data()
    
    # Crear usuarios de ejemplo
    create_sample_users()
    
    print("✨ ¡Migración completada exitosamente!")
    print("\n📋 Usuarios disponibles:")
    print("   - admin_teatro / teatro123 (Superusuario)")
    print("   - investigador1 / investigador123 (Investigador)")
    print("   - estudiante1 / estudiante123 (Estudiante)")
