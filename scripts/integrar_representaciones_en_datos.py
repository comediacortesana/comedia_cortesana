#!/usr/bin/env python3
"""
Script para integrar representaciones normalizadas en datos_obras.json

Convierte el formato de representaciones normalizadas al formato esperado por el frontend
y las integra en datos_obras.json para que se muestren en la tabla y se puedan filtrar.
"""

import json
from pathlib import Path
from typing import Dict, List
from collections import defaultdict


def convertir_formato_representacion(rep: Dict) -> Dict:
    """
    Convierte representación del formato normalizado al formato esperado por frontend
    """
    return {
        'fecha': rep.get('fecha', ''),
        'fecha_formateada': rep.get('fecha_formateada', ''),
        'lugar': rep.get('lugar_nombre', ''),
        'region': rep.get('lugar_region', ''),
        'pais': '',  # Se puede inferir después
        'tipo_lugar': rep.get('lugar_tipo', ''),
        'compania': rep.get('compañia', '') or rep.get('compania', ''),
        'director_compañia': rep.get('director_compañia', '') or rep.get('director_compania', ''),
        'mecenas': rep.get('mecenas', ''),
        'gestor_administrativo': rep.get('gestor_administrativo', ''),
        'personajes_historicos': rep.get('personajes_historicos', ''),
        'organizadores_fiesta': rep.get('organizadores_fiesta', ''),
        'tipo_funcion': rep.get('tipo_funcion', ''),
        'publico': rep.get('publico', ''),
        'entrada': rep.get('entrada', ''),
        'duracion': rep.get('duracion', ''),
        'observaciones': rep.get('observaciones', ''),
        'notas': rep.get('notas', ''),
        'fuente': rep.get('fuente', ''),
        'pagina_pdf': rep.get('pagina_pdf'),
        'texto_original_pdf': rep.get('texto_original', ''),
        'es_anterior_1650': False,  # Se calculará después si es necesario
        'es_anterior_1665': False,  # Se calculará después si es necesario
    }


def extraer_año_de_fecha(fecha_formateada: str) -> int:
    """Extrae el año de una fecha formateada"""
    if fecha_formateada and len(fecha_formateada) >= 4:
        try:
            return int(fecha_formateada[:4])
        except:
            return None
    return None


def integrar_representaciones():
    """Integra representaciones normalizadas en datos_obras.json"""
    base_dir = Path(__file__).parent.parent
    
    # Cargar datos_obras.json
    datos_file = base_dir / 'datos_obras.json'
    if not datos_file.exists():
        print(f"❌ No se encontró {datos_file}")
        return
    
    print(f"📖 Cargando {datos_file}...")
    with open(datos_file, 'r', encoding='utf-8') as f:
        datos = json.load(f)
    
    obras = datos.get('obras', [])
    print(f"   Encontradas {len(obras)} obras")
    
    # Cargar representaciones normalizadas
    reps_file = base_dir / 'data' / 'representaciones_normalizadas.json'
    if not reps_file.exists():
        print(f"❌ No se encontró {reps_file}")
        print("   Ejecuta primero: python scripts/normalize_representaciones.py")
        return
    
    print(f"📖 Cargando {reps_file}...")
    with open(reps_file, 'r', encoding='utf-8') as f:
        reps_data = json.load(f)
    
    # Crear índice de representaciones por título de obra
    reps_por_obra = defaultdict(list)
    for rep in reps_data.get('representaciones', []):
        titulo = rep.get('obra_titulo', '').strip()
        if titulo:
            reps_por_obra[titulo.lower()].append(rep)
    
    print(f"   Encontradas representaciones para {len(reps_por_obra)} obras")
    
    # Integrar representaciones en obras
    obras_actualizadas = 0
    total_reps_agregadas = 0
    
    for obra in obras:
        titulo = obra.get('Título', '') or obra.get('titulo', '')
        titulo_lower = titulo.lower().strip()
        
        if titulo_lower in reps_por_obra:
            # Convertir representaciones al formato esperado
            representaciones = []
            for rep_normalizada in reps_por_obra[titulo_lower]:
                rep_formateada = convertir_formato_representacion(rep_normalizada)
                
                # Calcular campos de época
                año = extraer_año_de_fecha(rep_formateada.get('fecha_formateada', ''))
                if año:
                    rep_formateada['es_anterior_1650'] = año < 1650
                    rep_formateada['es_anterior_1665'] = año < 1665
                
                representaciones.append(rep_formateada)
            
            # Agregar representaciones a la obra
            obra['representaciones'] = representaciones
            obra['total_representaciones'] = len(representaciones)
            
            # También actualizar campos legacy (primera representación)
            if representaciones:
                primera_rep = representaciones[0]
                obra['lugar'] = primera_rep.get('lugar', '')
                obra['region'] = primera_rep.get('region', '')
                obra['tipo_lugar'] = primera_rep.get('tipo_lugar', '')
                obra['compania'] = primera_rep.get('compania', '')
                obra['director_compañia'] = primera_rep.get('director_compañia', '')
            
            obras_actualizadas += 1
            total_reps_agregadas += len(representaciones)
    
    # Guardar archivo actualizado
    print(f"\n💾 Guardando archivo actualizado...")
    with open(datos_file, 'w', encoding='utf-8') as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)
    
    # También guardar backup
    backup_file = base_dir / 'datos_obras.json.backup'
    print(f"💾 Guardando backup en {backup_file}...")
    with open(backup_file, 'w', encoding='utf-8') as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Integración completada:")
    print(f"   - Obras actualizadas: {obras_actualizadas}")
    print(f"   - Representaciones agregadas: {total_reps_agregadas}")
    print(f"   - Archivo guardado: {datos_file}")
    print(f"   - Backup guardado: {backup_file}")
    
    # Estadísticas
    obras_con_reps = sum(1 for obra in obras if obra.get('representaciones'))
    reps_con_fecha = sum(
        sum(1 for rep in obra.get('representaciones', []) if rep.get('fecha_formateada'))
        for obra in obras
    )
    reps_con_lugar = sum(
        sum(1 for rep in obra.get('representaciones', []) if rep.get('lugar'))
        for obra in obras
    )
    
    print(f"\n📊 Estadísticas finales:")
    print(f"   - Obras con representaciones: {obras_con_reps}")
    print(f"   - Representaciones con fecha: {reps_con_fecha}")
    print(f"   - Representaciones con lugar: {reps_con_lugar}")


if __name__ == '__main__':
    integrar_representaciones()
