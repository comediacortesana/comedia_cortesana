"""
Script de diagnóstico simple usando solo requests (sin dependencias de supabase)
Uso: python scripts/diagnostico_simple.py
"""

import json
import sys

try:
    import requests
except ImportError:
    print("❌ Error: requests no está instalado")
    print("   Instala con: pip3 install requests")
    sys.exit(1)


def verificar_tabla(url, key, tabla):
    """Verifica si una tabla existe y cuenta registros"""
    headers = {
        'apikey': key,
        'Authorization': f'Bearer {key}',
        'Content-Type': 'application/json',
        'Prefer': 'count=exact'
    }
    
    try:
        # Hacer una consulta simple
        response = requests.get(
            f'{url}/rest/v1/{tabla}',
            headers=headers,
            params={'select': 'id', 'limit': '0'}
        )
        
        if response.status_code == 200:
            # Obtener el conteo del header
            content_range = response.headers.get('Content-Range', '')
            if content_range:
                # Format: "0-0/123" donde 123 es el total
                total = content_range.split('/')[-1]
                try:
                    return int(total)
                except:
                    return 0
            return 0
        elif response.status_code == 404 or response.status_code == 406:
            return None  # Tabla no existe
        else:
            return None
    except Exception as e:
        print(f"    Error consultando {tabla}: {e}")
        return None


def obtener_muestra_obra(url, key):
    """Obtiene una obra de ejemplo"""
    headers = {
        'apikey': key,
        'Authorization': f'Bearer {key}',
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.get(
            f'{url}/rest/v1/obras',
            headers=headers,
            params={'select': '*', 'limit': '1'}
        )
        
        if response.status_code == 200:
            data = response.json()
            if data:
                return data[0]
        return None
    except Exception as e:
        print(f"    Error obteniendo muestra: {e}")
        return None


def main():
    # Credenciales
    url = "https://kyxxpoewwjixbpcezays.supabase.co"
    key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imt5eHhwb2V3d2ppeGJwY2V6YXlzIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2MjQyMDMwOSwiZXhwIjoyMDc3OTk2MzA5fQ.X6T-hcv-i-bYGaPEG6sK8gqOUAvNCj_YPI4xAf89S30"
    
    print("="*70)
    print("🔍 DIAGNÓSTICO SIMPLE DE SUPABASE")
    print("="*70)
    
    print(f"\n🔌 Conectando a: {url}")
    
    # Verificar tablas
    print("\n📊 Verificando tablas...")
    
    tablas = [
        'obras',
        'comentarios',
        'validaciones',
        'perfiles_usuarios',
        'historial_validaciones',
        'logs_errores'
    ]
    
    resultados = {}
    for tabla in tablas:
        count = verificar_tabla(url, key, tabla)
        resultados[tabla] = count
        
        if count is None:
            print(f"  ❌ {tabla}: NO EXISTE")
        else:
            print(f"  ✅ {tabla}: {count} registros")
    
    # Verificar estructura de obras si existe
    if resultados.get('obras') is not None:
        print("\n📚 Verificando estructura de 'obras'...")
        muestra = obtener_muestra_obra(url, key)
        
        if muestra:
            campos = list(muestra.keys())
            print(f"  ✅ Campos encontrados: {len(campos)}")
            print(f"     Primeros 15 campos: {', '.join(campos[:15])}")
            
            # Mostrar ejemplo
            print(f"\n  📖 Ejemplo de obra:")
            print(f"     ID: {muestra.get('id', 'N/A')}")
            print(f"     Título: {muestra.get('titulo', 'N/A')}")
            print(f"     Autor: {muestra.get('autor', muestra.get('autor_nombre', 'N/A'))}")
            print(f"     Fuente: {muestra.get('fuente', 'N/A')}")
        else:
            print("  ⚠️  La tabla existe pero está vacía")
    
    # Reporte final
    print("\n" + "="*70)
    print("📋 REPORTE FINAL")
    print("="*70)
    
    tablas_existentes = [t for t, c in resultados.items() if c is not None]
    tablas_faltantes = [t for t, c in resultados.items() if c is None]
    
    print(f"\n✅ Tablas existentes: {len(tablas_existentes)}/6")
    if tablas_existentes:
        for tabla in tablas_existentes:
            print(f"   - {tabla}: {resultados[tabla]} registros")
    
    print(f"\n❌ Tablas faltantes: {len(tablas_faltantes)}/6")
    if tablas_faltantes:
        for tabla in tablas_faltantes:
            print(f"   - {tabla}")
    
    print("\n" + "="*70)
    
    # Estado y recomendaciones
    if len(tablas_existentes) == 0:
        print("🚨 ESTADO: BASE DE DATOS COMPLETAMENTE VACÍA")
        print("\n📝 PASOS PARA RECUPERAR:")
        print("   1. Ve a Supabase Dashboard > SQL Editor")
        print("   2. Ejecuta el contenido de: RECUPERACION_SUPABASE_COMPLETA.sql")
        print("   3. Luego ejecuta: python scripts/sync_to_supabase.py")
    elif len(tablas_existentes) < 6:
        print("⚠️  ESTADO: ESTRUCTURA INCOMPLETA")
        print("\n📝 PASOS PARA RECUPERAR:")
        print("   1. Ve a Supabase Dashboard > SQL Editor")
        print("   2. Ejecuta el contenido de: RECUPERACION_SUPABASE_COMPLETA.sql")
        print("   3. Luego ejecuta: python scripts/sync_to_supabase.py")
    else:
        total_obras = resultados.get('obras', 0)
        if total_obras == 0:
            print("⚠️  ESTADO: ESTRUCTURA OK, PERO SIN DATOS")
            print("\n📝 PASOS PARA RECUPERAR:")
            print("   1. Ejecuta: python scripts/sync_to_supabase.py")
        else:
            print("✅ ESTADO: TODO PARECE ESTAR BIEN")
            print(f"\n   Base de datos funcional con {total_obras} obras")
    
    print("="*70)
    print()


if __name__ == '__main__':
    main()

