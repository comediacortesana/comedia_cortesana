#!/usr/bin/env python3
"""
Script para probar la funcionalidad de páginas del PDF
"""

import os
import django
from pathlib import Path

# Configurar Django
import sys
sys.path.append('/Users/ivansimo/Documents/2025/ITEM/DELIA_DJANGO')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'teatro_espanol.settings')
django.setup()

from apps.obras.models import Obra, PaginaPDF

def test_pdf_pages():
    """Prueba la funcionalidad de páginas del PDF"""
    
    print("=== PRUEBA DE FUNCIONALIDAD DE PÁGINAS PDF ===\n")
    
    # 1. Verificar que las páginas existen
    total_paginas = PaginaPDF.objects.count()
    print(f"1. Total de páginas en la base de datos: {total_paginas}")
    
    # 2. Verificar que las imágenes existen
    paginas_con_imagen = PaginaPDF.objects.exclude(archivo_imagen='').count()
    print(f"2. Páginas con imagen: {paginas_con_imagen}")
    
    # 3. Verificar obras asociadas
    obras_con_pagina = Obra.objects.filter(pagina_pdf__isnull=False).count()
    print(f"3. Obras con página asociada: {obras_con_pagina}")
    
    # 4. Mostrar algunos ejemplos
    print("\n=== EJEMPLOS DE OBRAS CON PÁGINAS ===")
    obras_ejemplo = Obra.objects.filter(pagina_pdf__isnull=False)[:5]
    
    for obra in obras_ejemplo:
        pagina = PaginaPDF.objects.get(numero_pagina=obra.pagina_pdf)
        print(f"\n📖 {obra.titulo_limpio}")
        print(f"   📄 Página: {obra.pagina_pdf}")
        print(f"   🖼️  Imagen: {pagina.archivo_imagen}")
        print(f"   📝 Texto: {len(pagina.texto_extraido)} caracteres")
        print(f"   🔗 URL: /obras/pagina-pdf/{obra.pagina_pdf}/")
    
    # 5. Verificar archivos de imagen
    print("\n=== VERIFICACIÓN DE ARCHIVOS DE IMAGEN ===")
    media_dir = Path('/Users/ivansimo/Documents/2025/ITEM/DELIA_DJANGO/media/pdf_pages')
    
    if media_dir.exists():
        archivos_imagen = list(media_dir.glob('*.png'))
        print(f"Archivos de imagen en media: {len(archivos_imagen)}")
        
        # Verificar algunas imágenes específicas
        paginas_ejemplo = PaginaPDF.objects.exclude(archivo_imagen='')[:3]
        for pagina in paginas_ejemplo:
            ruta_imagen = media_dir / pagina.archivo_imagen
            existe = ruta_imagen.exists()
            print(f"   Página {pagina.numero_pagina}: {pagina.archivo_imagen} - {'✅' if existe else '❌'}")
    else:
        print("❌ Directorio media/pdf_pages no existe")
    
    # 6. Estadísticas por origen de datos
    print("\n=== ESTADÍSTICAS POR ORIGEN DE DATOS ===")
    from django.db.models import Count
    
    origen_stats = Obra.objects.values('origen_datos').annotate(
        count=Count('id')
    ).order_by('origen_datos')
    
    for stat in origen_stats:
        print(f"   {stat['origen_datos']}: {stat['count']} obras")
    
    # 7. Páginas más populares (con más obras)
    print("\n=== PÁGINAS MÁS POPULARES ===")
    paginas_populares = Obra.objects.filter(pagina_pdf__isnull=False).values('pagina_pdf').annotate(
        count=Count('id')
    ).order_by('-count')[:5]
    
    for pagina in paginas_populares:
        num_pagina = pagina['pagina_pdf']
        count = pagina['count']
        print(f"   Página {num_pagina}: {count} obras")
    
    print("\n=== PRUEBA COMPLETADA ===")

if __name__ == '__main__':
    test_pdf_pages()
