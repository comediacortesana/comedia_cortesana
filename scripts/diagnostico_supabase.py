"""
Script de diagnóstico para verificar el estado actual de Supabase
Uso: python scripts/diagnostico_supabase.py
"""

import os
import sys
from pathlib import Path
from getpass import getpass

# Agregar el directorio padre al path
sys.path.insert(0, str(Path(__file__).parent.parent))


def obtener_credenciales():
    """Obtiene las credenciales de Supabase"""
    
    # Intentar desde variables de entorno
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_KEY')
    
    if supabase_url and supabase_key:
        print("✅ Credenciales encontradas en variables de entorno")
        return supabase_url, supabase_key
    
    # Si no, pedirlas al usuario
    print("\n🔑 No se encontraron credenciales en variables de entorno")
    print("Por favor, proporciona tus credenciales de Supabase:\n")
    
    print("Puedes encontrarlas en: https://supabase.com/dashboard")
    print("Settings > API > Project URL y Project API keys (anon/public key)\n")
    
    supabase_url = input("SUPABASE_URL (ej: https://xxxxx.supabase.co): ").strip()
    supabase_key = input("SUPABASE_KEY (anon/public key): ").strip()
    
    if not supabase_url or not supabase_key:
        print("❌ Debes proporcionar ambas credenciales")
        sys.exit(1)
    
    return supabase_url, supabase_key


def conectar_supabase(url, key):
    """Intenta conectar a Supabase"""
    try:
        from supabase import create_client
        client = create_client(url, key)
        return client
    except ImportError:
        print("❌ Error: La librería 'supabase' no está instalada")
        print("   Instálala con: pip install supabase")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error al conectar: {e}")
        sys.exit(1)


def listar_tablas(client):
    """Lista todas las tablas públicas"""
    print("\n📊 Verificando tablas en Supabase...")
    
    tablas_esperadas = [
        'obras',
        'comentarios', 
        'validaciones',
        'perfiles_usuarios',
        'historial_validaciones',
        'logs_errores'
    ]
    
    resultados = {}
    
    for tabla in tablas_esperadas:
        try:
            # Intentar hacer una consulta simple
            result = client.table(tabla).select('*', count='exact').limit(0).execute()
            count = result.count if hasattr(result, 'count') else 0
            resultados[tabla] = count
            print(f"  ✅ {tabla}: {count} registros")
        except Exception as e:
            error_msg = str(e)
            if 'does not exist' in error_msg or '42P01' in error_msg:
                resultados[tabla] = None
                print(f"  ❌ {tabla}: NO EXISTE")
            else:
                resultados[tabla] = None
                print(f"  ⚠️  {tabla}: Error - {error_msg[:50]}")
    
    return resultados


def verificar_estructura_obras(client):
    """Verifica si la tabla obras tiene la estructura correcta"""
    print("\n📚 Verificando estructura de la tabla 'obras'...")
    
    try:
        result = client.table('obras').select('*').limit(1).execute()
        
        if not result.data:
            print("  ⚠️  La tabla 'obras' existe pero está vacía")
            return False
        
        # Ver qué campos tiene
        campos = list(result.data[0].keys())
        print(f"  ✅ Campos encontrados: {len(campos)}")
        print(f"     Algunos campos: {', '.join(campos[:10])}")
        
        # Verificar campos clave
        campos_clave = ['id', 'titulo', 'autor', 'fuente']
        campos_faltantes = [c for c in campos_clave if c not in campos]
        
        if campos_faltantes:
            print(f"  ⚠️  Campos clave faltantes: {', '.join(campos_faltantes)}")
        else:
            print(f"  ✅ Todos los campos clave presentes")
        
        return True
        
    except Exception as e:
        error_msg = str(e)
        if 'does not exist' in error_msg or '42P01' in error_msg:
            print("  ❌ La tabla 'obras' NO EXISTE")
        else:
            print(f"  ❌ Error: {error_msg}")
        return False


