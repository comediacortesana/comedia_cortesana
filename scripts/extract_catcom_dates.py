#!/usr/bin/env python3
"""
Script para extraer fechas y lugares de representaciones desde archivos CATCOM

Procesa archivos JSON de CATCOM y extrae información estructurada de fechas,
lugares y compañías desde el campo 'noticia' que contiene texto libre.
"""

import re
import json
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime

# Mapeo de meses en español
MESES_ES = {
    'enero': 1, 'febrero': 2, 'marzo': 3, 'abril': 4, 'mayo': 5, 'junio': 6,
    'julio': 7, 'agosto': 8, 'septiembre': 9, 'octubre': 10, 'noviembre': 11, 'diciembre': 12
}


def parsear_fecha_espanola(texto_fecha: str) -> Optional[Dict]:
    """
    Parsea fechas en formato español como "22 de enero de 1651"
    
    Returns:
        Dict con 'fecha_formateada' (YYYY-MM-DD) y 'fecha_original'
    """
    if not texto_fecha or not texto_fecha.strip():
        return None
    
    texto_fecha = texto_fecha.strip()
    
    # Patrón para "día de mes de año"
    patron_completo = r'(\d{1,2})\s+de\s+(\w+)\s+de\s+(\d{4})'
    match = re.search(patron_completo, texto_fecha, re.IGNORECASE)
    
    if match:
        dia = int(match.group(1))
        mes_nombre = match.group(2).lower()
        año = int(match.group(3))
        
        if mes_nombre in MESES_ES:
            mes = MESES_ES[mes_nombre]
            try:
                fecha_formateada = f"{año}-{mes:02d}-{dia:02d}"
                return {
                    'fecha_formateada': fecha_formateada,
                    'fecha_original': texto_fecha,
                    'año': año,
                    'mes': mes,
                    'dia': dia
                }
            except ValueError:
                return None
    
    # Patrón para rangos como "10-13 de mayo de 1696" o "27 y 28 de marzo de 1690"
    patron_rango = r'(\d{1,2})\s*(?:-|y)\s*(\d{1,2})\s+de\s+(\w+)\s+de\s+(\d{4})'
    match_rango = re.search(patron_rango, texto_fecha, re.IGNORECASE)
    
    if match_rango:
        dia_inicio = int(match_rango.group(1))
        dia_fin = int(match_rango.group(2))
        mes_nombre = match_rango.group(3).lower()
        año = int(match_rango.group(4))
        
        if mes_nombre in MESES_ES:
            mes = MESES_ES[mes_nombre]
            # Retornar fecha de inicio
            fecha_formateada = f"{año}-{mes:02d}-{dia_inicio:02d}"
            return {
                'fecha_formateada': fecha_formateada,
                'fecha_original': texto_fecha,
                'año': año,
                'mes': mes,
                'dia': dia_inicio,
                'es_rango': True,
                'dia_fin': dia_fin
            }
    
    # Patrón para "antes del X de Y de Z"
    patron_antes = r'antes\s+del\s+(\d{1,2})\s+de\s+(\w+)\s+de\s+(\d{4})'
    match_antes = re.search(patron_antes, texto_fecha, re.IGNORECASE)
    
    if match_antes:
        dia = int(match_antes.group(1))
        mes_nombre = match_antes.group(2).lower()
        año = int(match_antes.group(3))
        
        if mes_nombre in MESES_ES:
            mes = MESES_ES[mes_nombre]
            fecha_formateada = f"{año}-{mes:02d}-{dia:02d}"
            return {
                'fecha_formateada': fecha_formateada,
                'fecha_original': texto_fecha,
                'año': año,
                'mes': mes,
                'dia': dia,
                'nota': 'fecha_aproximada_antes_de'
            }
    
    # Patrón para "entre X y Y"
    patron_entre = r'Entre\s+(\d{1,2})\s+de\s+(\w+)\s+de\s+(\d{4})\s+y\s+(\d{1,2})\s+de\s+(\w+)\s+de\s+(\d{4})'
    match_entre = re.search(patron_entre, texto_fecha, re.IGNORECASE)
    
    if match_entre:
        dia_inicio = int(match_entre.group(1))
        mes_nombre_inicio = match_entre.group(2).lower()
        año_inicio = int(match_entre.group(3))
        
        if mes_nombre_inicio in MESES_ES:
            mes_inicio = MESES_ES[mes_nombre_inicio]
            fecha_formateada = f"{año_inicio}-{mes_inicio:02d}-{dia_inicio:02d}"
            return {
                'fecha_formateada': fecha_formateada,
                'fecha_original': texto_fecha,
                'año': año_inicio,
                'mes': mes_inicio,
                'dia': dia_inicio,
                'nota': 'fecha_aproximada_entre'
            }
    
    # Si solo hay año (buscar años del siglo XVII-XVIII)
    patron_año = r'\b(1[0-9]{3}|20[0-9]{2})\b'
    match_año = re.search(patron_año, texto_fecha)
    if match_año:
        año = int(match_año.group(1))
        # Solo considerar años razonables (1600-1800)
        if 1600 <= año <= 1800:
            return {
                'fecha_formateada': f"{año}-01-01",
                'fecha_original': str(año),
                'año': año,
                'nota': 'solo_año'
            }
    
    return None


