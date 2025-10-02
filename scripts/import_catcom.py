#!/usr/bin/env python
"""
Script para importar datos de CATCOM (archivos JSON) a Django
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
from apps.representaciones.models import Representacion
from apps.autores.models import Autor
from apps.lugares.models import Lugar
from apps.bibliografia.models import ReferenciaBibliografica


def import_catcom_data():
    """Importa datos de los archivos JSON de CATCOM"""
    
    # Ruta a los datos de CATCOM
    data_dir = Path(__file__).parent.parent / 'data' / 'catcom'
    
    if not data_dir.exists():
        print(f"Error: No se encontró el directorio de datos en {data_dir}")
        return
    
    print(f"Importando datos de {data_dir}")
    
    # Importar desde all_works.json
    all_works_path = data_dir / 'all_works.json'
    
    if not all_works_path.exists():
        print(f"Error: No se encontró el archivo {all_works_path}")
        return
    
    with open(all_works_path, 'r', encoding='utf-8') as f:
        obras_data = json.load(f)
    
    print(f"Procesando {len(obras_data)} obras de CATCOM...")
    
    # Diccionarios para evitar duplicados
    autores_dict = {}
    lugares_dict = {}
    obras_dict = {}
    
    for obra_data in obras_data:
        try:
            # Procesar autor
            autor_obj = None
            if 'attribution' in obra_data and obra_data['attribution']:
                # Extraer nombre del autor de la atribución
                attribution = obra_data['attribution']
                if 'Anónimo' not in attribution:
                    # Buscar nombres de autores conocidos
                    autores_conocidos = [
                        'Calderón', 'Lope de Vega', 'Moreto', 'Rojas Zorrilla', 
                        'Diamante', 'Matos Fragoso', 'Bances Candamo', 'Solís'
                    ]
                    for autor_nombre in autores_conocidos:
                        if autor_nombre in attribution:
                            if autor_nombre not in autores_dict:
                                autor_obj, created = Autor.objects.get_or_create(
                                    nombre=autor_nombre,
                                    defaults={
                                        'epoca': 'Siglo de Oro',
                                        'notas': 'Importado desde CATCOM'
                                    }
                                )
                                autores_dict[autor_nombre] = autor_obj
                                if created:
                                    print(f"  Creado autor: {autor_obj.nombre}")
                            else:
                                autor_obj = autores_dict[autor_nombre]
                            break
            
            # Crear o obtener obra
            titulo = obra_data.get('title', obra_data.get('main_title', ''))
            if not titulo:
                continue
            
            titulo_limpio = titulo.strip()
            genero = obra_data.get('genre', 'Comedia')
            
            # Mapear géneros
            genero_map = {
                'Comedia': 'comedia',
                'Auto': 'auto',
                'Zarzuela': 'zarzuela',
                'Entremés': 'entremes',
                'Tragedia': 'tragedia',
                'Loa': 'loa',
                'Sainete': 'sainete',
                'Baile': 'baile'
            }
            tipo_obra = genero_map.get(genero, 'comedia')
            
            obra, created = Obra.objects.get_or_create(
                titulo_limpio=titulo_limpio,
                defaults={
                    'titulo': titulo,
                    'autor': autor_obj,
                    'tipo_obra': tipo_obra,
                    'genero': genero,
                    'fuente_principal': 'CATCOM',
                    'idioma': 'Español',
                    'notas': f"Importado desde CATCOM. URL: {obra_data.get('url', '')}"
                }
            )
            
            if created:
                print(f"  Creada obra: {obra.titulo_limpio}")
            
            # Procesar representaciones
            if 'performances' in obra_data:
                for perf_data in obra_data['performances']:
                    lugar_nombre = perf_data.get('lugar', '')
                    if lugar_nombre:
                        # Crear o obtener lugar
                        if lugar_nombre not in lugares_dict:
                            lugar_obj, created = Lugar.objects.get_or_create(
                                nombre=lugar_nombre,
                                defaults={
                                    'pais': 'España',
                                    'tipo_lugar': 'otro',
                                    'notas_historicas': 'Importado desde CATCOM'
                                }
                            )
                            lugares_dict[lugar_nombre] = lugar_obj
                            if created:
                                print(f"  Creado lugar: {lugar_obj.nombre}")
                        else:
                            lugar_obj = lugares_dict[lugar_nombre]
                        
                        # Crear representación
                        Representacion.objects.get_or_create(
                            obra=obra,
                            fecha='',
                            lugar=lugar_obj,
                            tipo_lugar=perf_data.get('espacio', ''),
                            observaciones=perf_data.get('noticia', ''),
                            fuente='CATCOM'
                        )
            
            # Procesar referencias bibliográficas
            if 'bibliography' in obra_data:
                for biblio_item in obra_data['bibliography']:
                    if isinstance(biblio_item, str) and biblio_item.strip():
                        # Parsear la referencia bibliográfica
                        parts = biblio_item.split(':')
                        if len(parts) >= 2:
                            autor_ref = parts[0].strip()
                            titulo_ref = ':'.join(parts[1:]).strip()
                            
                            ReferenciaBibliografica.objects.get_or_create(
                                obra=obra,
                                titulo=titulo_ref,
                                autor=autor_ref,
                                tipo_referencia='libro',
                                fuente='CATCOM'
                            )
            
        except Exception as e:
            print(f"Error procesando obra {obra_data.get('title', 'Unknown')}: {e}")
            continue
    
    print("Importación de CATCOM completada exitosamente!")
    
    # Estadísticas
    print(f"\nEstadísticas de importación:")
    print(f"  Autores: {Autor.objects.count()}")
    print(f"  Lugares: {Lugar.objects.count()}")
    print(f"  Obras: {Obra.objects.count()}")
    print(f"  Representaciones: {Representacion.objects.count()}")
    print(f"  Referencias bibliográficas: {ReferenciaBibliografica.objects.count()}")


if __name__ == '__main__':
    import_catcom_data()