def verificar_usuarios(client):
    """Verifica usuarios y perfiles"""
    print("\n👤 Verificando usuarios...")
    
    try:
        # Intentar obtener perfiles (los usuarios de auth no son accesibles directamente)
        result = client.table('perfiles_usuarios').select('*', count='exact').limit(5).execute()
        count = result.count if hasattr(result, 'count') else len(result.data)
        
        print(f"  ✅ Perfiles de usuarios: {count}")
        
        if result.data:
            print("\n  Usuarios registrados:")
            for perfil in result.data:
                nombre = perfil.get('nombre_completo', 'N/A')
                rol = perfil.get('rol', 'N/A')
                print(f"    - {nombre} ({rol})")
        
        return True
        
    except Exception as e:
        error_msg = str(e)
        if 'does not exist' in error_msg or '42P01' in error_msg:
            print("  ❌ La tabla 'perfiles_usuarios' NO EXISTE")
        else:
            print(f"  ⚠️  Error: {error_msg}")
        return False


def generar_reporte(resultados):
    """Genera un reporte del diagnóstico"""
    print("\n" + "="*70)
    print("📋 REPORTE DE DIAGNÓSTICO DE SUPABASE")
    print("="*70)
    
    # Contar tablas existentes
    tablas_existentes = [t for t, count in resultados.items() if count is not None]
    tablas_faltantes = [t for t, count in resultados.items() if count is None]
    
    print(f"\n✅ Tablas existentes: {len(tablas_existentes)}/6")
    if tablas_existentes:
        for tabla in tablas_existentes:
            count = resultados[tabla]
            print(f"   - {tabla}: {count} registros")
    
    print(f"\n❌ Tablas faltantes: {len(tablas_faltantes)}/6")
    if tablas_faltantes:
        for tabla in tablas_faltantes:
            print(f"   - {tabla}")
    
    print("\n" + "="*70)
    
    # Determinar estado general
    if len(tablas_existentes) == 0:
        print("🚨 ESTADO: BASE DE DATOS VACÍA")
        print("   Necesitas ejecutar el script de recuperación completo")
        print("   1. Ejecuta RECUPERACION_SUPABASE_COMPLETA.sql en Supabase")
        print("   2. Luego ejecuta sync_to_supabase.py para restaurar datos")
    elif len(tablas_existentes) < 6:
        print("⚠️  ESTADO: RECUPERACIÓN PARCIAL NECESARIA")
        print("   Algunas tablas faltan. Ejecuta RECUPERACION_SUPABASE_COMPLETA.sql")
    else:
        total_obras = resultados.get('obras', 0)
        if total_obras == 0:
            print("⚠️  ESTADO: ESTRUCTURA OK, FALTAN DATOS")
            print("   Las tablas existen pero no hay obras")
            print("   Ejecuta sync_to_supabase.py para restaurar datos")
        else:
            print("✅ ESTADO: RECUPERACIÓN COMPLETA")
            print(f"   Todo parece estar en orden ({total_obras} obras)")
    
    print("="*70)


def main():
    print("="*70)
    print("🔍 DIAGNÓSTICO DE SUPABASE")
    print("="*70)
    
    # 1. Obtener credenciales
    print("\n🔐 Paso 1: Obteniendo credenciales...")
    url, key = obtener_credenciales()
    
    # 2. Conectar
    print("\n🔌 Paso 2: Conectando a Supabase...")
    try:
        client = conectar_supabase(url, key)
        print("✅ Conexión exitosa")
    except Exception as e:
        print(f"❌ No se pudo conectar: {e}")
        sys.exit(1)
    
    # 3. Listar tablas
    print("\n📊 Paso 3: Verificando estructura...")
    resultados = listar_tablas(client)
    
    # 4. Verificar obras si existe
    if resultados.get('obras') is not None:
        verificar_estructura_obras(client)
    
    # 5. Verificar usuarios si existe
    if resultados.get('perfiles_usuarios') is not None:
        verificar_usuarios(client)
    
    # 6. Generar reporte
    generar_reporte(resultados)
    
    print("\n✅ Diagnóstico completado\n")


if __name__ == '__main__':
    main()

