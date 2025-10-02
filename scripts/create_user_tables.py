#!/usr/bin/env python
"""
Script para crear las tablas de usuarios manualmente
"""
import os
import sys
import django

# Configurar Django
sys.path.append('/Users/ivansimo/Documents/2025/ITEM/DELIA_DJANGO')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'teatro_espanol.settings')
django.setup()

from django.db import connection

def create_user_tables():
    """
    Crea las tablas de usuarios manualmente usando SQL
    """
    print("🔧 Creando tablas de usuarios...")
    
    with connection.cursor() as cursor:
        # Crear tabla usuarios_usuario
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios_usuario (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                password VARCHAR(128) NOT NULL,
                last_login DATETIME,
                is_superuser BOOLEAN NOT NULL DEFAULT 0,
                username VARCHAR(150) NOT NULL UNIQUE,
                first_name VARCHAR(150) NOT NULL,
                last_name VARCHAR(150) NOT NULL,
                email VARCHAR(254) NOT NULL UNIQUE,
                is_staff BOOLEAN NOT NULL DEFAULT 0,
                is_active BOOLEAN NOT NULL DEFAULT 1,
                date_joined DATETIME NOT NULL,
                fecha_registro DATETIME NOT NULL,
                es_investigador BOOLEAN NOT NULL DEFAULT 0,
                institucion VARCHAR(200) NOT NULL DEFAULT '',
                biografia TEXT NOT NULL DEFAULT '',
                avatar VARCHAR(100) NOT NULL DEFAULT '',
                notificaciones_email BOOLEAN NOT NULL DEFAULT 1,
                tema_oscuro BOOLEAN NOT NULL DEFAULT 0
            )
        """)
        
        # Crear tabla usuarios_perfilusuario
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios_perfilusuario (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                especialidades TEXT NOT NULL DEFAULT '',
                intereses TEXT NOT NULL DEFAULT '',
                publicaciones TEXT NOT NULL DEFAULT '',
                redes_sociales TEXT NOT NULL DEFAULT '{}',
                perfil_publico BOOLEAN NOT NULL DEFAULT 1,
                mostrar_email BOOLEAN NOT NULL DEFAULT 0,
                mostrar_institucion BOOLEAN NOT NULL DEFAULT 1,
                fecha_actualizacion DATETIME NOT NULL,
                usuario_id INTEGER NOT NULL UNIQUE REFERENCES usuarios_usuario(id) DEFERRABLE INITIALLY DEFERRED
            )
        """)
        
        # Crear tabla usuarios_sesionusuario
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios_sesionusuario (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ip_address CHAR(39) NOT NULL,
                user_agent TEXT NOT NULL,
                fecha_inicio DATETIME NOT NULL,
                fecha_ultima_actividad DATETIME NOT NULL,
                activa BOOLEAN NOT NULL DEFAULT 1,
                usuario_id INTEGER NOT NULL REFERENCES usuarios_usuario(id) DEFERRABLE INITIALLY DEFERRED
            )
        """)
        
        # Crear índices
        cursor.execute("CREATE INDEX IF NOT EXISTS usuarios_usuario_username_idx ON usuarios_usuario(username)")
        cursor.execute("CREATE INDEX IF NOT EXISTS usuarios_usuario_email_idx ON usuarios_usuario(email)")
        cursor.execute("CREATE INDEX IF NOT EXISTS usuarios_perfilusuario_usuario_id_idx ON usuarios_perfilusuario(usuario_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS usuarios_sesionusuario_usuario_id_idx ON usuarios_sesionusuario(usuario_id)")
        
        print("✅ Tablas de usuarios creadas exitosamente")

def create_admin_user():
    """
    Crea el usuario administrador
    """
    print("👤 Creando usuario administrador...")
    
    from django.contrib.auth import get_user_model
    from django.utils import timezone
    from django.contrib.auth.hashers import make_password
    
    Usuario = get_user_model()
    
    # Verificar si ya existe
    if Usuario.objects.filter(username='admin_teatro').exists():
        print("✅ Usuario admin_teatro ya existe")
        return
    
    try:
        # Crear usuario usando SQL directo para evitar problemas de migración
        with connection.cursor() as cursor:
            now = timezone.now()
            password_hash = make_password('teatro123')
            
            cursor.execute("""
                INSERT INTO usuarios_usuario (
                    username, email, password, first_name, last_name,
                    is_superuser, is_staff, is_active, date_joined, fecha_registro,
                    es_investigador, institucion, biografia
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, [
                'admin_teatro',
                'admin@teatroespanol.com',
                password_hash,
                'Administrador',
                'Teatro Español',
                1,  # is_superuser
                1,  # is_staff
                1,  # is_active
                now,
                now,
                1,  # es_investigador
                'Teatro Español del Siglo de Oro',
                'Administrador del sistema de catálogo de teatro español'
            ])
            
            user_id = cursor.lastrowid
            
            # Crear perfil
            cursor.execute("""
                INSERT INTO usuarios_perfilusuario (
                    usuario_id, especialidades, intereses, publicaciones,
                    perfil_publico, mostrar_email, mostrar_institucion, fecha_actualizacion
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, [
                user_id,
                'Administración del sistema',
                'Teatro del Siglo de Oro, Gestión de datos',
                'Sistema de catálogo de teatro español',
                1,  # perfil_publico
                0,  # mostrar_email
                1,  # mostrar_institucion
                now
            ])
        
        print("✅ Usuario administrador creado exitosamente")
        
    except Exception as e:
        print(f"❌ Error creando usuario administrador: {e}")

def check_data():
    """
    Verifica qué datos existen en la base de datos
    """
    print("🔍 Verificando datos existentes...")
    
    from apps.obras.models import Obra
    from apps.autores.models import Autor
    from apps.lugares.models import Lugar
    from apps.representaciones.models import Representacion
    from apps.bibliografia.models import ReferenciaBibliografica
    from django.contrib.auth import get_user_model
    
    print(f"📚 Obras: {Obra.objects.count()}")
    print(f"✍️ Autores: {Autor.objects.count()}")
    print(f"📍 Lugares: {Lugar.objects.count()}")
    print(f"🎪 Representaciones: {Representacion.objects.count()}")
    print(f"📖 Referencias Bibliográficas: {ReferenciaBibliografica.objects.count()}")
    
    Usuario = get_user_model()
    print(f"👥 Usuarios: {Usuario.objects.count()}")

if __name__ == '__main__':
    print("🚀 Creando tablas de usuarios...")
    
    # Crear tablas
    create_user_tables()
    
    # Crear usuario administrador
    create_admin_user()
    
    # Verificar datos
    check_data()
    
    print("\n✨ ¡Tablas de usuarios creadas exitosamente!")
    print("\n🔑 Credenciales de acceso:")
    print("   Usuario: admin_teatro")
    print("   Contraseña: teatro123")
    print("   URL: http://127.0.0.1:8000/admin/")
    print("   Login: http://127.0.0.1:8000/usuarios/login/")
