"""
Script para sincronizar datos locales con Supabase
Uso: python scripts/sync_to_supabase.py [--dry-run] [--file datos.json]
"""

import argparse
import json
import sys
from pathlib import Path
from typing import List, Dict, Any

# Agregar el directorio padre al path para imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.supabase_client import SupabaseSync
from scripts.validate import DataValidator


def load_json_file(file_path: str) -> List[Dict[str, Any]]:
    """Carga datos desde un archivo JSON"""
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Manejar formato con metadata
    if isinstance(data, dict) and 'obras' in data:
        obras = data['obras']
    elif isinstance(data, list):
        obras = data
    else:
        raise ValueError("Formato de JSON no reconocido")
    
    # Normalizar nombres de campos (convertir español con mayúsculas a minúsculas)
    obras_normalizadas = []
    for obra in obras:
        obra_norm = {}
        for key, value in obra.items():
            # Mapear nombres en español a nombres en minúsculas
            key_mapping = {
                'ID': 'id',
                'Título': 'titulo',
                'Título Original': 'titulo_original',
                'Títulos Alternativos': 'titulo_alternativo',
                'Autor': 'autor_nombre',  # Temporal, se manejará después
                'Autor Nombre Completo': 'autor_nombre_completo',
                'Autor Nacimiento': 'autor_fecha_nacimiento',
                'Autor Muerte': 'autor_fecha_muerte',
                'Autor Época': 'autor_epoca',
                'Autor Biografía': 'autor_biografia',
                'Tipo de Obra': 'tipo_obra',
                'Género': 'genero',
                'Subgénero': 'subgenero',
                'Tema': 'tema',
                'Fuente Principal': 'fuente',
                'Origen de Datos': 'origen_datos',
                'Página PDF': 'pagina_pdf',
                'Número de Actos': 'actos',
                'Número de Versos': 'versos',
                'Idioma': 'idioma',
                'Fecha de Creación': 'fecha_creacion',
                'Música Conservada': 'musica_conservada',
                'Compositor': 'compositor',
                'Bibliotecas con Música': 'bibliotecas_musica',
                'Bibliografía Musical': 'bibliografia_musica',
                'Mecenas': 'mecenas',
                'Edición Príncipe': 'edicion_principe',
                'Notas Bibliográficas': 'notas_bibliograficas',
                'Manuscritos Conocidos': 'manuscritos_conocidos',
                'Ediciones Conocidas': 'ediciones_conocidas',
                'Notas': 'notas',
                'Observaciones': 'observaciones'
            }
            
            # Usar mapeo si existe, sino convertir a minúsculas y reemplazar espacios
            new_key = key_mapping.get(key)
            if not new_key:
                # Convertir a minúsculas y reemplazar espacios con guiones bajos
                new_key = key.lower().replace(' ', '_').replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u')
            
            # Convertir valores especiales
            if new_key == 'musica_conservada':
                # Convertir "No"/"Sí" a booleano
                if isinstance(value, str):
                    obra_norm[new_key] = value.lower() in ['sí', 'si', 'yes', 'true', '1']
                else:
                    obra_norm[new_key] = bool(value)
            elif new_key in ['actos', 'versos'] and value:
                # Convertir a entero si es posible
                try:
                    obra_norm[new_key] = int(value)
                except (ValueError, TypeError):
                    obra_norm[new_key] = value
            elif new_key == 'pagina_pdf' and value is not None:
                # Convertir a string si es numérico
                obra_norm[new_key] = str(value)
            else:
                obra_norm[new_key] = value
        
        # Construir objeto autor si hay campos de autor
        # Primero eliminar campos planos de autor que no deben ir a Supabase
        autor = {}
        campos_autor_planos = [
            'autor_nombre', 'autor_nombre_completo', 'autor_fecha_nacimiento',
            'autor_fecha_muerte', 'autor_epoca', 'autor_biografia'
        ]
        
        for campo in campos_autor_planos:
            valor = obra_norm.pop(campo, None)
            if valor is not None and valor != '':
                # Mapear nombre del campo plano al nombre en el objeto autor
                campo_autor = campo.replace('autor_', '')
                if campo == 'autor_nombre':
                    autor['nombre'] = valor
                elif campo == 'autor_nombre_completo':
                    autor['nombre_completo'] = valor
                elif campo == 'autor_fecha_nacimiento':
                    autor['fecha_nacimiento'] = valor
                elif campo == 'autor_fecha_muerte':
                    autor['fecha_muerte'] = valor
                elif campo == 'autor_epoca':
                    autor['epoca'] = valor
                elif campo == 'autor_biografia':
                    autor['biografia'] = valor
        
        # Solo agregar objeto autor si tiene contenido real (no vacío)
        if autor:
            obra_norm['autor'] = autor
        # Si no hay autor, asegurar que no exista el campo (o sea null)
        elif 'autor' not in obra_norm:
            obra_norm['autor'] = None
        
        obras_normalizadas.append(obra_norm)
    
    return obras_normalizadas


