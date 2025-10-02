#!/usr/bin/env python
"""
Script para restaurar los datos de obras después de implementar usuarios
"""
import os
import sys
import django

# Configurar Django
sys.path.append('/Users/ivansimo/Documents/2025/ITEM/DELIA_DJANGO')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'teatro_espanol.settings')
django.setup()

from django.contrib.auth import get_user_model
from apps.obras.models import Obra
from apps.autores.models import Autor
from apps.lugares.models import Lugar
from apps.representaciones.models import Representacion
from apps.bibliografia.models import ReferenciaBibliografica

def check_data():
    """
    Verifica qué datos existen en la base de datos
    """
    print("🔍 Verificando datos existentes...")
    
    print(f"📚 Obras: {Obra.objects.count()}")
    print(f"✍️ Autores: {Autor.objects.count()}")
    print(f"📍 Lugares: {Lugar.objects.count()}")
    print(f"🎪 Representaciones: {Representacion.objects.count()}")
    print(f"📖 Referencias Bibliográficas: {ReferenciaBibliografica.objects.count()}")
    
    Usuario = get_user_model()
    print(f"👥 Usuarios: {Usuario.objects.count()}")

def create_admin_user():
    """
    Crea el usuario administrador
    """
    print("👤 Creando usuario administrador...")
    
    Usuario = get_user_model()
    
    # Verificar si ya existe
    if Usuario.objects.filter(username='admin_teatro').exists():
        print("✅ Usuario admin_teatro ya existe")
        return
    
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
        
        # Crear perfil
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

def import_data_from_scripts():
    """
    Importa datos usando los scripts existentes
    """
    print("📥 Importando datos desde scripts existentes...")
    
    scripts_dir = "/Users/ivansimo/Documents/2025/ITEM/DELIA_DJANGO/scripts"
    
    # Lista de scripts de importación disponibles
    import_scripts = [
        "import_catcom.py",
        "import_fuentesxi.py", 
        "import_obras_only.py",
        "import_simple.py"
    ]
    
    for script in import_scripts:
        script_path = os.path.join(scripts_dir, script)
        if os.path.exists(script_path):
            print(f"🔄 Ejecutando {script}...")
            try:
                # Ejecutar el script
                import subprocess
                result = subprocess.run([
                    sys.executable, script_path
                ], capture_output=True, text=True, cwd=scripts_dir)
                
                if result.returncode == 0:
                    print(f"✅ {script} ejecutado exitosamente")
                else:
                    print(f"⚠️ {script} terminó con errores: {result.stderr}")
                    
            except Exception as e:
                print(f"❌ Error ejecutando {script}: {e}")
        else:
            print(f"⚠️ Script {script} no encontrado")

if __name__ == '__main__':
    print("🚀 Iniciando restauración de datos...")
    
    # Verificar datos actuales
    check_data()
    
    # Crear usuario administrador
    create_admin_user()
    
    # Si no hay obras, intentar importar
    if Obra.objects.count() == 0:
        print("📚 No se encontraron obras. Intentando importar datos...")
        import_data_from_scripts()
    else:
        print("✅ Ya existen obras en la base de datos")
    
    # Verificar datos finales
    print("\n📊 Estado final de los datos:")
    check_data()
    
    print("\n✨ ¡Restauración completada!")
    print("\n🔑 Credenciales de acceso:")
    print("   Usuario: admin_teatro")
    print("   Contraseña: teatro123")
    print("   URL: http://127.0.0.1:8000/admin/")
