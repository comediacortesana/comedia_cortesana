"""
Script completo para hacer backup de todas las tablas de Supabase
Uso: python scripts/backup_supabase_completo.py [--output backup.json] [--format json|db]
"""

import argparse
import json
import sys
import sqlite3
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime

# Agregar el directorio padre al path para imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.supabase_client import get_supabase_client


def get_all_table_data(client, table_name: str, page_size: int = 1000) -> List[Dict[str, Any]]:
    """
    Obtiene todos los datos de una tabla con paginación
    """
    all_data = []
    offset = 0
    
    while True:
        try:
            response = client.table(table_name).select('*').range(offset, offset + page_size - 1).execute()
            if not response.data:
                break
            all_data.extend(response.data)
            if len(response.data) < page_size:
                break
            offset += page_size
        except Exception as e:
            print(f"⚠️ Error obteniendo datos de {table_name}: {e}")
            break
    
    return all_data


def backup_to_json(
    output_file: str = 'backup_supabase.json',
    dry_run: bool = False
) -> Dict[str, Any]:
    """
    Hace backup de todas las tablas de Supabase a un archivo JSON
    """
    client = get_supabase_client()
    
    # Lista de tablas a respaldar
    tables = [
        'obras',
        'comentarios',
        'validaciones',
        'historial_validaciones',
        'perfiles_usuarios'
    ]
    
    print("📥 Iniciando backup de Supabase...")
    print(f"📊 Tablas a respaldar: {', '.join(tables)}\n")
    
    backup_data = {
        'metadata': {
            'fecha_backup': datetime.now().isoformat(),
            'fuente': 'Supabase',
            'version': '1.0'
        },
        'tables': {}
    }
    
    total_records = 0
    
    for table_name in tables:
        print(f"📥 Cargando {table_name}...", end=' ')
        try:
            table_data = get_all_table_data(client, table_name)
            backup_data['tables'][table_name] = table_data
            count = len(table_data)
            total_records += count
            print(f"✅ {count} registros")
        except Exception as e:
            print(f"❌ Error: {e}")
            backup_data['tables'][table_name] = []
            continue
    
    backup_data['metadata']['total_registros'] = total_records
    backup_data['metadata']['resumen'] = {
        table: len(data) for table, data in backup_data['tables'].items()
    }
    
    if dry_run:
        print(f"\n🔍 DRY RUN: Se guardarían {total_records} registros en {output_file}")
        print("\n📊 Resumen:")
        for table, count in backup_data['metadata']['resumen'].items():
            print(f"   - {table}: {count} registros")
        return {
            'success': True,
            'dry_run': True,
            'total_records': total_records,
            'summary': backup_data['metadata']['resumen']
        }
    
    # Guardar a archivo JSON
    output_path = Path(output_file)
    print(f"\n💾 Guardando backup en {output_path}...")
    
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(backup_data, f, ensure_ascii=False, indent=2, default=str)
        
        file_size_kb = output_path.stat().st_size / 1024
        print(f"✅ Backup guardado exitosamente: {output_path}")
        print(f"   Total de registros: {total_records}")
        print(f"   Tamaño del archivo: {file_size_kb:.2f} KB")
        print("\n📊 Resumen por tabla:")
        for table, count in backup_data['metadata']['resumen'].items():
            print(f"   - {table}: {count} registros")
        
        return {
            'success': True,
            'total_records': total_records,
            'file': str(output_path),
            'size_kb': file_size_kb,
            'summary': backup_data['metadata']['resumen']
        }
    except Exception as e:
        print(f"❌ Error guardando backup: {e}")
        return {
            'success': False,
            'error': str(e)
        }


