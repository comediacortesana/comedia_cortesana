#!/usr/bin/env python
"""
Script para importar datos de CATCOM desde la carpeta de backup
"""

import os
import sys
import django
import json
from datetime import datetime
from pathlib import Path

# Configurar Django
sys.path.append(str(Path(__file__).parent.parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'teatro_espanol.settings')
django.setup()

from apps.obras.models import Obra, Manuscrito
from apps.autores.models import Autor
from apps.bibliografia.models import ReferenciaBibliografica


def clean_title(title):
    """Limpia y normaliza un título"""
    if not title:
        return ""
    
    # Remover caracteres extraños y normalizar espacios
    title = title.strip()
    title = title.replace('\n', ' ').replace('\r', ' ')
    # Remover múltiples espacios
    import re
    title = re.sub(r'\s+', ' ', title)
    return title


def extract_author_from_title(title):
    """Intenta extraer el autor del título si está incluido"""
    if not title:
        return None
    
    # Patrones comunes de autoría en títulos
    patterns = [
        r'^(.+?)\s+de\s+([A-Z][a-záéíóúñü]+(?:\s+[A-Z][a-záéíóúñü]+)*)$',
        r'^(.+?)\s+por\s+([A-Z][a-záéíóúñü]+(?:\s+[A-Z][a-záéíóúñü]+)*)$',
    ]
    
    import re
    for pattern in patterns:
        match = re.match(pattern, title)
        if match:
            return match.group(2).strip()
    
    return None


def import_catcom_from_backup():
    """Importa datos de CATCOM desde backup"""
    
    # Ruta al archivo JSON en backup
    backup_dir = Path(__file__).parent.parent / 'CATCOM_backup'
    json_path = backup_dir / 'all_works.json'
    
    if not json_path.exists():
        print(f"Error: No se encontró el archivo JSON en {json_path}")
        return
    
    print(f"Importando datos de CATCOM desde {json_path}")
    
    # Leer datos JSON
    with open(json_path, 'r', encoding='utf-8') as f:
        obras_data = json.load(f)
    
    print(f"Procesando {len(obras_data)} obras de CATCOM...")
    
    # Diccionarios para evitar duplicados
    autores_dict = {}
    obras_importadas = 0
    obras_duplicadas = 0
    
    for i, obra_data in enumerate(obras_data):
        try:
            if i % 100 == 0:
                print(f"  Procesando obra {i+1}/{len(obras_data)}...")
            
            # Extraer datos básicos
            titulo_original = obra_data.get('title', '')
            titulo_principal = obra_data.get('main_title', titulo_original)
            titulo_alternativo = obra_data.get('alternative_titles', [])
            
            # Limpiar títulos
            titulo_limpio = clean_title(titulo_principal)
            if not titulo_limpio:
                continue
            
            # Verificar si ya existe
            if Obra.objects.filter(titulo_limpio=titulo_limpio).exists():
                obras_duplicadas += 1
                continue
            
            # Extraer autor
            autor_nombre = None
            if 'author' in obra_data and obra_data['author']:
                autor_nombre = obra_data['author']
            else:
                # Intentar extraer del título
                autor_nombre = extract_author_from_title(titulo_original)
            
            # Crear o obtener autor
            autor = None
            if autor_nombre and autor_nombre.strip():
                autor_nombre_limpio = autor_nombre.strip()
                if autor_nombre_limpio not in autores_dict:
                    autor, created = Autor.objects.get_or_create(
                        nombre=autor_nombre_limpio,
                        defaults={
                            'epoca': 'Siglo de Oro',
                            'notas': 'Importado desde CATCOM backup'
                        }
                    )
                    autores_dict[autor_nombre_limpio] = autor
                    if created:
                        print(f"    Creado autor: {autor.nombre}")
                else:
                    autor = autores_dict[autor_nombre_limpio]
            
            # Determinar tipo de obra
            tipo_obra = 'comedia'  # Por defecto
            if any(word in titulo_original.lower() for word in ['auto', 'sacramental']):
                tipo_obra = 'auto'
            elif any(word in titulo_original.lower() for word in ['tragedia', 'tragedia']):
                tipo_obra = 'tragedia'
            elif any(word in titulo_original.lower() for word in ['entremés', 'entremes']):
                tipo_obra = 'entremes'
            elif any(word in titulo_original.lower() for word in ['zarzuela']):
                tipo_obra = 'zarzuela'
            
            # Crear obra
            obra = Obra.objects.create(
                titulo=clean_title(titulo_original),
                titulo_limpio=titulo_limpio,
                titulo_alternativo='; '.join(titulo_alternativo) if titulo_alternativo else '',
                autor=autor,
                tipo_obra=tipo_obra,
                fuente_principal='CATCOM',
                notas='Importado desde CATCOM backup'
            )
            
            obras_importadas += 1
            
            # Importar referencias bibliográficas si existen
            if 'bibliography' in obra_data and obra_data['bibliography']:
                for bib_ref in obra_data['bibliography']:
                    if isinstance(bib_ref, dict):
                        ReferenciaBibliografica.objects.create(
                            obra=obra,
                            tipo_referencia='bibliografia',
                            titulo=bib_ref.get('title', ''),
                            autor=bib_ref.get('author', ''),
                            editorial=bib_ref.get('publisher', ''),
                            fecha_publicacion=bib_ref.get('date', ''),
                            notas='Importado desde CATCOM'
                        )
                    elif isinstance(bib_ref, str):
                        ReferenciaBibliografica.objects.create(
                            obra=obra,
                            tipo_referencia='bibliografia',
                            titulo=bib_ref,
                            notas='Importado desde CATCOM'
                        )
        
        except Exception as e:
            print(f"Error procesando obra {i+1}: {e}")
            continue
    
    print(f"\nImportación completada:")
    print(f"  Obras importadas: {obras_importadas}")
    print(f"  Obras duplicadas (omitidas): {obras_duplicadas}")
    
    # Estadísticas finales
    print_stats()


def print_stats():
    """Imprime estadísticas de la importación"""
    print("\n" + "="*50)
    print("ESTADÍSTICAS DE IMPORTACIÓN - CATCOM")
    print("="*50)
    print(f"  Obras: {Obra.objects.filter(fuente_principal='CATCOM').count()}")
    print(f"  Autores: {Autor.objects.count()}")
    print(f"  Referencias bibliográficas: {ReferenciaBibliografica.objects.count()}")


if __name__ == '__main__':
    import_catcom_from_backup()
