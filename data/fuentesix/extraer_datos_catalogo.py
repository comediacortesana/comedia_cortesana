#!/usr/bin/env python3
"""
Script para extraer datos de representaciones de archivos de catálogo alfabético

Procesa archivos como part_003, part_004 que contienen catálogos alfabéticos
de obras con múltiples representaciones documentadas.
"""

import re
import json
from datetime import datetime
from typing import List, Dict, Optional, Tuple

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
    
    # Patrón para rangos como "10-13 de mayo de 1696"
    patron_rango = r'(\d{1,2})\s*-\s*(\d{1,2})\s+de\s+(\w+)\s+de\s+(\d{4})'
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
    
    # Si solo hay año
    patron_año = r'(\d{4})'
    match_año = re.search(patron_año, texto_fecha)
    if match_año:
        año = int(match_año.group(1))
        return {
            'fecha_formateada': f"{año}-01-01",
            'fecha_original': texto_fecha,
            'año': año,
            'nota': 'solo_año'
        }
    
    return None

def extraer_compania(texto: str) -> Optional[str]:
    """Extrae nombre de compañía del texto"""
    # Patrones comunes
    patrones = [
        r'compañía\s+de\s+([^\.]+?)(?:\.|,|$)',
        r'([A-Z][a-z]+(?:\s+de\s+[A-Z][a-z]+)*)\s*\.\s*(?:Palacio|Buen Retiro|Corral)',
        r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s*\.\s*(?:Representación|Palacio)',
    ]
    
    for patron in patrones:
        match = re.search(patron, texto, re.IGNORECASE)
        if match:
            compania = match.group(1).strip()
            # Limpiar
            compania = re.sub(r'\s+', ' ', compania)
            if len(compania) > 2 and len(compania) < 100:
                return compania
    
    return None

def extraer_lugar(texto: str) -> Dict:
    """Extrae información de lugar del texto"""
    lugares_comunes = {
        'Palacio': {'nombre': 'Palacio', 'tipo': 'palacio', 'region': 'Comunidad de Madrid', 'ciudad': 'Madrid'},
        'Buen Retiro': {'nombre': 'Buen Retiro', 'tipo': 'palacio', 'region': 'Comunidad de Madrid', 'ciudad': 'Madrid'},
        'Coliseo del Buen Retiro': {'nombre': 'Coliseo del Buen Retiro', 'tipo': 'palacio', 'region': 'Comunidad de Madrid', 'ciudad': 'Madrid'},
        'Cuarto de la Reina': {'nombre': 'Cuarto de la Reina', 'tipo': 'palacio', 'region': 'Comunidad de Madrid', 'ciudad': 'Madrid'},
        'Cuarto del Rey': {'nombre': 'Cuarto del Rey', 'tipo': 'palacio', 'region': 'Comunidad de Madrid', 'ciudad': 'Madrid'},
        'Salón': {'nombre': 'Salón', 'tipo': 'palacio', 'region': 'Comunidad de Madrid', 'ciudad': 'Madrid'},
        'Salón dorado': {'nombre': 'Salón dorado', 'tipo': 'palacio', 'region': 'Comunidad de Madrid', 'ciudad': 'Madrid'},
        'Corral del Príncipe': {'nombre': 'Corral del Príncipe', 'tipo': 'corral', 'region': 'Comunidad de Madrid', 'ciudad': 'Madrid'},
        'Corral de la Cruz': {'nombre': 'Corral de la Cruz', 'tipo': 'corral', 'region': 'Comunidad de Madrid', 'ciudad': 'Madrid'},
        'Saloncete': {'nombre': 'Saloncete del Buen Retiro', 'tipo': 'palacio', 'region': 'Comunidad de Madrid', 'ciudad': 'Madrid'},
        'Pardo': {'nombre': 'Pardo', 'tipo': 'palacio', 'region': 'Comunidad de Madrid', 'ciudad': 'Madrid'},
    }
    
    lugar_info = {'nombre': '', 'tipo': '', 'region': '', 'ciudad': ''}
    
    for lugar_key, lugar_data in lugares_comunes.items():
        if lugar_key.lower() in texto.lower():
            lugar_info.update(lugar_data)
            break
    
    # Si no se encontró lugar específico pero dice "Representación palaciega"
    if not lugar_info['nombre'] and 'palaciega' in texto.lower():
        lugar_info = {'nombre': 'Palacio', 'tipo': 'palacio', 'region': 'Comunidad de Madrid', 'ciudad': 'Madrid'}
    
    return lugar_info

