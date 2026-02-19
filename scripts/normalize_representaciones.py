#!/usr/bin/env python3
"""
Script para normalizar y unificar representaciones de FUENTESIX y CATCOM

- Normaliza formatos de fecha
- Unifica nombres de lugares usando catálogo de FUENTESIX
- Crea estructura unificada para exportación
"""

import json
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime


def cargar_catalogo_lugares(catalogo_path: Path) -> Dict:
    """Carga el catálogo de lugares de FUENTESIX"""
    try:
        with open(catalogo_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error cargando catálogo de lugares: {e}")
        return {}


def normalizar_nombre_lugar(nombre: str, catalogo: Dict) -> Dict[str, str]:
    """
    Normaliza el nombre de un lugar usando el catálogo de FUENTESIX
    
    Returns:
        Dict con 'nombre', 'tipo', 'region', 'ciudad' normalizados
    """
    if not nombre:
        return {'nombre': '', 'tipo': '', 'region': '', 'ciudad': ''}
    
    nombre_limpio = nombre.strip()
    
    # Buscar en el catálogo de lugares
    if catalogo and 'categorias' in catalogo:
        for categoria_key, categoria_data in catalogo['categorias'].items():
            lugares = categoria_data.get('lugares', [])
            for lugar in lugares:
                lugar_nombre = lugar.get('nombre', '').lower()
                lugar_id = lugar.get('id', '')
                
                # Buscar coincidencias
                if nombre_limpio.lower() == lugar_nombre or nombre_limpio.lower() in lugar_nombre or lugar_nombre in nombre_limpio.lower():
                    return {
                        'nombre': lugar.get('nombre', nombre_limpio),
                        'tipo': categoria_data.get('tipo', ''),
                        'region': '',  # Se puede inferir después
                        'ciudad': lugar.get('ciudad', '')
                    }
    
    # Mapeo manual para lugares comunes de CATCOM
    mapeo_lugares = {
        'madrid': {'nombre': 'Madrid', 'tipo': '', 'region': 'Comunidad de Madrid', 'ciudad': 'Madrid'},
        'madrid (?)': {'nombre': 'Madrid', 'tipo': '', 'region': 'Comunidad de Madrid', 'ciudad': 'Madrid'},
        'alcázar': {'nombre': 'Alcázar de Madrid', 'tipo': 'palacio', 'region': 'Comunidad de Madrid', 'ciudad': 'Madrid'},
        'alcázar de madrid': {'nombre': 'Alcázar de Madrid', 'tipo': 'palacio', 'region': 'Comunidad de Madrid', 'ciudad': 'Madrid'},
        'buen retiro': {'nombre': 'Buen Retiro', 'tipo': 'palacio', 'region': 'Comunidad de Madrid', 'ciudad': 'Madrid'},
        'coliseo del buen retiro': {'nombre': 'Coliseo del Buen Retiro', 'tipo': 'palacio', 'region': 'Comunidad de Madrid', 'ciudad': 'Madrid'},
        'salón dorado': {'nombre': 'Salón Dorado del Alcázar', 'tipo': 'palacio', 'region': 'Comunidad de Madrid', 'ciudad': 'Madrid'},
        'salón dorado del alcázar': {'nombre': 'Salón Dorado del Alcázar', 'tipo': 'palacio', 'region': 'Comunidad de Madrid', 'ciudad': 'Madrid'},
        'cuarto de la reina': {'nombre': 'Cuarto de la Reina', 'tipo': 'palacio', 'region': 'Comunidad de Madrid', 'ciudad': 'Madrid'},
        'corral del príncipe': {'nombre': 'Corral del Príncipe', 'tipo': 'corral', 'region': 'Comunidad de Madrid', 'ciudad': 'Madrid'},
        'corral de la cruz': {'nombre': 'Corral de la Cruz', 'tipo': 'corral', 'region': 'Comunidad de Madrid', 'ciudad': 'Madrid'},
        'valladolid': {'nombre': 'Valladolid', 'tipo': 'corral', 'region': 'Castilla y León', 'ciudad': 'Valladolid'},
        'viena': {'nombre': 'Viena', 'tipo': 'palacio', 'region': '', 'ciudad': 'Viena'},
    }
    
    nombre_lower = nombre_limpio.lower()
    if nombre_lower in mapeo_lugares:
        return mapeo_lugares[nombre_lower]
    
    # Si no encontramos nada, devolver el nombre original
    return {
        'nombre': nombre_limpio,
        'tipo': '',
        'region': '',
        'ciudad': nombre_limpio.split('(')[0].strip()
    }


def normalizar_fecha(fecha_str: str, fecha_formateada: str = '') -> Dict[str, str]:
    """
    Normaliza formato de fecha, asegurando que fecha_formateada esté en formato ISO
    """
    if fecha_formateada and len(fecha_formateada) == 10 and fecha_formateada.count('-') == 2:
        # Ya está en formato ISO
        return {
            'fecha': fecha_str,
            'fecha_formateada': fecha_formateada
        }
    
    # Intentar parsear fecha_str si no tenemos fecha_formateada
    if not fecha_formateada and fecha_str:
        # Ya debería estar parseada por el script de extracción
        return {
            'fecha': fecha_str,
            'fecha_formateada': ''
        }
    
    return {
        'fecha': fecha_str or '',
        'fecha_formateada': fecha_formateada or ''
    }


def normalizar_representacion_fuentesix(rep: Dict, catalogo: Dict) -> Dict:
    """Normaliza una representación de FUENTESIX"""
    datos = rep.get('datos', {})
    
    lugar_nombre = datos.get('lugar_nombre', '')
    lugar_normalizado = normalizar_nombre_lugar(lugar_nombre, catalogo)
    
    fecha_info = normalizar_fecha(
        datos.get('fecha', ''),
        datos.get('fecha_formateada', '')
    )
    
    return {
        'obra_titulo': datos.get('obra_titulo', ''),
        'fecha': fecha_info['fecha'],
        'fecha_formateada': fecha_info['fecha_formateada'],
        'compañia': datos.get('compañia', '') or datos.get('compania', ''),
        'director_compañia': datos.get('director_compañia', '') or datos.get('director_compania', ''),
        'lugar_nombre': lugar_normalizado['nombre'] or lugar_nombre,
        'lugar_tipo': lugar_normalizado['tipo'] or datos.get('lugar_tipo', ''),
        'lugar_region': lugar_normalizado['region'] or datos.get('lugar_region', ''),
        'lugar_ciudad': lugar_normalizado['ciudad'] or datos.get('lugar_ciudad', ''),
        'tipo_funcion': datos.get('tipo_funcion', 'representación_normal'),
        'publico': datos.get('publico', ''),
        'observaciones': datos.get('observaciones', ''),
        'texto_original': datos.get('texto_original', ''),
        'fuente': 'FUENTESIX',
        'pagina_pdf': datos.get('pagina_pdf'),
        'confianza': datos.get('confianza', 'medio')
    }


def normalizar_representacion_catcom(rep: Dict, catalogo: Dict) -> Dict:
    """Normaliza una representación de CATCOM"""
    lugar_nombre = rep.get('lugar_nombre', '')
    lugar_normalizado = normalizar_nombre_lugar(lugar_nombre, catalogo)
    
    fecha_info = normalizar_fecha(
        rep.get('fecha', ''),
        rep.get('fecha_formateada', '')
    )
    
    return {
        'obra_titulo': rep.get('obra_titulo', ''),
        'fecha': fecha_info['fecha'],
        'fecha_formateada': fecha_info['fecha_formateada'],
        'compañia': rep.get('compañia', ''),
        'director_compañia': rep.get('director_compañia', ''),
        'lugar_nombre': lugar_normalizado['nombre'] or lugar_nombre,
        'lugar_tipo': lugar_normalizado['tipo'] or rep.get('lugar_tipo', ''),
        'lugar_region': lugar_normalizado['region'] or rep.get('lugar_region', ''),
        'lugar_ciudad': lugar_normalizado['ciudad'] or rep.get('lugar_ciudad', ''),
        'tipo_funcion': rep.get('tipo_funcion', 'representación_normal'),
        'publico': rep.get('publico', ''),
        'observaciones': rep.get('observaciones', ''),
        'texto_original': rep.get('texto_original', ''),
        'fuente': 'CATCOM',
        'confianza': rep.get('confianza', 'medio')
    }


def cargar_representaciones_fuentesix(base_dir: Path) -> List[Dict]:
    """Carga representaciones desde archivos FUENTESIX"""
    fuentesix_dir = base_dir / 'data' / 'fuentesix'
    representaciones = []
    
    # Buscar archivos de extracción
    archivos_extraccion = list(fuentesix_dir.glob('extraccion_*.json'))
    
    for archivo in archivos_extraccion:
        try:
            with open(archivo, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            reps = data.get('representaciones', [])
            representaciones.extend(reps)
        except Exception as e:
            print(f"Error procesando {archivo}: {e}")
    
    return representaciones


def cargar_representaciones_catcom(base_dir: Path) -> List[Dict]:
    """Carga representaciones desde archivo extraído de CATCOM"""
    catcom_file = base_dir / 'data' / 'CATCOM' / 'representaciones_extraidas.json'
    
    if not catcom_file.exists():
        print(f"⚠️ Archivo {catcom_file} no existe. Ejecuta primero extract_catcom_dates.py")
        return []
    
    try:
        with open(catcom_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return data.get('representaciones', [])
    except Exception as e:
        print(f"Error cargando representaciones CATCOM: {e}")
        return []


def main():
    """Normaliza y unifica representaciones de ambas fuentes"""
    base_dir = Path(__file__).parent.parent
    
    # Cargar catálogo de lugares
    catalogo_path = base_dir / 'data' / 'fuentesix' / 'analisis_lugares_mecenas.json'
    catalogo = cargar_catalogo_lugares(catalogo_path)
    
    print("Cargando representaciones de FUENTESIX...")
    reps_fuentesix = cargar_representaciones_fuentesix(base_dir)
    print(f"  - {len(reps_fuentesix)} representaciones encontradas")
    
    print("Cargando representaciones de CATCOM...")
    reps_catcom = cargar_representaciones_catcom(base_dir)
    print(f"  - {len(reps_catcom)} representaciones encontradas")
    
    # Normalizar representaciones
    print("\nNormalizando representaciones...")
    representaciones_normalizadas = []
    
    for rep in reps_fuentesix:
        rep_norm = normalizar_representacion_fuentesix(rep, catalogo)
        representaciones_normalizadas.append(rep_norm)
    
    for rep in reps_catcom:
        rep_norm = normalizar_representacion_catcom(rep, catalogo)
        representaciones_normalizadas.append(rep_norm)
    
    # Agrupar por obra
    obras_dict = {}
    for rep in representaciones_normalizadas:
        titulo = rep.get('obra_titulo', '')
        if titulo not in obras_dict:
            obras_dict[titulo] = []
        obras_dict[titulo].append(rep)
    
    # Guardar resultado
    output_file = base_dir / 'data' / 'representaciones_normalizadas.json'
    output_data = {
        'metadata': {
            'fecha_generacion': datetime.now().isoformat(),
            'total_representaciones': len(representaciones_normalizadas),
            'total_obras': len(obras_dict),
            'fuentes': ['FUENTESIX', 'CATCOM'],
            'representaciones_con_fecha': sum(1 for r in representaciones_normalizadas if r.get('fecha_formateada')),
            'representaciones_con_lugar': sum(1 for r in representaciones_normalizadas if r.get('lugar_nombre')),
        },
        'obras': obras_dict,
        'representaciones': representaciones_normalizadas
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Normalización completada:")
    print(f"   - Total representaciones: {len(representaciones_normalizadas)}")
    print(f"   - Total obras: {len(obras_dict)}")
    print(f"   - Con fecha: {output_data['metadata']['representaciones_con_fecha']}")
    print(f"   - Con lugar: {output_data['metadata']['representaciones_con_lugar']}")
    print(f"   - Archivo guardado en: {output_file}")


if __name__ == '__main__':
    main()
