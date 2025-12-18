#!/usr/bin/env python3
"""
Script para subir archivos de síntesis a Supabase Storage

Sube archivos *_sintesis_validacion.json al bucket 'sintesis' de Supabase.

Uso:
    # Configurar Service Role Key primero
    export SUPABASE_SERVICE_ROLE_KEY='tu-service-role-key'
    
    # Subir todos los archivos
    python subir_sintesis_supabase.py
    
    # Subir archivo específico
    python subir_sintesis_supabase.py archivo.json
"""

import json
import os
import sys
from pathlib import Path

# Intentar importar supabase
try:
    from supabase import create_client, Client
except ImportError:
    print("❌ Error: Necesitas instalar la librería supabase")
    print("   Ejecuta: pip install supabase")
    sys.exit(1)

# Configuración de Supabase
SUPABASE_URL = 'https://kyxxpoewwjixbpcezays.supabase.co'
# Necesitas la SERVICE_ROLE_KEY (no la anon key) para subir archivos
# Obtenerla desde: Supabase Dashboard → Settings → API → service_role key
SUPABASE_SERVICE_ROLE_KEY = os.getenv('SUPABASE_SERVICE_ROLE_KEY', '')

if not SUPABASE_SERVICE_ROLE_KEY:
    print("⚠️  ERROR: Necesitas configurar SUPABASE_SERVICE_ROLE_KEY")
    print("   1. Ve a Supabase Dashboard → Settings → API")
    print("   2. Copia la 'service_role' key (secreta)")
    print("   3. Ejecuta: export SUPABASE_SERVICE_ROLE_KEY='tu-key-aqui'")
    print("   4. O añádela al archivo .env")
    sys.exit(1)


def subir_archivo_sintesis(supabase: Client, archivo_path: str, bucket_name: str = 'sintesis'):
    """
    Sube un archivo de síntesis a Supabase Storage
    
    Args:
        supabase: Cliente de Supabase
        archivo_path: Ruta al archivo JSON de síntesis
        bucket_name: Nombre del bucket (default: 'sintesis')
    """
    archivo_path_obj = Path(archivo_path)
    
    if not archivo_path_obj.exists():
        print(f"❌ Archivo no encontrado: {archivo_path}")
        return False
    
    if not archivo_path_obj.name.endswith('_sintesis_validacion.json'):
        print(f"⚠️  Archivo no parece ser de síntesis: {archivo_path_obj.name}")
        respuesta = input("¿Subirlo de todas formas? (s/n): ")
        if respuesta.lower() != 's':
            return False
    
    # Leer archivo
    try:
        with open(archivo_path, 'r', encoding='utf-8') as f:
            contenido = f.read()
            # Validar que sea JSON válido
            json.loads(contenido)
    except json.JSONDecodeError as e:
        print(f"❌ Error: El archivo no es JSON válido: {e}")
        return False
    except Exception as e:
        print(f"❌ Error leyendo archivo: {e}")
        return False
    
    # Nombre del archivo en el bucket (solo el nombre, sin ruta)
    nombre_archivo = archivo_path_obj.name
    
    print(f"📤 Subiendo {nombre_archivo}...")
    
    try:
        # Leer archivo como bytes
        with open(archivo_path, 'rb') as f:
            contenido_bytes = f.read()
        
        # Subir archivo con opciones
        response = supabase.storage.from_(bucket_name).upload(
            nombre_archivo,
            contenido_bytes,
            file_options={
                "content-type": "application/json",
                "upsert": "true"  # Sobrescribir si ya existe
            }
        )
        
        print(f"✅ Archivo subido exitosamente: {nombre_archivo}")
        print(f"   Tamaño: {len(contenido_bytes)} bytes")
        return True
        
    except Exception as e:
        print(f"❌ Error subiendo archivo: {e}")
        print(f"   Tipo de error: {type(e).__name__}")
        if hasattr(e, 'message'):
            print(f"   Mensaje: {e.message}")
        return False


def subir_todos_archivos_sintesis(directorio: str = None):
    """
    Sube todos los archivos de síntesis encontrados
    
    Args:
        directorio: Directorio donde buscar archivos (default: data/fuentesix)
    """
    if not directorio:
        # Directorio por defecto
        script_dir = Path(__file__).parent
        directorio = script_dir
    
    directorio_path = Path(directorio)
    
    if not directorio_path.exists():
        print(f"❌ Directorio no encontrado: {directorio}")
        return
    
    # Inicializar cliente Supabase
    try:
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)
    except Exception as e:
        print(f"❌ Error inicializando Supabase: {e}")
        return
    
    # Buscar archivos de síntesis
    archivos_sintesis = list(directorio_path.glob('*_sintesis_validacion.json'))
    
    if not archivos_sintesis:
        print(f"⚠️  No se encontraron archivos de síntesis en {directorio_path}")
        return
    
    print(f"📁 Encontrados {len(archivos_sintesis)} archivos de síntesis:")
    for archivo in archivos_sintesis:
        print(f"   - {archivo.name}")
    
    print("\n🚀 Iniciando subida...\n")
    
    exitosos = 0
    fallidos = 0
    
    for archivo in archivos_sintesis:
        if subir_archivo_sintesis(supabase, str(archivo)):
            exitosos += 1
        else:
            fallidos += 1
        print()  # Línea en blanco
    
    print("=" * 50)
    print(f"✅ Exitosos: {exitosos}")
    print(f"❌ Fallidos: {fallidos}")
    print(f"📊 Total: {len(archivos_sintesis)}")


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Subir archivos de síntesis a Supabase Storage')
    parser.add_argument('archivo', nargs='?', help='Archivo específico a subir (opcional)')
    parser.add_argument('--directorio', '-d', help='Directorio donde buscar archivos (default: data/fuentesix)')
    
    args = parser.parse_args()
    
    if args.archivo:
        # Subir archivo específico
        if not SUPABASE_SERVICE_ROLE_KEY:
            print("⚠️  ERROR: Necesitas configurar SUPABASE_SERVICE_ROLE_KEY")
            sys.exit(1)
        
        supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)
        subir_archivo_sintesis(supabase, args.archivo)
    else:
        # Subir todos los archivos del directorio
        directorio = args.directorio or Path(__file__).parent
        subir_todos_archivos_sintesis(directorio)






