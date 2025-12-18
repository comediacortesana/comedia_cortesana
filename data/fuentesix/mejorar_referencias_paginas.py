#!/usr/bin/env python3
"""
Script para mejorar referencias a páginas PDF en datos extraídos

Añade referencias precisas a páginas del PDF original para que los usuarios
puedan abrir el documento y verificar la información.
"""

import json
import re
import os
from typing import Dict, List, Optional

class MapeadorPaginasPDF:
    """Mapea páginas del texto extraído a páginas del PDF original"""
    
    def __init__(self):
        # Mapeo de archivos part_XXX a rangos de páginas del PDF
        # Basado en pdf_page_mapping.json: part_001 tiene páginas 1-25, part_002 tiene 26-50, etc.
        self.mapeo_part_a_paginas = {
            'part_001': {'inicio': 1, 'fin': 25, 'offset': 0},  # Páginas 1-25 del PDF
            'part_002': {'inicio': 26, 'fin': 50, 'offset': 25},  # Páginas 26-50
            'part_003': {'inicio': 51, 'fin': 75, 'offset': 50},  # Páginas 51-75
            'part_004': {'inicio': 76, 'fin': 100, 'offset': 75},  # Páginas 76-100
            'part_005': {'inicio': 101, 'fin': 125, 'offset': 100},  # Páginas 101-125
            'part_006': {'inicio': 126, 'fin': 150, 'offset': 125},  # Páginas 126-150
            'part_007': {'inicio': 151, 'fin': 175, 'offset': 150},  # Páginas 151-175
            'part_008': {'inicio': 176, 'fin': 200, 'offset': 175},  # Páginas 176-200
            'part_009': {'inicio': 201, 'fin': 225, 'offset': 200},  # Páginas 201-225
            'part_010': {'inicio': 226, 'fin': 250, 'offset': 225},  # Páginas 226-250
            'part_011': {'inicio': 251, 'fin': 252, 'offset': 250},  # Páginas 251-252
        }
        
        # Mapeo de "PÁGINA X" en texto a página real del PDF
        self.mapeo_paginas_texto = {}
    
    def extraer_numero_pagina_del_texto(self, texto: str, archivo_fuente: str) -> Optional[int]:
        """
        Extrae el número de página del PDF basándose en el texto y archivo fuente
        
        Args:
            texto: Texto donde buscar referencia a página
            archivo_fuente: Nombre del archivo fuente (ej: "part_001")
        
        Returns:
            Número de página del PDF o None
        """
        # Buscar patrón "--- PÁGINA X ---"
        patron_pagina = r'---\s*PÁGINA\s+(\d+)\s*---'
        match = re.search(patron_pagina, texto)
        
        if match:
            pagina_texto = int(match.group(1))
            
            # Determinar archivo part
            part_match = re.search(r'part_(\d+)', archivo_fuente, re.IGNORECASE)
            if part_match:
                part_num = int(part_match.group(1))
                part_key = f'part_{part_num:03d}'
                
                # Calcular página real del PDF
                if part_key in self.mapeo_part_a_paginas:
                    offset = self.mapeo_part_a_paginas[part_key]['offset']
                    pagina_pdf = offset + pagina_texto
                    return pagina_pdf
        
        return None
    
    def encontrar_paginas_en_frase(self, frase: str, archivo_fuente: str, numero_linea: int) -> List[Dict]:
        """
        Encuentra todas las referencias a páginas en una frase
        
        Returns:
            Lista de dicts con información de páginas
        """
        paginas = []
        
        # Buscar referencias explícitas como "(Fuentes V, pág. 187)"
        patron_pagina_fuente = r'\(Fuentes\s+[IVX]+,?\s+pág\.?\s+(\d+)\)'
        matches = re.finditer(patron_pagina_fuente, frase, re.IGNORECASE)
        
        for match in matches:
            pagina_fuente = int(match.group(1))
            paginas.append({
                'tipo': 'referencia_fuente',
                'pagina': pagina_fuente,
                'fuente': match.group(0),
                'contexto': frase[match.start()-50:match.end()+50] if len(frase) > match.end()+50 else frase
            })
        
        # Buscar patrón "--- PÁGINA X ---" cerca de la línea
        # Esto requiere contexto del archivo completo
        patron_pagina_marcador = r'---\s*PÁGINA\s+(\d+)\s*---'
        match = re.search(patron_pagina_marcador, frase)
        if match:
            pagina_texto = int(match.group(1))
            pagina_pdf = self.extraer_numero_pagina_del_texto(frase, archivo_fuente)
            if pagina_pdf:
                paginas.append({
                    'tipo': 'marcador_pagina',
                    'pagina': pagina_pdf,
                    'pagina_texto': pagina_texto,
                    'contexto': 'Marcador de página en texto extraído'
                })
        
        return paginas
    
    def crear_referencia_pagina_completa(
        self,
        pagina_pdf: int,
        archivo_fuente: str,
        tipo_referencia: str = 'directa',
        contexto: str = None
    ) -> Dict:
        """
        Crea una referencia completa a una página del PDF
        
        Returns:
            Dict con toda la información de referencia
        """
        # Determinar ruta de imagen
        ruta_imagen = f"data/raw/images/FUENTES IX 1_part_{archivo_fuente.split('part_')[1].split('_')[0]}_ALL_PAGES/page_{pagina_pdf:03d}.png"
        
        # URL para abrir en el sistema (ajustar según estructura)
        url_pagina = f"/obras/pagina-pdf/{pagina_pdf}/"
        url_imagen = f"/media/pdf_pages/page_{pagina_pdf:03d}.png"
        
        return {
            'pagina_pdf': pagina_pdf,
            'archivo_fuente': archivo_fuente,
            'tipo_referencia': tipo_referencia,  # 'directa', 'inferida', 'referencia_fuente'
            'ruta_imagen': ruta_imagen,
            'url_pagina': url_pagina,
            'url_imagen': url_imagen,
            'contexto': contexto,
            'texto_referencia': f"Página {pagina_pdf} del PDF original",
            'enlace_verificacion': f"Ver página {pagina_pdf} en PDF original"
        }


