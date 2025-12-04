"""
Script para ejecutar migraciones de datos
Uso: python scripts/migrate_data.py [--migration nombre_migracion]
"""

import argparse
import sys
from pathlib import Path
from typing import Dict, Any, List

# Agregar el directorio padre al path para imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.supabase_client import SupabaseSync


class Migration:
    """Clase base para migraciones"""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
    
    def up(self, sync: SupabaseSync) -> Dict[str, Any]:
        """Ejecuta la migración"""
        raise NotImplementedError
    
    def down(self, sync: SupabaseSync) -> Dict[str, Any]:
        """Revierte la migración"""
        raise NotImplementedError


class MigrateSubtituloFromTituloAlternativo(Migration):
    """Migración: Copiar titulo_alternativo a subtitulo si subtitulo está vacío"""
    
    def __init__(self):
        super().__init__(
            'migrate_subtitulo',
            'Migra datos de titulo_alternativo a subtitulo'
        )
    
    def up(self, sync: SupabaseSync) -> Dict[str, Any]:
        """Ejecuta la migración"""
        print(f"🔄 Ejecutando migración: {self.description}")
        
        # Obtener todas las obras
        obras = sync.get_all_obras()
        print(f"📊 Total de obras: {len(obras)}")
        
        migradas = 0
        for obra in obras:
            if (not obra.get('subtitulo') and 
                obra.get('titulo_alternativo')):
                try:
                    sync.update_obra(obra['id'], {
                        'subtitulo': obra['titulo_alternativo']
                    })
                    migradas += 1
                except Exception as e:
                    print(f"⚠️  Error migrando obra {obra['id']}: {e}")
        
        print(f"✅ Migración completada: {migradas} obras migradas")
        return {
            'success': True,
            'migrated_count': migradas,
            'total_count': len(obras)
        }
    
    def down(self, sync: SupabaseSync) -> Dict[str, Any]:
        """Revierte la migración (no se puede revertir fácilmente)"""
        print("⚠️  Esta migración no se puede revertir automáticamente")
        return {'success': False, 'reason': 'No reversible'}


class MigrateAutorFromStringToObject(Migration):
    """Migración: Convertir autor de string a objeto"""
    
    def __init__(self):
        super().__init__(
            'migrate_autor_to_object',
            'Convierte autor de string a objeto anidado'
        )
    
    def up(self, sync: SupabaseSync) -> Dict[str, Any]:
        """Ejecuta la migración"""
        print(f"🔄 Ejecutando migración: {self.description}")
        
        obras = sync.get_all_obras()
        print(f"📊 Total de obras: {len(obras)}")
        
        migradas = 0
        for obra in obras:
            autor = obra.get('autor')
            if isinstance(autor, str) and autor:
                try:
                    sync.update_obra(obra['id'], {
                        'autor': {'nombre': autor}
                    })
                    migradas += 1
                except Exception as e:
                    print(f"⚠️  Error migrando obra {obra['id']}: {e}")
        
        print(f"✅ Migración completada: {migradas} obras migradas")
        return {
            'success': True,
            'migrated_count': migradas,
            'total_count': len(obras)
        }
    
    def down(self, sync: SupabaseSync) -> Dict[str, Any]:
        """Revierte la migración"""
        print(f"🔄 Revirtiendo migración: {self.description}")
        
        obras = sync.get_all_obras()
        revertidas = 0
        
        for obra in obras:
            autor = obra.get('autor')
            if isinstance(autor, dict) and autor.get('nombre'):
                try:
                    sync.update_obra(obra['id'], {
                        'autor': autor['nombre']
                    })
                    revertidas += 1
                except Exception as e:
                    print(f"⚠️  Error revirtiendo obra {obra['id']}: {e}")
        
        print(f"✅ Reversión completada: {revertidas} obras revertidas")
        return {
            'success': True,
            'reverted_count': revertidas
        }


# Registro de migraciones disponibles
AVAILABLE_MIGRATIONS: Dict[str, Migration] = {
    'migrate_subtitulo': MigrateSubtituloFromTituloAlternativo(),
    'migrate_autor_to_object': MigrateAutorFromStringToObject(),
}


def list_migrations():
    """Lista todas las migraciones disponibles"""
    print("📋 Migraciones disponibles:\n")
    for name, migration in AVAILABLE_MIGRATIONS.items():
        print(f"  {name}")
        print(f"    Descripción: {migration.description}\n")


def run_migration(migration_name: str, dry_run: bool = False) -> Dict[str, Any]:
    """Ejecuta una migración"""
    if migration_name not in AVAILABLE_MIGRATIONS:
        print(f"❌ Migración '{migration_name}' no encontrada")
        list_migrations()
        return {'success': False, 'reason': 'Migration not found'}
    
    migration = AVAILABLE_MIGRATIONS[migration_name]
    
    if dry_run:
        print(f"🔍 DRY RUN: Se ejecutaría la migración '{migration_name}'")
        print(f"   Descripción: {migration.description}")
        return {'success': True, 'dry_run': True}
    
    sync = SupabaseSync()
    return migration.up(sync)


def main():
    parser = argparse.ArgumentParser(
        description='Ejecuta migraciones de datos en Supabase'
    )
    parser.add_argument(
        '--migration',
        type=str,
        help='Nombre de la migración a ejecutar'
    )
    parser.add_argument(
        '--list',
        action='store_true',
        help='Lista todas las migraciones disponibles'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Simular migración sin ejecutar cambios'
    )
    
    args = parser.parse_args()
    
    if args.list:
        list_migrations()
        return
    
    if not args.migration:
        print("❌ Debes especificar una migración con --migration")
        print("\nUsa --list para ver migraciones disponibles")
        sys.exit(1)
    
    result = run_migration(args.migration, dry_run=args.dry_run)
    
    if result.get('success'):
        print("\n✅ Proceso completado exitosamente")
        sys.exit(0)
    else:
        print("\n❌ Proceso falló")
        sys.exit(1)


if __name__ == '__main__':
    main()

