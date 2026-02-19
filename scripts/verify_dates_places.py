#!/usr/bin/env python3
"""
Script para verificar y generar estadísticas de cobertura de fechas y lugares

Analiza los datos guardados y genera un reporte sobre:
- Obras con representaciones estructuradas
- Representaciones con fechas extraídas
- Representaciones con lugares normalizados
- Cobertura por fuente (CATCOM vs FUENTESIX)
"""

import json
from pathlib import Path
from typing import Dict, List
from datetime import datetime


def analizar_datos_json(datos_path: Path) -> Dict:
    """Analiza el archivo datos_obras.json"""
    if not datos_path.exists():
        return None
    
    try:
        with open(datos_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error leyendo {datos_path}: {e}")
        return None
    
    obras = data.get('obras', [])
    
    stats = {
        'total_obras': len(obras),
        'obras_con_representaciones': 0,
        'total_representaciones': 0,
        'representaciones_con_fecha': 0,
        'representaciones_con_fecha_formateada': 0,
        'representaciones_con_lugar': 0,
        'representaciones_con_region': 0,
        'representaciones_con_compania': 0,
        'por_fuente': {},
        'obras_sin_fecha': [],
        'obras_sin_lugar': [],
    }
    
    for obra in obras:
        fuente = obra.get('fuente', 'DESCONOCIDA')
        if fuente not in stats['por_fuente']:
            stats['por_fuente'][fuente] = {
                'total_obras': 0,
                'obras_con_representaciones': 0,
                'total_representaciones': 0,
                'representaciones_con_fecha': 0,
                'representaciones_con_lugar': 0,
            }
        
        stats['por_fuente'][fuente]['total_obras'] += 1
        
        representaciones = obra.get('representaciones', [])
        if representaciones:
            stats['obras_con_representaciones'] += 1
            stats['por_fuente'][fuente]['obras_con_representaciones'] += 1
            stats['total_representaciones'] += len(representaciones)
            stats['por_fuente'][fuente]['total_representaciones'] += len(representaciones)
            
            tiene_fecha = False
            tiene_lugar = False
            
            for rep in representaciones:
                if rep.get('fecha'):
                    stats['representaciones_con_fecha'] += 1
                    stats['por_fuente'][fuente]['representaciones_con_fecha'] += 1
                    tiene_fecha = True
                
                if rep.get('fecha_formateada'):
                    stats['representaciones_con_fecha_formateada'] += 1
                
                if rep.get('lugar'):
                    stats['representaciones_con_lugar'] += 1
                    stats['por_fuente'][fuente]['representaciones_con_lugar'] += 1
                    tiene_lugar = True
                
                if rep.get('region'):
                    stats['representaciones_con_region'] += 1
                
                if rep.get('compania'):
                    stats['representaciones_con_compania'] += 1
            
            if not tiene_fecha:
                stats['obras_sin_fecha'].append({
                    'titulo': obra.get('titulo', 'Sin título'),
                    'id': obra.get('id'),
                    'fuente': fuente
                })
            
            if not tiene_lugar:
                stats['obras_sin_lugar'].append({
                    'titulo': obra.get('titulo', 'Sin título'),
                    'id': obra.get('id'),
                    'fuente': fuente
                })
    
    return stats


def analizar_representaciones_normalizadas(normalizadas_path: Path) -> Dict:
    """Analiza el archivo de representaciones normalizadas"""
    if not normalizadas_path.exists():
        return None
    
    try:
        with open(normalizadas_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error leyendo {normalizadas_path}: {e}")
        return None
    
    representaciones = data.get('representaciones', [])
    
    stats = {
        'total_representaciones': len(representaciones),
        'con_fecha': sum(1 for r in representaciones if r.get('fecha')),
        'con_fecha_formateada': sum(1 for r in representaciones if r.get('fecha_formateada')),
        'con_lugar': sum(1 for r in representaciones if r.get('lugar_nombre')),
        'con_region': sum(1 for r in representaciones if r.get('lugar_region')),
        'con_compania': sum(1 for r in representaciones if r.get('compañia')),
        'por_fuente': {}
    }
    
    for rep in representaciones:
        fuente = rep.get('fuente', 'DESCONOCIDA')
        if fuente not in stats['por_fuente']:
            stats['por_fuente'][fuente] = {
                'total': 0,
                'con_fecha': 0,
                'con_lugar': 0,
            }
        
        stats['por_fuente'][fuente]['total'] += 1
        if rep.get('fecha'):
            stats['por_fuente'][fuente]['con_fecha'] += 1
        if rep.get('lugar_nombre'):
            stats['por_fuente'][fuente]['con_lugar'] += 1
    
    return stats


def generar_reporte(stats_json: Dict, stats_normalizadas: Dict = None):
    """Genera un reporte de estadísticas"""
    print("\n" + "="*80)
    print("📊 REPORTE DE COBERTURA DE FECHAS Y LUGARES")
    print("="*80 + "\n")
    
    if stats_json:
        print("📁 DATOS DE datos_obras.json")
        print("-" * 80)
        print(f"Total obras: {stats_json['total_obras']}")
        print(f"Obras con representaciones: {stats_json['obras_con_representaciones']} ({stats_json['obras_con_representaciones']/stats_json['total_obras']*100:.1f}%)")
        print(f"Total representaciones: {stats_json['total_representaciones']}")
        print(f"\nRepresentaciones con:")
        print(f"  - Fecha: {stats_json['representaciones_con_fecha']} ({stats_json['representaciones_con_fecha']/max(stats_json['total_representaciones'], 1)*100:.1f}%)")
        print(f"  - Fecha formateada: {stats_json['representaciones_con_fecha_formateada']} ({stats_json['representaciones_con_fecha_formateada']/max(stats_json['total_representaciones'], 1)*100:.1f}%)")
        print(f"  - Lugar: {stats_json['representaciones_con_lugar']} ({stats_json['representaciones_con_lugar']/max(stats_json['total_representaciones'], 1)*100:.1f}%)")
        print(f"  - Región: {stats_json['representaciones_con_region']} ({stats_json['representaciones_con_region']/max(stats_json['total_representaciones'], 1)*100:.1f}%)")
        print(f"  - Compañía: {stats_json['representaciones_con_compania']} ({stats_json['representaciones_con_compania']/max(stats_json['total_representaciones'], 1)*100:.1f}%)")
        
        print(f"\nPor fuente:")
        for fuente, datos in stats_json['por_fuente'].items():
            print(f"\n  {fuente}:")
            print(f"    Obras: {datos['total_obras']}")
            print(f"    Obras con representaciones: {datos['obras_con_representaciones']}")
            print(f"    Representaciones: {datos['total_representaciones']}")
            if datos['total_representaciones'] > 0:
                print(f"    Con fecha: {datos['representaciones_con_fecha']} ({datos['representaciones_con_fecha']/datos['total_representaciones']*100:.1f}%)")
                print(f"    Con lugar: {datos['representaciones_con_lugar']} ({datos['representaciones_con_lugar']/datos['total_representaciones']*100:.1f}%)")
        
        if stats_json['obras_sin_fecha']:
            print(f"\n⚠️ Obras sin fecha ({len(stats_json['obras_sin_fecha'])}):")
            for obra in stats_json['obras_sin_fecha'][:10]:
                print(f"  - {obra['titulo']} (ID: {obra['id']}, Fuente: {obra['fuente']})")
            if len(stats_json['obras_sin_fecha']) > 10:
                print(f"  ... y {len(stats_json['obras_sin_fecha']) - 10} más")
        
        if stats_json['obras_sin_lugar']:
            print(f"\n⚠️ Obras sin lugar ({len(stats_json['obras_sin_lugar'])}):")
            for obra in stats_json['obras_sin_lugar'][:10]:
                print(f"  - {obra['titulo']} (ID: {obra['id']}, Fuente: {obra['fuente']})")
            if len(stats_json['obras_sin_lugar']) > 10:
                print(f"  ... y {len(stats_json['obras_sin_lugar']) - 10} más")
    
    if stats_normalizadas:
        print("\n" + "="*80)
        print("📁 DATOS DE representaciones_normalizadas.json")
        print("-" * 80)
        print(f"Total representaciones: {stats_normalizadas['total_representaciones']}")
        print(f"Con fecha: {stats_normalizadas['con_fecha']} ({stats_normalizadas['con_fecha']/max(stats_normalizadas['total_representaciones'], 1)*100:.1f}%)")
        print(f"Con fecha formateada: {stats_normalizadas['con_fecha_formateada']} ({stats_normalizadas['con_fecha_formateada']/max(stats_normalizadas['total_representaciones'], 1)*100:.1f}%)")
        print(f"Con lugar: {stats_normalizadas['con_lugar']} ({stats_normalizadas['con_lugar']/max(stats_normalizadas['total_representaciones'], 1)*100:.1f}%)")
        print(f"Con región: {stats_normalizadas['con_region']} ({stats_normalizadas['con_region']/max(stats_normalizadas['total_representaciones'], 1)*100:.1f}%)")
        print(f"Con compañía: {stats_normalizadas['con_compania']} ({stats_normalizadas['con_compania']/max(stats_normalizadas['total_representaciones'], 1)*100:.1f}%)")
        
        print(f"\nPor fuente:")
        for fuente, datos in stats_normalizadas['por_fuente'].items():
            print(f"\n  {fuente}:")
            print(f"    Total: {datos['total']}")
            if datos['total'] > 0:
                print(f"    Con fecha: {datos['con_fecha']} ({datos['con_fecha']/datos['total']*100:.1f}%)")
                print(f"    Con lugar: {datos['con_lugar']} ({datos['con_lugar']/datos['total']*100:.1f}%)")
    
    print("\n" + "="*80 + "\n")


def main():
    """Función principal"""
    base_dir = Path(__file__).parent.parent
    
    # Analizar datos_obras.json
    datos_path = base_dir / 'datos_obras.json'
    stats_json = analizar_datos_json(datos_path)
    
    # Analizar representaciones normalizadas
    normalizadas_path = base_dir / 'data' / 'representaciones_normalizadas.json'
    stats_normalizadas = analizar_representaciones_normalizadas(normalizadas_path)
    
    # Generar reporte
    generar_reporte(stats_json, stats_normalizadas)
    
    # Guardar reporte en archivo
    reporte_path = base_dir / 'data' / 'reporte_cobertura_fechas_lugares.json'
    reporte_data = {
        'fecha_generacion': datetime.now().isoformat(),
        'datos_obras': stats_json,
        'representaciones_normalizadas': stats_normalizadas
    }
    
    with open(reporte_path, 'w', encoding='utf-8') as f:
        json.dump(reporte_data, f, ensure_ascii=False, indent=2)
    
    print(f"📄 Reporte guardado en: {reporte_path}")


if __name__ == '__main__':
    main()
