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
            # Primero intentar cargar representaciones extraídas
            representaciones_extraidas = {}
            extraidas_file = Path(__file__).parent.parent / 'data' / 'CATCOM' / 'representaciones_extraidas.json'
            if extraidas_file.exists():
                try:
                    with open(extraidas_file, 'r', encoding='utf-8') as f:
                        extraidas_data = json.load(f)
                    # Crear índice por título de obra
                    for rep in extraidas_data.get('representaciones', []):
                        rep_titulo = rep.get('obra_titulo', '').lower().strip()
                        if rep_titulo not in representaciones_extraidas:
                            representaciones_extraidas[rep_titulo] = []
                        representaciones_extraidas[rep_titulo].append(rep)
                except Exception as e:
                    print(f"  ⚠️ No se pudieron cargar representaciones extraídas: {e}")
            
            if 'performances' in obra_data:
                titulo_lower = titulo_limpio.lower()
                reps_extraidas = representaciones_extraidas.get(titulo_lower, [])
                
                for idx, perf_data in enumerate(obra_data['performances']):
                    lugar_nombre = perf_data.get('lugar', '')
                    if not lugar_nombre:
                        continue
                    
                    # Buscar representación extraída correspondiente (por índice o por lugar)
                    rep_extraida = None
                    if idx < len(reps_extraidas):
                        rep_extraida = reps_extraidas[idx]
                    else:
                        # Buscar por lugar
                        lugar_limpio = lugar_nombre.split('(')[0].strip().lower()
                        for rep in reps_extraidas:
                            if lugar_limpio in rep.get('lugar_nombre', '').lower():
                                rep_extraida = rep
                                break
                    
                    # Crear o obtener lugar
                    lugar_final = rep_extraida.get('lugar_nombre', lugar_nombre) if rep_extraida else lugar_nombre
                    if lugar_final not in lugares_dict:
                        lugar_obj, created = Lugar.objects.get_or_create(
                            nombre=lugar_final,
                            defaults={
                                'pais': 'España',
                                'region': rep_extraida.get('lugar_region', '') if rep_extraida else '',
                                'tipo_lugar': rep_extraida.get('lugar_tipo', 'otro') if rep_extraida else 'otro',
                                'notas_historicas': 'Importado desde CATCOM'
                            }
                        )
                        lugares_dict[lugar_final] = lugar_obj
                        if created:
                            print(f"  Creado lugar: {lugar_obj.nombre}")
                    else:
                        lugar_obj = lugares_dict[lugar_final]
                    
                    # Extraer fecha y compañía
                    fecha_str = ''
                    fecha_formateada = None
                    compania = ''
                    
                    if rep_extraida:
                        fecha_str = rep_extraida.get('fecha', '')
                        fecha_formateada_str = rep_extraida.get('fecha_formateada', '')
                        if fecha_formateada_str:
                            try:
                                fecha_formateada = datetime.strptime(fecha_formateada_str, '%Y-%m-%d').date()
                            except:
                                pass
                        compania = rep_extraida.get('compañia', '')
                    
                    # Si no hay fecha extraída, intentar extraer del texto
                    if not fecha_str:
                        noticia = perf_data.get('noticia', '')
                        # Buscar patrón básico de fecha
                        import re
                        fecha_match = re.search(r'(\d{1,2}\s+de\s+\w+\s+de\s+\d{4})', noticia, re.IGNORECASE)
                        if fecha_match:
                            fecha_str = fecha_match.group(1)
                    
                    # Si no hay compañía extraída, intentar extraer del texto
                    if not compania:
                        noticia = perf_data.get('noticia', '')
                        compania_match = re.search(r'compañía\s+de\s+([^\.]+?)(?:\.|,|$)', noticia, re.IGNORECASE)
                        if compania_match:
                            compania = compania_match.group(1).strip()
                    
                    # Determinar tipo de lugar
                    tipo_lugar = perf_data.get('espacio', '')
                    if rep_extraida and rep_extraida.get('lugar_tipo'):
                        tipo_lugar = rep_extraida.get('lugar_tipo')
                    elif not tipo_lugar or tipo_lugar == 'Ø':
                        tipo_lugar = ''
                    
                    # Crear representación
                    Representacion.objects.get_or_create(
                        obra=obra,
                        fecha=fecha_str,
                        lugar=lugar_obj,
                        defaults={
                            'fecha_formateada': fecha_formateada,
                            'tipo_lugar': tipo_lugar,
                            'compañia': compania,
                            'observaciones': perf_data.get('noticia', ''),
                            'fuente': 'CATCOM'
                        }
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
