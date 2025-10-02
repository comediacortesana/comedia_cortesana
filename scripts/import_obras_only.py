#!/usr/bin/env python
"""
Script para importar solo obras de FUENTESXI y CATCOM
"""

import os
import sys
import django
import sqlite3
import json
from pathlib import Path

# Configurar Django
sys.path.append(str(Path(__file__).parent.parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'teatro_espanol.settings')
django.setup()

from apps.obras.models import Obra
from apps.autores.models import Autor


def import_fuentesxi_obras():
    """Importa solo obras de FUENTESXI"""
    
    # Ruta a la base de datos
    backup_dir = Path(__file__).parent.parent / 'FUENTESXI_backup'
    db_path = backup_dir / 'teatro_espanol_mejorado.db'
    
    if not db_path.exists():
        print(f"Error: No se encontró la base de datos en {db_path}")
        return
    
    print(f"Importando obras de FUENTESXI desde {db_path}")
    
    # Conectar a la base de datos SQLite
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Importar autores
        print("Importando autores...")
        cursor.execute("SELECT DISTINCT autor FROM obras WHERE autor IS NOT NULL AND autor != ''")
        autores_data = cursor.fetchall()
        
        autores_dict = {}
        for (autor_nombre,) in autores_data:
            if autor_nombre and autor_nombre.strip():
                autor, created = Autor.objects.get_or_create(
                    nombre=autor_nombre.strip(),
                    defaults={
                        'epoca': 'Siglo de Oro',
                        'notas': 'Importado desde FUENTESXI'
                    }
                )
                autores_dict[autor_nombre] = autor
                if created:
                    print(f"  Creado autor: {autor.nombre}")
        
        # Importar obras
        print("Importando obras...")
        cursor.execute("""
            SELECT id, titulo, titulo_limpio, titulo_alternativo, autor, tipo_obra, 
                   edicion_principe, notas_bibliograficas, mecenas, musica_conservada, 
                   compositor, fuente_principal, tema, genero
            FROM obras
        """)
        obras_data = cursor.fetchall()
        
        obras_importadas = 0
        for obra_row in obras_data:
            (id_original, titulo, titulo_limpio, titulo_alternativo, autor_nombre, 
             tipo_obra, edicion_principe, notas_bibliograficas, mecenas, musica_conservada,
             compositor, fuente_principal, tema, genero) = obra_row
            
            # Obtener autor
            autor = autores_dict.get(autor_nombre) if autor_nombre else None
            
            # Crear obra
            obra, created = Obra.objects.get_or_create(
                titulo_limpio=titulo_limpio or titulo,
                defaults={
                    'titulo': titulo or '',
                    'titulo_alternativo': titulo_alternativo or '',
                    'autor': autor,
                    'tipo_obra': tipo_obra or 'comedia',
                    'genero': genero or '',
                    'edicion_principe': edicion_principe or '',
                    'notas_bibliograficas': notas_bibliograficas or '',
                    'fuente_principal': 'FUENTESXI',
                    'tema': tema or '',
                    'musica_conservada': bool(musica_conservada),
                    'compositor': compositor or '',
                    'mecenas': mecenas or ''
                }
            )
            if created:
                obras_importadas += 1
                if obras_importadas % 50 == 0:
                    print(f"  Importadas {obras_importadas} obras...")
        
        conn.close()
        print(f"Importación de FUENTESXI completada: {obras_importadas} obras nuevas")
        
    except Exception as e:
        print(f"Error durante la importación: {e}")
        conn.close()
        raise


def import_catcom_obras():
    """Importa solo obras de CATCOM"""
    
    # Ruta al archivo JSON
    backup_dir = Path(__file__).parent.parent / 'CATCOM_backup'
    json_path = backup_dir / 'all_works.json'
    
    if not json_path.exists():
        print(f"Error: No se encontró el archivo JSON en {json_path}")
        return
    
    print(f"Importando obras de CATCOM desde {json_path}")
    
    # Leer datos JSON
    with open(json_path, 'r', encoding='utf-8') as f:
        obras_data = json.load(f)
    
    print(f"Procesando {len(obras_data)} obras de CATCOM...")
    
    autores_dict = {}
    obras_importadas = 0
    
    for i, obra_data in enumerate(obras_data):
        try:
            if i % 500 == 0:
                print(f"  Procesando obra {i+1}/{len(obras_data)}...")
            
            # Extraer datos básicos
            titulo_original = obra_data.get('title', '')
            titulo_principal = obra_data.get('main_title', titulo_original)
            
            if not titulo_principal or not titulo_principal.strip():
                continue
            
            titulo_limpio = titulo_principal.strip()
            
            # Verificar si ya existe
            if Obra.objects.filter(titulo_limpio=titulo_limpio).exists():
                continue
            
            # Extraer autor
            autor_nombre = None
            if 'author' in obra_data and obra_data['author']:
                autor_nombre = obra_data['author']
            
            # Crear o obtener autor
            autor = None
            if autor_nombre and autor_nombre.strip():
                autor_nombre_limpio = autor_nombre.strip()
                if autor_nombre_limpio not in autores_dict:
                    autor, created = Autor.objects.get_or_create(
                        nombre=autor_nombre_limpio,
                        defaults={
                            'epoca': 'Siglo de Oro',
                            'notas': 'Importado desde CATCOM'
                        }
                    )
                    autores_dict[autor_nombre_limpio] = autor
                else:
                    autor = autores_dict[autor_nombre_limpio]
            
            # Crear obra
            obra = Obra.objects.create(
                titulo=titulo_limpio,
                titulo_limpio=titulo_limpio,
                autor=autor,
                tipo_obra='comedia',
                fuente_principal='CATCOM',
                notas='Importado desde CATCOM backup'
            )
            
            obras_importadas += 1
            
        except Exception as e:
            print(f"Error procesando obra {i+1}: {e}")
            continue
    
    print(f"Importación de CATCOM completada: {obras_importadas} obras nuevas")


def print_stats():
    """Imprime estadísticas finales"""
    print("\n" + "="*50)
    print("ESTADÍSTICAS FINALES")
    print("="*50)
    print(f"  Obras totales: {Obra.objects.count()}")
    print(f"    - FUENTESXI: {Obra.objects.filter(fuente_principal='FUENTESXI').count()}")
    print(f"    - CATCOM: {Obra.objects.filter(fuente_principal='CATCOM').count()}")
    print(f"  Autores: {Autor.objects.count()}")


if __name__ == '__main__':
    import_fuentesxi_obras()
    import_catcom_obras()
    print_stats()
