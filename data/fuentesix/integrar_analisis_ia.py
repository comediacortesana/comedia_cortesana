#!/usr/bin/env python3
"""
Script para integrar análisis de IA a la base de datos

Toma los datos extraídos y sus análisis, y los guarda en la tabla
analisis_ia_fuentes_ix de Supabase.
"""

import json
import sys
from datetime import datetime
from sistema_analisis_ia import AnalisisIA

def procesar_extraccion_con_analisis(archivo_extraccion: str, archivo_analisis: str = None):
    """
    Procesa un archivo de extracción y genera análisis de IA para cada registro
    
    Args:
        archivo_extraccion: Ruta al archivo JSON de extracción
        archivo_analisis: Ruta opcional al archivo JSON de análisis inteligente
    """
    # Cargar datos extraídos
    with open(archivo_extraccion, 'r', encoding='utf-8') as f:
        datos_extraccion = json.load(f)
    
    metadata = datos_extraccion.get('metadata', {})
    analisis_ia = AnalisisIA()
    
    # Procesar representaciones
    representaciones = datos_extraccion.get('representaciones', [])
    for i, rep in enumerate(representaciones):
        datos_rep = rep.get('datos', rep)
        metadata_rep = rep.get('metadata_registro', {})
        
        # Extraer frases originales
        frases_originales = []
        if datos_rep.get('texto_original'):
            frases_originales.append(datos_rep['texto_original'])
        
        # Generar interpretaciones basadas en observaciones
        interpretaciones = []
        if datos_rep.get('observaciones'):
            obs = datos_rep['observaciones']
            if 'DISCREPANCIA' in obs:
                interpretaciones.append(f"Discrepancia detectada: {obs}")
            else:
                interpretaciones.append(obs)
        
        # Detectar discrepancias
        discrepancias = []
        if 'DISCREPANCIA' in datos_rep.get('observaciones', ''):
            # Parsear discrepancias del texto de observaciones
            discrepancias.append({
                'tipo': 'general',
                'descripcion': datos_rep.get('observaciones', ''),
                'confianza': datos_rep.get('confianza', 'medio')
            })
        
        # Crear análisis
        analisis_ia.crear_analisis_registro(
            tipo_registro='representacion',
            registro_id=metadata_rep.get('id_temporal', f"temp_rep_{i}"),
            datos_extraidos={
                'obra_titulo': datos_rep.get('obra_titulo'),
                'fecha': datos_rep.get('fecha'),
                'compañia': datos_rep.get('compañia'),
                'lugar': datos_rep.get('lugar_nombre')
            },
            frases_originales=frases_originales,
            interpretaciones=interpretaciones,
            discrepancias=discrepancias,
            confianza=datos_rep.get('confianza', 'medio'),
            contexto_adicional={
                'archivo_fuente': metadata.get('archivo_fuente'),
                'pagina_pdf': datos_rep.get('pagina_pdf'),
                'version_extraccion': metadata.get('version_extraccion')
            }
        )
    
    # Procesar lugares
    lugares = datos_extraccion.get('lugares_nuevos', [])
    for i, lugar in enumerate(lugares):
        datos_lugar = lugar.get('datos', lugar)
        metadata_lugar = lugar.get('metadata_registro', {})
        
        analisis_ia.crear_analisis_registro(
            tipo_registro='lugar',
            registro_id=metadata_lugar.get('id_temporal', f"temp_lugar_{i}"),
            datos_extraidos={
                'nombre': datos_lugar.get('nombre'),
                'tipo': datos_lugar.get('tipo'),
                'region': datos_lugar.get('region')
            },
            frases_originales=[],
            interpretaciones=[f"Lugar identificado: {datos_lugar.get('nombre')}"],
            confianza='alto',
            contexto_adicional={
                'archivo_fuente': metadata.get('archivo_fuente'),
                'variantes': datos_lugar.get('variantes', [])
            }
        )
    
    # Guardar análisis
    archivo_salida = archivo_extraccion.replace('.json', '_analisis_ia.json')
    analisis_ia.guardar_analisis(archivo_salida)
    
    print(f"\n✅ Análisis generados:")
    print(f"   - Representaciones: {len(representaciones)}")
    print(f"   - Lugares: {len(lugares)}")
    print(f"   - Total análisis: {len(analisis_ia.analisis)}")
    
    return archivo_salida


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Uso: python integrar_analisis_ia.py <archivo_extraccion.json> [archivo_analisis.json]")
        sys.exit(1)
    
    archivo_extraccion = sys.argv[1]
    archivo_analisis = sys.argv[2] if len(sys.argv) > 2 else None
    
    procesar_extraccion_con_analisis(archivo_extraccion, archivo_analisis)






