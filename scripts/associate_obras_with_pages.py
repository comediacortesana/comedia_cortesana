#!/usr/bin/env python3
"""
Script para asociar obras con páginas del PDF basándose en el texto extraído.
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

from apps.obras.models import Obra, PaginaPDF
from apps.representaciones.models import Representacion
from django.db.models import Q

def find_obra_in_text(texto, obra):
    """Busca una obra específica en el texto de una página"""
    # Normalizar texto para búsqueda
    texto_normalizado = texto.lower().strip()
    titulo_normalizado = obra.titulo_limpio.lower().strip()
    
    # Buscar coincidencias exactas
    if titulo_normalizado in texto_normalizado:
        return True
    
    # Buscar variaciones del título
    titulo_palabras = titulo_normalizado.split()
    if len(titulo_palabras) >= 2:
        # Buscar al menos 2 palabras del título
        palabras_encontradas = sum(1 for palabra in titulo_palabras if palabra in texto_normalizado)
        if palabras_encontradas >= min(2, len(titulo_palabras)):
            return True
    
    return False

def associate_obras_with_pages():
    """Asocia obras con páginas del PDF basándose en el contenido"""
    
    print("Iniciando asociación de obras con páginas del PDF...")
    
    # Obtener todas las páginas del PDF
    paginas = PaginaPDF.objects.all().order_by('numero_pagina')
    print(f"Total de páginas: {paginas.count()}")
    
    # Obtener todas las obras de FUENTESXI
    obras = Obra.objects.filter(fuente_principal='FUENTESXI')
    print(f"Total de obras FUENTESXI: {obras.count()}")
    
    asociaciones = 0
    
    for obra in obras:
        print(f"\nBuscando: {obra.titulo_limpio}")
        
        # Buscar en todas las páginas
        for pagina in paginas:
            if find_obra_in_text(pagina.texto_extraido, obra):
                # Asociar obra con página
                obra.pagina_pdf = pagina.numero_pagina
                obra.origen_datos = 'pdf'
                obra.texto_original_pdf = pagina.texto_extraido[:500] + '...' if len(pagina.texto_extraido) > 500 else pagina.texto_extraido
                obra.save()
                
                print(f"  ✓ Asociada con página {pagina.numero_pagina}")
                asociaciones += 1
                break
        else:
            print(f"  ✗ No encontrada en ninguna página")
    
    print(f"\nAsociaciones completadas: {asociaciones}")
    
    # Estadísticas finales
    obras_con_pagina = Obra.objects.filter(pagina_pdf__isnull=False).count()
    print(f"Obras con página asociada: {obras_con_pagina}")
    
    return asociaciones

def associate_representaciones_with_pages():
    """Asocia representaciones con páginas del PDF"""
    
    print("\nIniciando asociación de representaciones con páginas del PDF...")
    
    # Obtener representaciones que no tienen página asociada
    representaciones = Representacion.objects.filter(pagina_pdf__isnull=True)
    print(f"Representaciones sin página: {representaciones.count()}")
    
    asociaciones = 0
    
    for representacion in representaciones:
        # Si la obra tiene página asociada, usar la misma página
        if representacion.obra.pagina_pdf:
            representacion.pagina_pdf = representacion.obra.pagina_pdf
            representacion.texto_original_pdf = representacion.obra.texto_original_pdf
            representacion.save()
            asociaciones += 1
    
    print(f"Representaciones asociadas: {asociaciones}")
    return asociaciones

def create_page_search_index():
    """Crea un índice de búsqueda para páginas"""
    
    print("\nCreando índice de búsqueda...")
    
    # Crear archivo de índice
    index_file = Path('/Users/ivansimo/Documents/2025/ITEM/DELIA_DJANGO/data/page_search_index.json')
    
    import json
    
    index = {}
    for pagina in PaginaPDF.objects.all():
        # Extraer palabras clave del texto
        texto = pagina.texto_extraido.lower()
        palabras = re.findall(r'\b\w{3,}\b', texto)  # Palabras de 3+ caracteres
        
        # Contar frecuencia de palabras
        from collections import Counter
        word_count = Counter(palabras)
        
        # Guardar las 20 palabras más frecuentes
        top_words = [word for word, count in word_count.most_common(20)]
        
        index[pagina.numero_pagina] = {
            'texto_preview': pagina.texto_extraido[:200] + '...' if len(pagina.texto_extraido) > 200 else pagina.texto_extraido,
            'palabras_clave': top_words,
            'archivo_imagen': pagina.archivo_imagen,
            'part_file': pagina.part_file
        }
    
    with open(index_file, 'w', encoding='utf-8') as f:
        json.dump(index, f, indent=2, ensure_ascii=False)
    
    print(f"Índice guardado en: {index_file}")

if __name__ == '__main__':
    print("Iniciando proceso de asociación...")
    
    # Asociar obras con páginas
    obras_asociadas = associate_obras_with_pages()
    
    # Asociar representaciones con páginas
    representaciones_asociadas = associate_representaciones_with_pages()
    
    # Crear índice de búsqueda
    create_page_search_index()
    
    print(f"\n¡Proceso completado!")
    print(f"Obras asociadas: {obras_asociadas}")
    print(f"Representaciones asociadas: {representaciones_asociadas}")
