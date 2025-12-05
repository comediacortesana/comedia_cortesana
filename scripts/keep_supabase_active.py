#!/usr/bin/env python3
"""
Script para mantener Supabase activo mediante consultas periódicas.
Este script hace una consulta simple a Supabase para evitar que se ponga en modo inactivo.
"""

import os
import sys
import requests
from datetime import datetime

def query_supabase():
    """Hace una consulta simple a Supabase para mantenerlo activo"""
    
    # Obtener variables de entorno
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_KEY')
    
    if not supabase_url:
        print("❌ Error: SUPABASE_URL no está definido")
        sys.exit(1)
    
    if not supabase_key:
        print("❌ Error: SUPABASE_KEY no está definido")
        sys.exit(1)
    
    # Construir URL de la API REST de Supabase
    # Hacemos una consulta simple a la tabla 'obras' limitada a 1 resultado
    api_url = f"{supabase_url}/rest/v1/obras?select=id&limit=1"
    
    headers = {
        'apikey': supabase_key,
        'Authorization': f'Bearer {supabase_key}',
        'Content-Type': 'application/json',
        'Prefer': 'return=representation'
    }
    
    try:
        print(f"🔄 Consultando Supabase a las {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}...")
        print(f"📍 URL: {supabase_url}")
        
        # Hacer la consulta
        response = requests.get(api_url, headers=headers, timeout=30)
        
        if response.status_code == 200:
            print("✅ Consulta exitosa - Supabase está activo")
            print(f"📊 Respuesta: {len(response.json())} registro(s) obtenido(s)")
            return True
        elif response.status_code == 401:
            print("❌ Error de autenticación - Verifica SUPABASE_KEY")
            print(f"   Status: {response.status_code}")
            sys.exit(1)
        elif response.status_code == 404:
            print("⚠️  Tabla 'obras' no encontrada - Esto es normal si la tabla no existe aún")
            print(f"   Status: {response.status_code}")
            return True  # No es un error crítico
        else:
            print(f"⚠️  Respuesta inesperada: Status {response.status_code}")
            print(f"   Mensaje: {response.text[:200]}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ Error: Timeout al conectar con Supabase")
        sys.exit(1)
    except requests.exceptions.ConnectionError:
        print("❌ Error: No se pudo conectar con Supabase")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error inesperado: {str(e)}")
        sys.exit(1)


if __name__ == '__main__':
    success = query_supabase()
    if success:
        print("✅ Script completado exitosamente")
        sys.exit(0)
    else:
        print("⚠️  Script completado con advertencias")
        sys.exit(0)  # No fallar el workflow por advertencias menores