def backup_to_sqlite(
    output_file: str = 'backup_supabase.db',
    dry_run: bool = False
) -> Dict[str, Any]:
    """
    Hace backup de todas las tablas de Supabase a un archivo SQLite
    """
    client = get_supabase_client()
    
    tables = [
        'obras',
        'comentarios',
        'validaciones',
        'historial_validaciones',
        'perfiles_usuarios'
    ]
    
    print("📥 Iniciando backup de Supabase a SQLite...")
    print(f"📊 Tablas a respaldar: {', '.join(tables)}\n")
    
    if dry_run:
        print(f"🔍 DRY RUN: Se crearía {output_file}")
        return {
            'success': True,
            'dry_run': True
        }
    
    output_path = Path(output_file)
    
    # Crear conexión SQLite
    conn = sqlite3.connect(output_path)
    cursor = conn.cursor()
    
    # Crear tabla de metadata
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS backup_metadata (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    ''')
    
    cursor.execute('''
        INSERT OR REPLACE INTO backup_metadata (key, value)
        VALUES (?, ?)
    ''', ('fecha_backup', datetime.now().isoformat()))
    
    cursor.execute('''
        INSERT OR REPLACE INTO backup_metadata (key, value)
        VALUES (?, ?)
    ''', ('fuente', 'Supabase'))
    
    total_records = 0
    
    for table_name in tables:
        print(f"📥 Cargando {table_name}...", end=' ')
        try:
            table_data = get_all_table_data(client, table_name)
            count = len(table_data)
            
            if count > 0:
                # Crear tabla SQLite
                # Primero necesitamos obtener la estructura de la primera fila
                first_row = table_data[0]
                columns = list(first_row.keys())
                
                # Crear tabla con columnas dinámicas
                column_defs = ', '.join([
                    f"{col} TEXT" for col in columns
                ])
                cursor.execute(f'''
                    CREATE TABLE IF NOT EXISTS {table_name} (
                        {column_defs}
                    )
                ''')
                
                # Insertar datos
                for row in table_data:
                    # Convertir valores a string para SQLite
                    values = [str(row.get(col, '')) if row.get(col) is not None else '' for col in columns]
                    placeholders = ', '.join(['?'] * len(columns))
                    cursor.execute(f'''
                        INSERT INTO {table_name} ({', '.join(columns)})
                        VALUES ({placeholders})
                    ''', values)
                
                conn.commit()
                total_records += count
                print(f"✅ {count} registros")
            else:
                print(f"⚠️ Sin datos")
        except Exception as e:
            print(f"❌ Error: {e}")
            continue
    
    conn.close()
    
    file_size_kb = output_path.stat().st_size / 1024
    print(f"\n✅ Backup SQLite guardado exitosamente: {output_path}")
    print(f"   Total de registros: {total_records}")
    print(f"   Tamaño del archivo: {file_size_kb:.2f} KB")
    
    return {
        'success': True,
        'total_records': total_records,
        'file': str(output_path),
        'size_kb': file_size_kb
    }


def main():
    parser = argparse.ArgumentParser(
        description='Hace backup completo de Supabase (todas las tablas)'
    )
    parser.add_argument(
        '--output',
        type=str,
        default='backup_supabase.json',
        help='Archivo de salida (default: backup_supabase.json)'
    )
    parser.add_argument(
        '--format',
        type=str,
        choices=['json', 'db', 'sqlite'],
        default='json',
        help='Formato de salida: json o db/sqlite (default: json)'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Simular backup sin guardar archivo'
    )
    
    args = parser.parse_args()
    
    # Determinar formato según extensión del archivo si no se especifica
    if args.format == 'json' and args.output.endswith('.db'):
        args.format = 'sqlite'
    elif args.format == 'json' and args.output.endswith('.sqlite'):
        args.format = 'sqlite'
    elif (args.format == 'sqlite' or args.format == 'db') and args.output.endswith('.json'):
        args.format = 'json'
    
    if args.format == 'json':
        result = backup_to_json(
            output_file=args.output,
            dry_run=args.dry_run
        )
    else:
        result = backup_to_sqlite(
            output_file=args.output,
            dry_run=args.dry_run
        )
    
    if result.get('success'):
        print("\n✅ Proceso completado exitosamente")
        sys.exit(0)
    else:
        print("\n❌ Proceso falló")
        sys.exit(1)


if __name__ == '__main__':
    main()