def procesar_entrada_obra(texto_completo: str, titulo_obra: str, numero_linea: int) -> List[Dict]:
    """
    Procesa una entrada de obra del catálogo y extrae todas las representaciones
    
    Returns:
        Lista de representaciones extraídas
    """
    representaciones = []
    
    # Dividir por representaciones numeradas (1), (2), etc.
    patron_representacion = r'\((\d+)\)\s+([^\(]+?)(?=\((?:\d+)\)|$)'
    matches = re.finditer(patron_representacion, texto_completo)
    
    for match in matches:
        num_rep = match.group(1)
        texto_rep = match.group(2).strip()
        
        # Extraer fecha
        fecha_info = None
        patron_fecha = r'(\d{1,2}\s+de\s+\w+\s+de\s+\d{4}|Entre[^\.]+|antes\s+del[^\.]+|\d{4})'
        match_fecha = re.search(patron_fecha, texto_rep)
        if match_fecha:
            fecha_info = parsear_fecha_espanola(match_fecha.group(1))
        
        # Extraer compañía
        compania = extraer_compania(texto_rep)
        
        # Extraer lugar
        lugar_info = extraer_lugar(texto_rep)
        
        # Extraer fuente
        fuente_match = re.search(r'\(Fuentes\s+([IVX]+)\)', texto_rep)
        fuente = fuente_match.group(1) if fuente_match else ''
        
        # Crear representación
        representacion = {
            'obra_titulo': titulo_obra,
            'fecha': fecha_info['fecha_original'] if fecha_info else '',
            'fecha_formateada': fecha_info['fecha_formateada'] if fecha_info else '',
            'compañia': compania or '',
            'director_compañia': compania or '',
            'lugar_nombre': lugar_info['nombre'],
            'lugar_tipo': lugar_info['tipo'],
            'lugar_region': lugar_info['region'],
            'lugar_ciudad': lugar_info['ciudad'],
            'mecenas': '',
            'organizadores_fiesta': [],
            'personajes_historicos': [],
            'tipo_funcion': 'representación_normal',
            'publico': 'corte' if 'palacio' in lugar_info['tipo'].lower() or 'palaciega' in texto_rep.lower() else '',
            'observaciones': f"Fuente: Fuentes {fuente}. Representación #{num_rep}",
            'texto_original': texto_rep[:500],
            'confianza': 'medio',
            'numero_representacion': num_rep
        }
        
        representaciones.append(representacion)
    
    return representaciones

def procesar_archivo_catalogo(ruta_archivo: str) -> Dict:
    """
    Procesa un archivo de catálogo completo
    
    Returns:
        Dict con representaciones, obras, lugares, etc.
    """
    with open(ruta_archivo, 'r', encoding='utf-8') as f:
        contenido = f.read()
    
    # Dividir por páginas
    paginas = re.split(r'---\s*PÁGINA\s+\d+\s*---', contenido)
    
    todas_representaciones = []
    todas_obras = []
    lugares_unicos = {}
    companias_unicas = {}
    
    numero_linea = 0
    
    for pagina_num, pagina in enumerate(paginas[1:], 1):  # Saltar primera (vacía)
        # Buscar entradas de obras (títulos en mayúsculas al inicio de línea)
        lineas = pagina.split('\n')
        
        titulo_actual = None
        texto_obra_actual = []
        
        for linea in lineas:
            numero_linea += 1
            linea = linea.strip()
            
            if not linea:
                continue
            
            # Detectar título de obra (línea que empieza con mayúscula y no tiene fecha)
            if re.match(r'^[A-ZÁÉÍÓÚÑ][^\(]*$', linea) and not re.search(r'\d{4}', linea):
                # Guardar obra anterior si existe
                if titulo_actual and texto_obra_actual:
                    texto_completo = ' '.join(texto_obra_actual)
                    representaciones = procesar_entrada_obra(texto_completo, titulo_actual, numero_linea)
                    todas_representaciones.extend(representaciones)
                    
                    if representaciones:
                        todas_obras.append({
                            'titulo': titulo_actual,
                            'total_representaciones': len(representaciones)
                        })
                
                # Nueva obra
                titulo_actual = linea
                texto_obra_actual = []
            elif titulo_actual:
                # Continuar acumulando texto de la obra
                texto_obra_actual.append(linea)
        
        # Procesar última obra
        if titulo_actual and texto_obra_actual:
            texto_completo = ' '.join(texto_obra_actual)
            representaciones = procesar_entrada_obra(texto_completo, titulo_actual, numero_linea)
            todas_representaciones.extend(representaciones)
            
            if representaciones:
                todas_obras.append({
                    'titulo': titulo_actual,
                    'total_representaciones': len(representaciones)
                })
    
    # Recopilar lugares únicos
    for rep in todas_representaciones:
        if rep['lugar_nombre']:
            lugar_key = rep['lugar_nombre']
            if lugar_key not in lugares_unicos:
                lugares_unicos[lugar_key] = {
                    'nombre': rep['lugar_nombre'],
                    'tipo': rep['lugar_tipo'],
                    'region': rep['lugar_region'],
                    'ciudad': rep['lugar_ciudad']
                }
    
    # Recopilar compañías únicas
    for rep in todas_representaciones:
        if rep['compañia']:
            if rep['compañia'] not in companias_unicas:
                companias_unicas[rep['compañia']] = {
                    'nombre_completo': rep['compañia'],
                    'director': rep['director_compañia']
                }
    
    return {
        'representaciones': todas_representaciones,
        'obras': todas_obras,
        'lugares_nuevos': list(lugares_unicos.values()),
        'compañias_identificadas': list(companias_unicas.values()),
        'total_representaciones': len(todas_representaciones),
        'total_obras': len(todas_obras)
    }

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("Uso: python extraer_datos_catalogo.py <archivo_txt>")
        sys.exit(1)
    
    archivo = sys.argv[1]
    resultado = procesar_archivo_catalogo(archivo)
    
    print(f"✅ Procesado: {archivo}")
    print(f"   - Representaciones: {resultado['total_representaciones']}")
    print(f"   - Obras: {resultado['total_obras']}")
    print(f"   - Lugares: {len(resultado['lugares_nuevos'])}")
    print(f"   - Compañías: {len(resultado['compañias_identificadas'])}")
    
    # Guardar resultado
    archivo_salida = archivo.replace('.txt', '_extraccion.json')
    with open(archivo_salida, 'w', encoding='utf-8') as f:
        json.dump(resultado, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Resultado guardado en: {archivo_salida}")