def extraer_compania(texto: str) -> Optional[str]:
    """Extrae nombre de compañía del texto"""
    # Patrones comunes para compañías
    patrones = [
        r'compañía\s+de\s+([A-ZÁÉÍÓÚÑ][^\.]+?)(?:\.|,|$)',
        r'compañías\s+de\s+([A-ZÁÉÍÓÚÑ][^\.]+?)(?:\.|,|$)',
        r'([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+de\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)*)\s+(?:hizo|representó|hiz)',
        r'([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)*)\s+y\s+([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)*)\s+(?:hicieron|representaron)',
    ]
    
    for patron in patrones:
        match = re.search(patron, texto, re.IGNORECASE)
        if match:
            if len(match.groups()) == 2:
                # Dos compañías
                compania = f"{match.group(1).strip()} y {match.group(2).strip()}"
            else:
                compania = match.group(1).strip()
            
            # Limpiar
            compania = re.sub(r'\s+', ' ', compania)
            # Remover palabras comunes al final
            compania = re.sub(r'\s+(hizo|representó|hiz|hicieron|representaron)$', '', compania, flags=re.IGNORECASE)
            
            if len(compania) > 2 and len(compania) < 150:
                return compania
    
    return None


def extraer_lugar_detallado(texto: str, lugar_base: str) -> Dict[str, str]:
    """
    Extrae información detallada del lugar desde el texto
    """
    lugar_info = {
        'nombre': lugar_base,
        'tipo': '',
        'detalle': ''
    }
    
    # Buscar lugares específicos mencionados en el texto
    lugares_especificos = {
        'Alcázar': {'nombre': 'Alcázar de Madrid', 'tipo': 'palacio'},
        'Buen Retiro': {'nombre': 'Buen Retiro', 'tipo': 'palacio'},
        'Coliseo del Buen Retiro': {'nombre': 'Coliseo del Buen Retiro', 'tipo': 'palacio'},
        'Salón Dorado': {'nombre': 'Salón Dorado del Alcázar', 'tipo': 'palacio'},
        'Cuarto de la Reina': {'nombre': 'Cuarto de la Reina', 'tipo': 'palacio'},
        'Corral del Príncipe': {'nombre': 'Corral del Príncipe', 'tipo': 'corral'},
        'Corral de la Cruz': {'nombre': 'Corral de la Cruz', 'tipo': 'corral'},
    }
    
    for lugar_key, lugar_data in lugares_especificos.items():
        if lugar_key.lower() in texto.lower():
            lugar_info['nombre'] = lugar_data['nombre']
            lugar_info['tipo'] = lugar_data['tipo']
            lugar_info['detalle'] = lugar_key
            break
    
    return lugar_info


