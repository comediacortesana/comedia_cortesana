#!/usr/bin/env python3
"""
Actualiza el sistema de análisis de IA para incluir referencias precisas a páginas PDF
"""

import json
import re
from sistema_analisis_ia import AnalisisIA

def actualizar_analisis_con_referencias_paginas(archivo_analisis: str, archivo_extraccion: str):
    """
    Actualiza análisis de IA añadiendo referencias precisas a páginas PDF
    """
    # Cargar análisis existente
    with open(archivo_analisis, 'r', encoding='utf-8') as f:
        datos_analisis = json.load(f)
    
    # Cargar extracción para obtener datos completos
    with open(archivo_extraccion, 'r', encoding='utf-8') as f:
        datos_extraccion = json.load(f)
    
    metadata = datos_extraccion.get('metadata', {})
    archivo_fuente = metadata.get('archivo_fuente', '')
    
    # Actualizar cada análisis
    for analisis in datos_analisis.get('analisis', []):
        tipo_registro = analisis.get('tipo_registro')
        registro_id = analisis.get('registro_id', '')
        
        # Buscar registro correspondiente en extracción
        if tipo_registro == 'representacion':
            # Extraer índice del registro_id
            match = re.search(r'representacion_(\d+)', registro_id)
            if match:
                idx = int(match.group(1)) - 1
                representaciones = datos_extraccion.get('representaciones', [])
                if idx < len(representaciones):
                    rep = representaciones[idx]
                    datos_rep = rep.get('datos', rep)
                    pagina_pdf = datos_rep.get('pagina_pdf')
                    
                    if pagina_pdf:
                        # Añadir referencia completa a página PDF
                        referencia_pagina = {
                            'pagina_pdf': pagina_pdf,
                            'archivo_fuente': archivo_fuente,
                            'url_pagina': f"/obras/pagina-pdf/{pagina_pdf}/",
                            'url_imagen': f"/media/pdf_pages/page_{pagina_pdf:03d}.png",
                            'ruta_imagen_local': f"data/raw/images/FUENTES IX 1_part_001_ALL_PAGES/page_{pagina_pdf:03d}.png",
                            'texto_referencia': f"📄 Ver página {pagina_pdf} del PDF original",
                            'instrucciones': f"Abre el PDF original en la página {pagina_pdf} para verificar esta información"
                        }
                        
                        # Añadir a contexto_adicional
                        if 'contexto_adicional' not in analisis:
                            analisis['contexto_adicional'] = {}
                        analisis['contexto_adicional']['referencia_pagina_pdf'] = referencia_pagina
                        
                        # Actualizar archivo_fuente y pagina_pdf en metadata
                        analisis['archivo_fuente'] = archivo_fuente
                        analisis['pagina_pdf'] = pagina_pdf
        
        # Buscar referencias a páginas en frases originales
        frases_originales = analisis.get('frases_originales', [])
        referencias_paginas_encontradas = []
        
        for frase in frases_originales:
            # Buscar referencias como "(Fuentes V, pág. 187)"
            patron = r'\(Fuentes\s+[IVX]+,?\s+pág\.?\s+(\d+)\)'
            matches = re.finditer(patron, frase, re.IGNORECASE)
            
            for match in matches:
                pagina_fuente = int(match.group(1))
                referencias_paginas_encontradas.append({
                    'tipo': 'referencia_en_fuente',
                    'pagina': pagina_fuente,
                    'texto_completo': match.group(0),
                    'contexto': frase[max(0, match.start()-30):match.end()+30],
                    'url_pagina': f"/obras/pagina-pdf/{pagina_fuente}/"
                })
        
        if referencias_paginas_encontradas:
            if 'contexto_adicional' not in analisis:
                analisis['contexto_adicional'] = {}
            analisis['contexto_adicional']['referencias_paginas_adicionales'] = referencias_paginas_encontradas
    
    # Guardar análisis actualizado
    archivo_salida = archivo_analisis.replace('.json', '_con_referencias_paginas.json')
    with open(archivo_salida, 'w', encoding='utf-8') as f:
        json.dump(datos_analisis, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Análisis actualizado guardado en: {archivo_salida}")
    print(f"   - Total análisis: {len(datos_analisis.get('analisis', []))}")
    print(f"   - Análisis con referencias a páginas: {sum(1 for a in datos_analisis.get('analisis', []) if a.get('contexto_adicional', {}).get('referencia_pagina_pdf'))}")
    
    return archivo_salida


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 3:
        print("Uso: python actualizar_sistema_analisis_con_paginas.py <archivo_analisis.json> <archivo_extraccion.json>")
        sys.exit(1)
    
    archivo_analisis = sys.argv[1]
    archivo_extraccion = sys.argv[2]
    
    actualizar_analisis_con_referencias_paginas(archivo_analisis, archivo_extraccion)






