#!/usr/bin/env python3
"""
Script para añadir metadata_registro a cada registro en archivos JSON de extracción

Este script transforma los archivos JSON de extracción añadiendo metadata_registro
a cada registro individual para trazabilidad completa.
"""

import json
import sys
from datetime import datetime

def añadir_metadata_registro(registro, metadata_global, tipo_registro, indice):
    """
    Añade metadata_registro a un registro individual
    
    Args:
        registro: Registro individual (dict)
        metadata_global: Metadata global del archivo
        tipo_registro: Tipo de registro ('obra', 'representacion', 'lugar', etc.)
        indice: Índice del registro en la lista
    """
    # Extraer información del registro
    pagina_pdf = registro.get('pagina_pdf', None)
    texto_original = registro.get('texto_original', '')
    confianza = registro.get('confianza', metadata_global.get('confianza_promedio', 'medio'))
    
    # Crear metadata_registro
    metadata_registro = {
        'fecha_extraccion': metadata_global.get('fecha_extraccion', datetime.now().isoformat() + 'Z'),
        'version_extraccion': metadata_global.get('version_extraccion', '1.0.0'),
        'archivo_fuente': metadata_global.get('archivo_fuente', ''),
        'pagina_pdf': pagina_pdf,
        'texto_original': texto_original[:500] if texto_original else '',  # Limitar a 500 caracteres
        'confianza': confianza,
        'extractor': metadata_global.get('metodo_extraccion', 'IA_manual'),
        'validado': False,
        'fecha_validacion': None,
        'validado_por': None,
        'id_temporal': f"temp_{metadata_global.get('archivo_fuente', 'unknown').replace(' ', '_')}_{tipo_registro}_{indice + 1}"
    }
    
    return metadata_registro

def transformar_archivo_json(ruta_entrada, ruta_salida=None):
    """
    Transforma un archivo JSON añadiendo metadata_registro a cada registro
    
    Args:
        ruta_entrada: Ruta al archivo JSON original
        ruta_salida: Ruta donde guardar el archivo transformado (opcional)
    """
    # Cargar archivo
    with open(ruta_entrada, 'r', encoding='utf-8') as f:
        datos = json.load(f)
    
    metadata = datos.get('metadata', {})
    
    # Transformar obras
    obras = datos.get('obras', [])
    obras_transformadas = []
    for i, obra in enumerate(obras):
        datos_obra = obra.get('datos', obra)
        metadata_obra = añadir_metadata_registro(obra, metadata, 'obra', i)
        obras_transformadas.append({
            'datos': datos_obra,
            'metadata_registro': metadata_obra
        })
    
    # Transformar representaciones
    representaciones = datos.get('representaciones', [])
    representaciones_transformadas = []
    for i, rep in enumerate(representaciones):
        # Si ya tiene estructura 'datos', mantenerla; si no, crear estructura
        if 'datos' in rep:
            datos_rep = rep['datos']
            metadata_rep = rep.get('metadata_registro', {})
            if not metadata_rep:
                metadata_rep = añadir_metadata_registro(rep, metadata, 'representacion', i)
        else:
            datos_rep = rep
            metadata_rep = añadir_metadata_registro(rep, metadata, 'representacion', i)
        
        representaciones_transformadas.append({
            'datos': datos_rep,
            'metadata_registro': metadata_rep
        })
    
    # Transformar lugares
    lugares = datos.get('lugares_nuevos', [])
    lugares_transformados = []
    for i, lugar in enumerate(lugares):
        datos_lugar = lugar.get('datos', lugar)
        metadata_lugar = añadir_metadata_registro(lugar, metadata, 'lugar', i)
        lugares_transformados.append({
            'datos': datos_lugar,
            'metadata_registro': metadata_lugar
        })
    
    # Crear estructura transformada
    datos_transformados = {
        'metadata': metadata,
        'obras': obras_transformadas,
        'representaciones': representaciones_transformadas,
        'lugares_nuevos': lugares_transformados,
        # Mantener otros campos
        'mecenas_unicos': datos.get('mecenas_unicos', []),
        'personajes_historicos': datos.get('personajes_historicos', []),
        'titulos_alternativos': datos.get('titulos_alternativos', []),
        'compañias_identificadas': datos.get('compañias_identificadas', []),
        'notas_contextuales': datos.get('notas_contextuales', []),
        'resumen_estadisticas': datos.get('resumen_estadisticas', {})
    }
    
    # Guardar archivo transformado
    if not ruta_salida:
        ruta_salida = ruta_entrada.replace('.json', '_con_metadata.json')
    
    with open(ruta_salida, 'w', encoding='utf-8') as f:
        json.dump(datos_transformados, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Archivo transformado guardado en: {ruta_salida}")
    print(f"   - Obras: {len(obras_transformadas)}")
    print(f"   - Representaciones: {len(representaciones_transformadas)}")
    print(f"   - Lugares: {len(lugares_transformados)}")
    
    return ruta_salida

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Uso: python actualizar_metadata_versionado.py <archivo_json> [archivo_salida]")
        sys.exit(1)
    
    ruta_entrada = sys.argv[1]
    ruta_salida = sys.argv[2] if len(sys.argv) > 2 else None
    
    transformar_archivo_json(ruta_entrada, ruta_salida)






