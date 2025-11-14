"""
Script para sincronizar datos locales con Google Sheets
Uso: python scripts/sync_to_sheets.py [--dry-run] [--file datos.json]
"""

import argparse
import json
import sys
from pathlib import Path
from typing import List, Dict, Any
import os

try:
    from google.oauth2.credentials import Credentials
    from google.oauth2 import service_account
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
except ImportError:
    print("❌ Error: google-api-python-client no está instalado")
    print("   Instala con: pip install -r scripts/requirements.txt")
    sys.exit(1)

# Agregar el directorio padre al path para imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.validate import DataValidator
from dotenv import load_dotenv

load_dotenv()


def get_sheets_service():
    """Crea y retorna el servicio de Google Sheets"""
    credentials_file = os.getenv('GOOGLE_SHEETS_CREDENTIALS_FILE')
    if not credentials_file:
        raise ValueError("GOOGLE_SHEETS_CREDENTIALS_FILE debe estar en .env")
    
    credentials = service_account.Credentials.from_service_account_file(
        credentials_file,
        scopes=['https://www.googleapis.com/auth/spreadsheets']
    )
    
    return build('sheets', 'v4', credentials=credentials)


def obras_to_sheets_format(obras: List[Dict[str, Any]]) -> List[List[Any]]:
    """
    Convierte obras a formato de filas para Google Sheets
    """
    # Definir orden de columnas (debe coincidir con Google Sheets)
    columnas = [
        'id', 'titulo', 'titulo_original', 'titulo_alternativo',
        'tipo_obra', 'genero', 'subgenero', 'tema', 'idioma',
        'fecha_creacion', 'actos', 'versos',
        'musica_conservada', 'compositor', 'bibliotecas_musica', 'bibliografia_musica',
        'mecenas',
        'edicion_principe', 'notas_bibliograficas', 'manuscritos_conocidos', 'ediciones_conocidas',
        'fuente', 'origen_datos', 'pagina_pdf', 'texto_original_pdf',
        'notas', 'observaciones',
        # Campos de autor (se pueden expandir o mantener como JSON)
        'autor_nombre', 'autor_nombre_completo', 'autor_fecha_nacimiento',
        'autor_fecha_muerte', 'autor_epoca', 'autor_biografia'
    ]
    
    rows = []
    
    # Encabezados
    rows.append(columnas)
    
    # Datos
    for obra in obras:
        row = []
        for col in columnas:
            if col.startswith('autor_'):
                # Campo de autor anidado
                autor_field = col.replace('autor_', '')
                autor = obra.get('autor', {})
                if isinstance(autor, dict):
                    value = autor.get(autor_field, '')
                else:
                    value = autor if autor_field == 'nombre' else ''
            else:
                value = obra.get(col, '')
            
            # Convertir None a string vacío
            if value is None:
                value = ''
            elif isinstance(value, bool):
                value = 'Sí' if value else 'No'
            elif isinstance(value, (dict, list)):
                value = json.dumps(value, ensure_ascii=False)
            
            row.append(str(value))
        
        rows.append(row)
    
    return rows


def sync_to_sheets(
    obras: List[Dict[str, Any]],
    spreadsheet_id: str,
    sheet_name: str = 'Obras',
    dry_run: bool = False
) -> Dict[str, Any]:
    """
    Sincroniza obras a Google Sheets
    """
    validator = DataValidator()
    
    # Validar
    print("🔍 Validando datos...")
    validation_result = validator.validate_batch(obras)
    
    print(f"✅ Válidas: {validation_result['stats']['valid_count']}")
    print(f"❌ Inválidas: {validation_result['stats']['invalid_count']}")
    
    # Transformar
    obras_validas = [
        validator.transform_obra(item['obra']) 
        for item in validation_result['valid']
    ]
    
    if dry_run:
        print(f"\n🔍 DRY RUN: Se sincronizarían {len(obras_validas)} obras a Google Sheets")
        return {
            'success': True,
            'dry_run': True,
            'count': len(obras_validas)
        }
    
    # Convertir a formato de Sheets
    print(f"\n📤 Convirtiendo {len(obras_validas)} obras a formato de Sheets...")
    rows = obras_to_sheets_format(obras_validas)
    
    # Sincronizar
    print(f"📤 Sincronizando a Google Sheets...")
    try:
        service = get_sheets_service()
        
        # Limpiar hoja existente (opcional, comentar si quieres mantener datos)
        # service.spreadsheets().values().clear(
        #     spreadsheetId=spreadsheet_id,
        #     range=f'{sheet_name}!A:Z'
        # ).execute()
        
        # Escribir datos
        range_name = f'{sheet_name}!A1'
        body = {
            'values': rows
        }
        
        result = service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id,
            range=range_name,
            valueInputOption='RAW',
            body=body
        ).execute()
        
        print(f"✅ Sincronización completada: {result.get('updatedCells')} celdas actualizadas")
        
        return {
            'success': True,
            'count': len(obras_validas),
            'updated_cells': result.get('updatedCells')
        }
        
    except HttpError as error:
        print(f"❌ Error de Google Sheets API: {error}")
        return {
            'success': False,
            'error': str(error)
        }
    except Exception as e:
        print(f"❌ Error durante la sincronización: {e}")
        return {
            'success': False,
            'error': str(e)
        }


def main():
    parser = argparse.ArgumentParser(
        description='Sincroniza datos locales con Google Sheets'
    )
    parser.add_argument(
        '--file',
        type=str,
        default='datos_obras.json',
        help='Archivo JSON con los datos a sincronizar'
    )
    parser.add_argument(
        '--spreadsheet-id',
        type=str,
        help='ID de la hoja de cálculo (o usar GOOGLE_SHEETS_SPREADSHEET_ID en .env)'
    )
    parser.add_argument(
        '--sheet-name',
        type=str,
        default='Obras',
        help='Nombre de la hoja (default: Obras)'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Simular sincronización sin guardar cambios'
    )
    
    args = parser.parse_args()
    
    # Obtener spreadsheet_id
    spreadsheet_id = args.spreadsheet_id or os.getenv('GOOGLE_SHEETS_SPREADSHEET_ID')
    if not spreadsheet_id:
        print("❌ Debes proporcionar --spreadsheet-id o definir GOOGLE_SHEETS_SPREADSHEET_ID en .env")
        sys.exit(1)
    
    # Cargar datos
    file_path = Path(args.file)
    if not file_path.exists():
        print(f"❌ Archivo no encontrado: {file_path}")
        sys.exit(1)
    
    print(f"📂 Cargando datos desde {file_path}...")
    obras = load_json_file(str(file_path))
    print(f"📊 Total de obras cargadas: {len(obras)}")
    
    # Sincronizar
    result = sync_to_sheets(
        obras,
        spreadsheet_id=spreadsheet_id,
        sheet_name=args.sheet_name,
        dry_run=args.dry_run
    )
    
    if result['success']:
        print("\n✅ Proceso completado exitosamente")
        sys.exit(0)
    else:
        print("\n❌ Proceso falló")
        sys.exit(1)


def load_json_file(file_path: str) -> List[Dict[str, Any]]:
    """Carga datos desde un archivo JSON"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


if __name__ == '__main__':
    main()

