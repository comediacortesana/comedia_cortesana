#!/usr/bin/env python3
"""
Script para procesar los archivos de texto extraído del PDF FUENTES IX 1
y crear las referencias de página en la base de datos.
"""

import os
import re
import django
from pathlib import Path

# Configurar Django
import sys
sys.path.append('/Users/ivansimo/Documents/2025/ITEM/DELIA_DJANGO')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'teatro_espanol.settings')
django.setup()

from apps.obras.models import PaginaPDF
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import shutil

def process_text_files():
    """Procesa todos los archivos de texto extraído y crea las páginas PDF"""
    
    # Ruta a los archivos de texto extraído
    texto_dir = Path('/Users/ivansimo/Documents/2025/ITEM/DELIA_DJANGO/FUENTESXI_backup/texto_extraido')
    
    # Ruta a las imágenes
    images_dir = Path('/Users/ivansimo/Documents/2025/ITEM/DELIA_DJANGO/FUENTESXI_backup/images_for_claude')
    
    # Crear directorio para las imágenes en media
    media_pages_dir = Path('/Users/ivansimo/Documents/2025/ITEM/DELIA_DJANGO/media/pdf_pages')
    media_pages_dir.mkdir(exist_ok=True)
    
    # Patrón para extraer número de página
    page_pattern = re.compile(r'^--- PÁGINA (\d+) ---$')
    
    # Procesar cada archivo de texto
    for txt_file in texto_dir.glob('*_texto_extraido.txt'):
        print(f"Procesando: {txt_file.name}")
        
        # Extraer información del nombre del archivo
        part_match = re.search(r'part_(\d+)', txt_file.name)
        if not part_match:
            continue
            
        part_number = int(part_match.group(1))
        part_file = f"part_{part_number:03d}"
        
        # Calcular offset de páginas (cada parte tiene 25 páginas, excepto la última)
        page_offset = (part_number - 1) * 25
        
        # Buscar directorio de imágenes correspondiente
        images_part_dir = images_dir / f"FUENTES IX 1_{part_file}_ALL_PAGES"
        
        with open(txt_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Dividir por páginas
        pages = content.split('--- PÁGINA')
        
        for page_content in pages[1:]:  # Saltar el primer elemento vacío
            lines = page_content.strip().split('\n')
            if not lines:
                continue
                
            # Extraer número de página de la primera línea
            first_line = lines[0].strip()
            page_match = page_pattern.match(f'--- PÁGINA {first_line} ---')
            if not page_match:
                # Intentar extraer número directamente
                number_match = re.search(r'(\d+)', first_line)
                if not number_match:
                    continue
                local_page_number = int(number_match.group(1))
            else:
                local_page_number = int(page_match.group(1))
            
            # Calcular número de página global
            page_number = page_offset + local_page_number
            
            # Obtener texto de la página (sin el marcador)
            page_text = '\n'.join(lines[1:]).strip()
            
            # Buscar imagen correspondiente (usar número local para el archivo)
            image_filename = f"page_{local_page_number:03d}.png"
            source_image_path = images_part_dir / image_filename
            
            # Copiar imagen a media si existe (usar número global para el nombre final)
            target_image_filename = f"page_{page_number:03d}.png"
            target_image_path = None
            if source_image_path.exists():
                target_image_path = media_pages_dir / target_image_filename
                shutil.copy2(source_image_path, target_image_path)
                print(f"  Copiada imagen: {target_image_filename}")
            
            # Crear o actualizar registro en la base de datos
            pagina, created = PaginaPDF.objects.get_or_create(
                numero_pagina=page_number,
                defaults={
                    'texto_extraido': page_text,
                    'archivo_imagen': target_image_filename if target_image_path else '',
                    'part_file': part_file
                }
            )
            
            if not created:
                # Actualizar si ya existe
                pagina.texto_extraido = page_text
                pagina.archivo_imagen = target_image_filename if target_image_path else ''
                pagina.part_file = part_file
                pagina.save()
            
            print(f"  Página {page_number}: {'Creada' if created else 'Actualizada'}")
    
    print(f"\nProcesamiento completado. Total de páginas: {PaginaPDF.objects.count()}")

def create_page_mapping():
    """Crea un mapeo de páginas para facilitar búsquedas"""
    
    print("\nCreando mapeo de páginas...")
    
    # Crear un archivo de mapeo para referencia
    mapping_file = Path('/Users/ivansimo/Documents/2025/ITEM/DELIA_DJANGO/data/pdf_page_mapping.json')
    
    import json
    
    mapping = {}
    for pagina in PaginaPDF.objects.all().order_by('numero_pagina'):
        mapping[pagina.numero_pagina] = {
            'texto_preview': pagina.texto_extraido[:200] + '...' if len(pagina.texto_extraido) > 200 else pagina.texto_extraido,
            'archivo_imagen': pagina.archivo_imagen,
            'part_file': pagina.part_file,
            'ruta_imagen': pagina.ruta_imagen_completa
        }
    
    with open(mapping_file, 'w', encoding='utf-8') as f:
        json.dump(mapping, f, indent=2, ensure_ascii=False)
    
    print(f"Mapeo guardado en: {mapping_file}")

if __name__ == '__main__':
    print("Iniciando procesamiento de páginas PDF...")
    process_text_files()
    create_page_mapping()
    print("¡Procesamiento completado!")