def mejorar_referencias_paginas(archivo_extraccion: str, archivo_texto_original: str = None):
    """
    Mejora un archivo de extracción añadiendo referencias precisas a páginas PDF
    
    Args:
        archivo_extraccion: Archivo JSON de extracción a mejorar
        archivo_texto_original: Archivo de texto original (opcional, para contexto)
    """
    mapeador = MapeadorPaginasPDF()
    
    # Cargar datos extraídos
    with open(archivo_extraccion, 'r', encoding='utf-8') as f:
        datos = json.load(f)
    
    metadata = datos.get('metadata', {})
    archivo_fuente = metadata.get('archivo_fuente', '')
    
    # Cargar texto original si está disponible
    texto_completo = None
    if archivo_texto_original and os.path.exists(archivo_texto_original):
        with open(archivo_texto_original, 'r', encoding='utf-8') as f:
            texto_completo = f.read()
    
    # Mejorar representaciones
    representaciones = datos.get('representaciones', [])
    for rep in representaciones:
        datos_rep = rep.get('datos', rep)
        metadata_rep = rep.get('metadata_registro', {})
        
        # Extraer página PDF si existe
        pagina_pdf = datos_rep.get('pagina_pdf') or metadata_rep.get('pagina_pdf')
        
        # Buscar referencias adicionales en texto original
        referencias_paginas = []
        
        if datos_rep.get('texto_original'):
            frase = datos_rep['texto_original']
            paginas_encontradas = mapeador.encontrar_paginas_en_frase(frase, archivo_fuente, metadata_rep.get('linea_texto', 0))
            referencias_paginas.extend(paginas_encontradas)
        
        # Crear referencia completa
        if pagina_pdf:
            referencia = mapeador.crear_referencia_pagina_completa(
                pagina_pdf=pagina_pdf,
                archivo_fuente=archivo_fuente,
                tipo_referencia='directa',
                contexto=datos_rep.get('texto_original', '')
            )
            
            # Añadir a metadata_registro
            if 'metadata_registro' not in rep:
                rep['metadata_registro'] = {}
            
            rep['metadata_registro']['referencia_pagina_pdf'] = referencia
            rep['metadata_registro']['referencias_paginas_adicionales'] = referencias_paginas
        
        # Añadir también a datos_rep para acceso directo
        if pagina_pdf:
            datos_rep['referencia_pagina_pdf'] = {
                'pagina': pagina_pdf,
                'url': f"/obras/pagina-pdf/{pagina_pdf}/",
                'texto': f"Ver página {pagina_pdf} en PDF original"
            }
    
    # Mejorar lugares
    lugares = datos.get('lugares_nuevos', [])
    for lugar in lugares:
        datos_lugar = lugar.get('datos', lugar)
        metadata_lugar = lugar.get('metadata_registro', {})
        
        # Buscar página donde se mencionó el lugar
        if texto_completo and datos_lugar.get('nombre'):
            # Buscar primera mención del lugar en el texto
            nombre_lugar = datos_lugar['nombre']
            indice = texto_completo.find(nombre_lugar)
            if indice != -1:
                # Buscar marcador de página más cercano antes de esta mención
                texto_antes = texto_completo[:indice]
                paginas_antes = re.findall(r'---\s*PÁGINA\s+(\d+)\s*---', texto_antes)
                if paginas_antes:
                    pagina_texto = int(paginas_antes[-1])
                    pagina_pdf = mapeador.extraer_numero_pagina_del_texto(
                        f"--- PÁGINA {pagina_texto} ---",
                        archivo_fuente
                    )
                    if pagina_pdf:
                        referencia = mapeador.crear_referencia_pagina_completa(
                            pagina_pdf=pagina_pdf,
                            archivo_fuente=archivo_fuente,
                            tipo_referencia='inferida',
                            contexto=f"Primera mención de '{nombre_lugar}'"
                        )
                        if 'metadata_registro' not in lugar:
                            lugar['metadata_registro'] = {}
                        lugar['metadata_registro']['referencia_pagina_pdf'] = referencia
    
    # Guardar archivo mejorado
    archivo_salida = archivo_extraccion.replace('.json', '_con_referencias_paginas.json')
    with open(archivo_salida, 'w', encoding='utf-8') as f:
        json.dump(datos, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Referencias mejoradas guardadas en: {archivo_salida}")
    print(f"   - Representaciones con referencias: {sum(1 for r in representaciones if r.get('datos', {}).get('referencia_pagina_pdf'))}")
    
    return archivo_salida


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("Uso: python mejorar_referencias_paginas.py <archivo_extraccion.json> [archivo_texto_original.txt]")
        sys.exit(1)
    
    archivo_extraccion = sys.argv[1]
    archivo_texto = sys.argv[2] if len(sys.argv) > 2 else None
    
    mejorar_referencias_paginas(archivo_extraccion, archivo_texto)