def procesar_performance(perf: Dict, obra_titulo: str) -> Optional[Dict]:
    """
    Procesa una performance de CATCOM y extrae información estructurada
    """
    noticia = perf.get('noticia', '')
    lugar_base = perf.get('lugar', '').strip()
    espacio = perf.get('espacio', '').strip()
    
    if not noticia:
        return None
    
    # Extraer fecha
    fecha_info = None
    patrones_fecha = [
        r'(\d{1,2}\s+de\s+\w+\s+de\s+\d{4})',  # "2 de diciembre de 1674"
        r'(\d{1,2}\s*(?:-|y)\s*\d{1,2}\s+de\s+\w+\s+de\s+\d{4})',  # "27 y 28 de marzo de 1690"
        r'(antes\s+del\s+\d{1,2}\s+de\s+\w+\s+de\s+\d{4})',  # "antes del X de Y de Z"
        r'(Entre\s+\d{1,2}\s+de\s+\w+\s+de\s+\d{4}\s+y\s+\d{1,2}\s+de\s+\w+\s+de\s+\d{4})',  # "Entre X y Y"
    ]
    
    for patron in patrones_fecha:
        match = re.search(patron, noticia, re.IGNORECASE)
        if match:
            fecha_info = parsear_fecha_espanola(match.group(1))
            if fecha_info:
                break
    
    # Si no encontramos fecha completa, buscar solo año
    if not fecha_info:
        fecha_info = parsear_fecha_espanola(noticia)
    
    # Extraer compañía
    compania = extraer_compania(noticia)
    
    # Extraer lugar detallado
    lugar_info = extraer_lugar_detallado(noticia, lugar_base)
    
    # Determinar tipo de lugar desde espacio
    tipo_lugar = ''
    if espacio:
        if 'palacio' in espacio.lower():
            tipo_lugar = 'palacio'
        elif 'corral' in espacio.lower():
            tipo_lugar = 'corral'
        elif espacio == 'Ø':
            tipo_lugar = lugar_info.get('tipo', '')
        else:
            tipo_lugar = espacio
    
    # Si no tenemos tipo de lugar, intentar inferirlo
    if not tipo_lugar:
        if lugar_info.get('tipo'):
            tipo_lugar = lugar_info['tipo']
        elif 'palacio' in noticia.lower() or 'alcázar' in noticia.lower():
            tipo_lugar = 'palacio'
        elif 'corral' in noticia.lower():
            tipo_lugar = 'corral'
    
    # Crear representación estructurada
    representacion = {
        'obra_titulo': obra_titulo,
        'fecha': fecha_info['fecha_original'] if fecha_info else '',
        'fecha_formateada': fecha_info['fecha_formateada'] if fecha_info else '',
        'año': fecha_info.get('año') if fecha_info else None,
        'compañia': compania or '',
        'director_compañia': compania or '',
        'lugar_nombre': lugar_info['nombre'],
        'lugar_tipo': tipo_lugar or lugar_info.get('tipo', ''),
        'lugar_region': '',  # Se normalizará después
        'lugar_ciudad': lugar_base.split('(')[0].strip() if lugar_base else '',
        'tipo_funcion': 'representación_normal',
        'publico': 'corte' if tipo_lugar == 'palacio' else 'pueblo',
        'observaciones': noticia[:500],  # Primeros 500 caracteres
        'texto_original': noticia,
        'fuente': 'CATCOM',
        'confianza': 'medio' if fecha_info else 'bajo',
        'nota_fecha': fecha_info.get('nota') if fecha_info else None,
    }
    
    return representacion


def procesar_archivo_catcom(archivo_path: Path) -> List[Dict]:
    """
    Procesa un archivo JSON de CATCOM y extrae representaciones
    """
    try:
        with open(archivo_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error leyendo {archivo_path}: {e}")
        return []
    
    obra_titulo = data.get('main_title') or data.get('title', '')
    performances = data.get('performances', [])
    
    representaciones = []
    for perf in performances:
        rep = procesar_performance(perf, obra_titulo)
        if rep:
            representaciones.append(rep)
    
    return representaciones


def main():
    """
    Procesa todos los archivos CATCOM y genera archivo JSON con representaciones estructuradas
    """
    base_dir = Path(__file__).parent.parent
    catcom_dir = base_dir / 'data' / 'CATCOM' / 'catcom'
    output_file = base_dir / 'data' / 'CATCOM' / 'representaciones_extraidas.json'
    
    if not catcom_dir.exists():
        print(f"Error: No se encontró el directorio {catcom_dir}")
        return
    
    print(f"Procesando archivos CATCOM en {catcom_dir}...")
    
    archivos_json = list(catcom_dir.glob('work_*.json'))
    print(f"Encontrados {len(archivos_json)} archivos")
    
    todas_representaciones = []
    obras_procesadas = 0
    representaciones_extraidas = 0
    
    for archivo in archivos_json:
        representaciones = procesar_archivo_catcom(archivo)
        if representaciones:
            todas_representaciones.extend(representaciones)
            obras_procesadas += 1
            representaciones_extraidas += len(representaciones)
        
        if obras_procesadas % 100 == 0:
            print(f"Procesadas {obras_procesadas} obras, {representaciones_extraidas} representaciones...")
    
    # Guardar resultados
    output_data = {
        'metadata': {
            'fecha_generacion': datetime.now().isoformat(),
            'fuente': 'CATCOM',
            'total_archivos_procesados': len(archivos_json),
            'total_obras_con_representaciones': obras_procesadas,
            'total_representaciones': len(todas_representaciones),
            'representaciones_con_fecha': sum(1 for r in todas_representaciones if r.get('fecha_formateada')),
            'representaciones_con_lugar': sum(1 for r in todas_representaciones if r.get('lugar_nombre')),
        },
        'representaciones': todas_representaciones
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Procesamiento completado:")
    print(f"   - Obras procesadas: {obras_procesadas}")
    print(f"   - Representaciones extraídas: {len(todas_representaciones)}")
    print(f"   - Con fecha: {output_data['metadata']['representaciones_con_fecha']}")
    print(f"   - Con lugar: {output_data['metadata']['representaciones_con_lugar']}")
    print(f"   - Archivo guardado en: {output_file}")


if __name__ == '__main__':
    main()
