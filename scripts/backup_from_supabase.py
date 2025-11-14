"""
Script para hacer backup de Supabase a JSON
Uso: python scripts/backup_from_supabase.py [--output datos_obras.json]
"""

import argparse
import json
import sys
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime

# Agregar el directorio padre al path para imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.supabase_client import SupabaseSync


def backup_supabase_to_json(
    output_file: str = 'datos_obras.json',
    dry_run: bool = False
) -> Dict[str, Any]:
    """
    Hace backup de todas las obras de Supabase a un archivo JSON
    """
    sync = SupabaseSync()
    
    print("📥 Cargando obras desde Supabase...")
    obras = sync.get_all_obras()
    
    if not obras:
        print("⚠️ No se encontraron obras en Supabase")
        return {'success': False, 'reason': 'No hay obras en Supabase'}
    
    print(f"✅ {len(obras)} obras cargadas desde Supabase")
    
    # Formatear datos con metadata
    datos_backup = {
        'metadata': {
            'total_obras': len(obras),
            'fecha_backup': datetime.now().isoformat(),
            'fuente': 'Supabase',
            'version': '1.0'
        },
        'obras': obras
    }
    
    if dry_run:
        print(f"\n🔍 DRY RUN: Se guardarían {len(obras)} obras en {output_file}")
        return {
            'success': True,
            'dry_run': True,
            'count': len(obras)
        }
    
    # Guardar a archivo JSON
    output_path = Path(output_file)
    print(f"\n💾 Guardando backup en {output_path}...")
    
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(datos_backup, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Backup guardado exitosamente: {output_path}")
        print(f"   Total de obras: {len(obras)}")
        print(f"   Tamaño del archivo: {output_path.stat().st_size / 1024:.2f} KB")
        
        return {
            'success': True,
            'count': len(obras),
            'file': str(output_path),
            'size_kb': output_path.stat().st_size / 1024
        }
    except Exception as e:
        print(f"❌ Error guardando backup: {e}")
        return {
            'success': False,
            'error': str(e)
        }


def main():
    parser = argparse.ArgumentParser(
        description='Hace backup de Supabase a archivo JSON'
    )
    parser.add_argument(
        '--output',
        type=str,
        default='datos_obras.json',
        help='Archivo JSON de salida (default: datos_obras.json)'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Simular backup sin guardar archivo'
    )
    
    args = parser.parse_args()
    
    result = backup_supabase_to_json(
        output_file=args.output,
        dry_run=args.dry_run
    )
    
    if result['success']:
        print("\n✅ Proceso completado exitosamente")
        sys.exit(0)
    else:
        print("\n❌ Proceso falló")
        sys.exit(1)


if __name__ == '__main__':
    main()

