#!/usr/bin/env python3
"""
Script para probar la conexión con Supabase
"""

import urllib.request
import urllib.error
import json
from datetime import datetime

# Configuración de Supabase
SUPABASE_URL = 'https://kyxxpoewwjixbpcezays.supabase.co'
SUPABASE_ANON_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imt5eHhwb2V3d2ppeGJwY2V6YXlzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjI0MjAzMDksImV4cCI6MjA3Nzk5NjMwOX0.sIw7flVHQ00r3VwrhU7tvohVzKpb7LGtXVzG43FAP10'

def test_connection():
    """Prueba la conexión básica con Supabase"""
    print("=" * 60)
    print("🔍 PRUEBA DE CONEXIÓN CON SUPABASE")
    print("=" * 60)
    print(f"URL: {SUPABASE_URL}")
    print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Headers necesarios para Supabase
    headers = {
        'apikey': SUPABASE_ANON_KEY,
        'Authorization': f'Bearer {SUPABASE_ANON_KEY}',
        'Content-Type': 'application/json',
        'Prefer': 'return=representation'
    }
    
    # Test 1: Verificar que el endpoint responde
    print("📡 Test 1: Verificando endpoint de Supabase...")
    try:
        req = urllib.request.Request(
            f"{SUPABASE_URL}/rest/v1/",
            headers=headers
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            status_code = response.getcode()
            print(f"   Status Code: {status_code}")
            if status_code in [200, 404, 406]:  # 404/406 son normales para el endpoint raíz
                print("   ✅ Endpoint responde correctamente")
            else:
                print(f"   ⚠️ Respuesta inesperada: {status_code}")
        print()
    except urllib.error.HTTPError as e:
        print(f"   Status Code: {e.code}")
        if e.code in [404, 406]:
            print("   ✅ Endpoint responde (404/406 es normal para endpoint raíz)")
        else:
            print(f"   ⚠️ Respuesta: {e.code}")
        print()
    except urllib.error.URLError as e:
        print(f"   ❌ Error de conexión: {e}")
        print()
        return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        print()
        return False
    
    # Test 2: Probar acceso a la tabla de perfiles
    print("📡 Test 2: Probando acceso a tabla 'perfiles_usuarios'...")
    try:
        req = urllib.request.Request(
            f"{SUPABASE_URL}/rest/v1/perfiles_usuarios?select=id&limit=1",
            headers=headers
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            status_code = response.getcode()
            print(f"   Status Code: {status_code}")
            if status_code == 200:
                data = json.loads(response.read().decode())
                print(f"   ✅ Acceso exitoso. Datos recibidos: {len(data)} registros")
                if data:
                    print(f"   📋 Ejemplo: {json.dumps(data[0], indent=2)}")
        print()
    except urllib.error.HTTPError as e:
        print(f"   Status Code: {e.code}")
        if e.code == 401:
            print("   ⚠️ Error 401: Problema de autenticación (RLS puede estar bloqueando)")
        elif e.code == 404:
            print("   ⚠️ Error 404: Tabla no encontrada")
        else:
            error_body = e.read().decode()[:200]
            print(f"   ⚠️ Respuesta: {error_body}")
        print()
    except Exception as e:
        print(f"   ❌ Error: {e}")
        print()
    
    # Test 3: Probar acceso a la tabla de obras
    print("📡 Test 3: Probando acceso a tabla 'obras'...")
    try:
        req = urllib.request.Request(
            f"{SUPABASE_URL}/rest/v1/obras?select=id,titulo&limit=1",
            headers=headers
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            status_code = response.getcode()
            print(f"   Status Code: {status_code}")
            if status_code == 200:
                data = json.loads(response.read().decode())
                print(f"   ✅ Acceso exitoso. Datos recibidos: {len(data)} registros")
                if data:
                    print(f"   📋 Ejemplo: {json.dumps(data[0], indent=2)}")
        print()
    except urllib.error.HTTPError as e:
        print(f"   Status Code: {e.code}")
        if e.code == 401:
            print("   ⚠️ Error 401: Problema de autenticación (RLS puede estar bloqueando)")
        elif e.code == 404:
            print("   ⚠️ Error 404: Tabla no encontrada")
        else:
            error_body = e.read().decode()[:200]
            print(f"   ⚠️ Respuesta: {error_body}")
        print()
    except Exception as e:
        print(f"   ❌ Error: {e}")
        print()
    
    # Test 4: Verificar CORS
    print("📡 Test 4: Verificando headers CORS...")
    try:
        req = urllib.request.Request(
            f"{SUPABASE_URL}/rest/v1/obras",
            headers=headers,
            method='OPTIONS'
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            cors_headers = {
                'access-control-allow-origin': response.headers.get('access-control-allow-origin'),
                'access-control-allow-methods': response.headers.get('access-control-allow-methods'),
                'access-control-allow-headers': response.headers.get('access-control-allow-headers'),
            }
            print(f"   CORS Headers: {json.dumps(cors_headers, indent=2)}")
            if cors_headers['access-control-allow-origin']:
                print("   ✅ CORS configurado correctamente")
            else:
                print("   ⚠️ CORS puede no estar configurado")
        print()
    except Exception as e:
        print(f"   ⚠️ No se pudo verificar CORS: {e}")
        print()
    
    print("=" * 60)
    print("✅ Pruebas completadas")
    print("=" * 60)
    return True

if __name__ == '__main__':
    try:
        test_connection()
    except KeyboardInterrupt:
        print("\n\n⚠️ Prueba interrumpida por el usuario")
    except Exception as e:
        print(f"\n\n❌ Error fatal: {e}")
        import traceback
        traceback.print_exc()