def sync_obras_to_supabase(
    obras: List[Dict[str, Any]], 
    dry_run: bool = False,
    batch_size: int = 100
) -> Dict[str, Any]:
    """
    Sincroniza obras a Supabase
    """
    validator = DataValidator()
    sync = SupabaseSync()
    
    # Validar todas las obras
    print("🔍 Validando datos...")
    validation_result = validator.validate_batch(obras)
    
    print(f"✅ Válidas: {validation_result['stats']['valid_count']}")
    print(f"❌ Inválidas: {validation_result['stats']['invalid_count']}")
    
    if validation_result['invalid']:
        print("\n⚠️  Obras con errores:")
        for invalid in validation_result['invalid'][:5]:  # Mostrar solo las primeras 5
            obra = invalid.get('obra', {})
            if isinstance(obra, dict):
                obra_id = obra.get('id') or obra.get('ID') or obra.get('Id') or 'N/A'
            else:
                obra_id = str(obra) if obra else 'N/A'
            errors = invalid.get('errors', [])
            error_msg = ', '.join(errors[:2]) if isinstance(errors, list) else str(errors)
            print(f"  - ID {obra_id}: {error_msg}")
        if len(validation_result['invalid']) > 5:
            print(f"  ... y {len(validation_result['invalid']) - 5} más")
    
    if not dry_run and validation_result['invalid']:
        respuesta = input("\n¿Continuar solo con las obras válidas? (s/n): ")
        if respuesta.lower() != 's':
            print("❌ Sincronización cancelada")
            return {'success': False, 'reason': 'Usuario canceló'}
    
    # Transformar obras válidas
    # La normalización ya elimina campos planos de autor y los agrupa en objeto autor
    obras_validas = [
        validator.transform_obra(item['obra']) 
        for item in validation_result['valid']
    ]
    
    # Asegurar que no queden campos planos de autor (por si acaso)
    campos_autor_planos = [
        'autor_nombre', 'autor_nombre_completo', 'autor_fecha_nacimiento',
        'autor_fecha_muerte', 'autor_epoca', 'autor_biografia'
    ]
    for obra in obras_validas:
        for campo in campos_autor_planos:
            obra.pop(campo, None)  # Eliminar si existe
    
    if dry_run:
        print(f"\n🔍 DRY RUN: Se sincronizarían {len(obras_validas)} obras")
        return {
            'success': True,
            'dry_run': True,
            'count': len(obras_validas),
            'validation': validation_result['stats']
        }
    
    # Sincronizar
    print(f"\n📤 Sincronizando {len(obras_validas)} obras a Supabase...")
    try:
        results = sync.upsert_multiple_obras(obras_validas, batch_size=batch_size)
        print(f"✅ Sincronización completada: {len(results)} obras procesadas")
        
        return {
            'success': True,
            'count': len(results),
            'validation': validation_result['stats']
        }
    except Exception as e:
        print(f"❌ Error durante la sincronización: {e}")
        return {
            'success': False,
            'error': str(e)
        }


def main():
    parser = argparse.ArgumentParser(
        description='Sincroniza datos locales con Supabase'
    )
    parser.add_argument(
        '--file',
        type=str,
        default='datos_obras.json',
        help='Archivo JSON con los datos a sincronizar'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Simular sincronización sin guardar cambios'
    )
    parser.add_argument(
        '--batch-size',
        type=int,
        default=100,
        help='Tamaño del lote para sincronización (default: 100)'
    )
    
    args = parser.parse_args()
    
    # Cargar datos
    file_path = Path(args.file)
    if not file_path.exists():
        print(f"❌ Archivo no encontrado: {file_path}")
        sys.exit(1)
    
    print(f"📂 Cargando datos desde {file_path}...")
    obras = load_json_file(str(file_path))
    print(f"📊 Total de obras cargadas: {len(obras)}")
    
    # Sincronizar
    result = sync_obras_to_supabase(
        obras, 
        dry_run=args.dry_run,
        batch_size=args.batch_size
    )
    
    if result['success']:
        print("\n✅ Proceso completado exitosamente")
        sys.exit(0)
    else:
        print("\n❌ Proceso falló")
        sys.exit(1)


if __name__ == '__main__':
    main()

