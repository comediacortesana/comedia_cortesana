"""
Script para mantener Supabase activo con consultas periódicas
Ejecutado por GitHub Actions cada 12 horas
"""

import os
import sys
import json
from datetime import datetime

try:
    import requests
except ImportError:
    print("❌ Error: requests no está instalado")
    sys.exit(1)


def main():
    """Realiza consultas simples a Supabase para mantenerlo activo"""
    
    # Obtener credenciales
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_KEY')
    
    if not supabase_url or not supabase_key:
        print("❌ Error: SUPABASE_URL y SUPABASE_KEY deben estar definidos")
        sys.exit(1)
    
    print("="*70)
    print("🤖 KEEP SUPABASE ACTIVE")
    print("="*70)
    print(f"⏰ Timestamp: {datetime.utcnow().isoformat()}Z")
    print(f"🔌 URL: {supabase_url}")
    print()
    
    headers = {
        'apikey': supabase_key,
        'Authorization': f'Bearer {supabase_key}',
        'Content-Type': 'application/json'
    }
    
    # Lista de consultas simples a realizar
    queries = [
        {
            'name': 'Obras',
            'endpoint': '/rest/v1/obras',
            'params': {'select': 'id', 'limit': '1'}
        },
        {
            'name': 'Comentarios',
            'endpoint': '/rest/v1/comentarios',
            'params': {'select': 'id', 'limit': '1'}
        },
        {
            'name': 'Perfiles',
            'endpoint': '/rest/v1/perfiles_usuarios',
            'params': {'select': 'id', 'limit': '1'}
        }
    ]
    
    success_count = 0
    error_count = 0
    
    print("📊 Ejecutando consultas...")
    print()
    
    for query in queries:
        try:
            url = f"{supabase_url}{query['endpoint']}"
            response = requests.get(
                url,
                headers=headers,
                params=query['params'],
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                count = len(data)
                print(f"  ✅ {query['name']}: OK ({count} registros)")
                success_count += 1
            else:
                print(f"  ⚠️  {query['name']}: HTTP {response.status_code}")
                error_count += 1
                
        except Exception as e:
            print(f"  ❌ {query['name']}: Error - {str(e)[:50]}")
            error_count += 1
    
    print()
    print("="*70)
    print("📋 RESUMEN")
    print("="*70)
    print(f"✅ Consultas exitosas: {success_count}/{len(queries)}")
    
    if error_count > 0:
        print(f"❌ Consultas fallidas: {error_count}/{len(queries)}")
    
    print()
    print(f"⏰ Finalizado: {datetime.utcnow().isoformat()}Z")
    print("🔄 Próxima ejecución: según schedule de GitHub Actions")
    print("="*70)
    
    # Salir con error si todas las consultas fallaron
    if success_count == 0:
        print()
        print("⚠️  ADVERTENCIA: Todas las consultas fallaron")
        sys.exit(1)
    
    # Éxito si al menos una consulta funcionó
    sys.exit(0)


if __name__ == '__main__':
    main()

