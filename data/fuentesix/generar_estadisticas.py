#!/usr/bin/env python3
"""
Script para generar estadísticas y análisis de completitud de datos
"""

import json
from pathlib import Path
from collections import defaultdict
from datetime import datetime

BASE_DIR = Path(__file__).parent.parent.parent
DATOS_OBRAS = BASE_DIR / "datos_obras.json"
CONTEXTO_FUENTESIX = Path(__file__).parent / "contexto_extraido_por_tipo.json"

def normalizarFuente(fuente):
    """Normaliza fuente"""
    if not fuente:
        return ""
    limpio = str(fuente).strip().upper().replace(" ", "")
    if "FUENTESIX" in limpio or "FUENTESXI" in limpio:
        return "FUENTES IX"
    return fuente.strip()

def analizar_completitud():
    """Analiza completitud de campos en las obras"""
    print("📊 Analizando completitud de datos...")
    
    with open(DATOS_OBRAS, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    obras = data.get("obras", [])
    
    # Campos a analizar
    campos_obra = {
        "titulo": "Título",
        "titulo_original": "Título Original",
        "titulo_alternativo": "Títulos Alternativos",
        "autor": "Autor",
        "tipo_obra": "Tipo de Obra",
        "genero": "Género",
        "subgenero": "Subgénero",
        "fecha_creacion": "Fecha de Creación",
        "tema": "Tema",
        "mecenas": "Mecenas",
        "edicion_principe": "Edición Príncipe",
        "notas_bibliograficas": "Notas Bibliográficas",
        "manuscritos_conocidos": "Manuscritos Conocidos",
        "representaciones": "Representaciones"
    }
    
    campos_autor = {
        "nombre": "Nombre",
        "nombre_completo": "Nombre Completo",
        "fecha_nacimiento": "Fecha Nacimiento",
        "fecha_muerte": "Fecha Muerte",
        "biografia": "Biografía"
    }
    
    # Estadísticas por fuente
    stats_por_fuente = defaultdict(lambda: {
        "total": 0,
        "campos_obra": defaultdict(int),
        "campos_autor": defaultdict(int),
        "con_representaciones": 0,
        "total_representaciones": 0,
        "con_fecha": 0,
        "con_lugar": 0,
        "con_compania": 0
    })
    
    # Estadísticas generales
    stats_general = {
        "total_obras": len(obras),
        "por_fuente": defaultdict(int),
        "campos_completitud": {},
        "representaciones_stats": {
            "total": 0,
            "con_fecha": 0,
            "con_lugar": 0,
            "con_compania": 0,
            "lugares_unicos": set(),
            "companias_unicas": set()
        }
    }
    
    for obra in obras:
        fuente = normalizarFuente(obra.get("fuente", ""))
        stats_por_fuente[fuente]["total"] += 1
        stats_general["por_fuente"][fuente] += 1
        
        # Analizar campos de obra
        for campo_key, campo_nombre in campos_obra.items():
            valor = obra.get(campo_key)
            if valor:
                if isinstance(valor, str) and valor.strip():
                    stats_por_fuente[fuente]["campos_obra"][campo_key] += 1
                elif isinstance(valor, list) and len(valor) > 0:
                    stats_por_fuente[fuente]["campos_obra"][campo_key] += 1
                elif isinstance(valor, dict) and valor:
                    stats_por_fuente[fuente]["campos_obra"][campo_key] += 1
                elif not isinstance(valor, (str, list, dict)):
                    stats_por_fuente[fuente]["campos_obra"][campo_key] += 1
        
        # Analizar autor
        autor = obra.get("autor", {})
        if isinstance(autor, dict):
            for campo_key, campo_nombre in campos_autor.items():
                valor = autor.get(campo_key)
                if valor and (isinstance(valor, str) and valor.strip()):
                    stats_por_fuente[fuente]["campos_autor"][campo_key] += 1
        
        # Analizar representaciones
        representaciones = obra.get("representaciones", [])
        if representaciones:
            stats_por_fuente[fuente]["con_representaciones"] += 1
            stats_por_fuente[fuente]["total_representaciones"] += len(representaciones)
            stats_general["representaciones_stats"]["total"] += len(representaciones)
            
            for rep in representaciones:
                if rep.get("fecha") or rep.get("fecha_formateada"):
                    stats_por_fuente[fuente]["con_fecha"] += 1
                    stats_general["representaciones_stats"]["con_fecha"] += 1
                
                if rep.get("lugar"):
                    stats_por_fuente[fuente]["con_lugar"] += 1
                    stats_general["representaciones_stats"]["con_lugar"] += 1
                    stats_general["representaciones_stats"]["lugares_unicos"].add(rep.get("lugar"))
                
                if rep.get("compania"):
                    stats_por_fuente[fuente]["con_compania"] += 1
                    stats_general["representaciones_stats"]["con_compania"] += 1
                    stats_general["representaciones_stats"]["companias_unicas"].add(rep.get("compania"))
        
        # Fecha de creación
        if obra.get("fecha_creacion") and obra.get("fecha_creacion") not in ["", "No especificada"]:
            stats_por_fuente[fuente]["con_fecha"] += 1
        
        # Lugar principal
        if obra.get("lugar"):
            stats_por_fuente[fuente]["con_lugar"] += 1
    
    # Calcular porcentajes de completitud
    completitud_por_fuente = {}
    for fuente, stats in stats_por_fuente.items():
        total = stats["total"]
        if total == 0:
            continue
        
        completitud = {
            "total_obras": total,
            "campos_obra": {},
            "campos_autor": {},
            "representaciones": {
                "obras_con_reps": stats["con_representaciones"],
                "porcentaje_con_reps": (stats["con_representaciones"] / total * 100) if total > 0 else 0,
                "total_reps": stats["total_representaciones"],
                "promedio_reps": (stats["total_representaciones"] / total) if total > 0 else 0,
                "reps_con_fecha": stats["con_fecha"],
                "reps_con_lugar": stats["con_lugar"],
                "reps_con_compania": stats["con_compania"]
            }
        }
        
        for campo_key, campo_nombre in campos_obra.items():
            count = stats["campos_obra"][campo_key]
            completitud["campos_obra"][campo_key] = {
                "nombre": campo_nombre,
                "completas": count,
                "porcentaje": (count / total * 100) if total > 0 else 0
            }
        
        for campo_key, campo_nombre in campos_autor.items():
            count = stats["campos_autor"][campo_key]
            completitud["campos_autor"][campo_key] = {
                "nombre": campo_nombre,
                "completas": count,
                "porcentaje": (count / total * 100) if total > 0 else 0
            }
        
        completitud_por_fuente[fuente] = completitud
    
    # Convertir sets a listas para JSON
    stats_general["representaciones_stats"]["lugares_unicos"] = len(stats_general["representaciones_stats"]["lugares_unicos"])
    stats_general["representaciones_stats"]["companias_unicas"] = len(stats_general["representaciones_stats"]["companias_unicas"])
    
    return {
        "fecha_analisis": datetime.now().isoformat(),
        "estadisticas_generales": stats_general,
        "completitud_por_fuente": completitud_por_fuente
    }

def analizar_fuentesix_especifico():
    """Análisis específico de FUENTES IX"""
    print("🔍 Analizando FUENTES IX específicamente...")
    
    with open(CONTEXTO_FUENTESIX, 'r', encoding='utf-8') as f:
        contexto = json.load(f)
    
    obras_fuentesix = contexto.get("obras", [])
    
    # Análisis
    obras_sin_autor = []
    obras_sin_representaciones = []
    obras_con_referencias_cruzadas = []
    titulos_alternativos_count = 0
    
    for obra in obras_fuentesix:
        if not obra.get("autor") or obra.get("autor") == "Anónimo":
            obras_sin_autor.append(obra.get("titulo", ""))
        
        if not obra.get("representaciones") or len(obra.get("representaciones", [])) == 0:
            obras_sin_representaciones.append(obra.get("titulo", ""))
        
        if obra.get("referencias_cruzadas"):
            obras_con_referencias_cruzadas.append({
                "titulo": obra.get("titulo", ""),
                "referencias": obra.get("referencias_cruzadas", [])
            })
        
        if obra.get("titulos_alternativos"):
            titulos_alternativos_count += len(obra.get("titulos_alternativos", []))
    
    # Análisis de representaciones
    fechas_por_año = defaultdict(int)
    lugares_frecuentes = defaultdict(int)
    companias_frecuentes = defaultdict(int)
    
    for obra in obras_fuentesix:
        for rep in obra.get("representaciones", []):
            fecha = rep.get("fecha", "")
            # Extraer año
            import re
            match = re.search(r'(\d{4})', fecha)
            if match:
                año = int(match.group(1))
                if 1600 <= año <= 1710:
                    fechas_por_año[año] += 1
            
            lugar = rep.get("lugar", "")
            if lugar:
                lugares_frecuentes[lugar] += 1
            
            compania = rep.get("compania", "")
            if compania:
                companias_frecuentes[compania] += 1
    
    return {
        "total_obras": len(obras_fuentesix),
        "obras_sin_autor": {
            "total": len(obras_sin_autor),
            "porcentaje": (len(obras_sin_autor) / len(obras_fuentesix) * 100) if obras_fuentesix else 0,
            "ejemplos": obras_sin_autor[:10]
        },
        "obras_sin_representaciones": {
            "total": len(obras_sin_representaciones),
            "porcentaje": (len(obras_sin_representaciones) / len(obras_fuentesix) * 100) if obras_fuentesix else 0,
            "ejemplos": obras_sin_representaciones[:10]
        },
        "obras_con_referencias_cruzadas": {
            "total": len(obras_con_referencias_cruzadas),
            "ejemplos": obras_con_referencias_cruzadas[:5]
        },
        "titulos_alternativos": {
            "total": titulos_alternativos_count,
            "promedio_por_obra": (titulos_alternativos_count / len(obras_fuentesix)) if obras_fuentesix else 0
        },
        "distribucion_temporal": dict(sorted(fechas_por_año.items())),
        "lugares_mas_frecuentes": dict(sorted(lugares_frecuentes.items(), key=lambda x: -x[1])[:20]),
        "companias_mas_frecuentes": dict(sorted(companias_frecuentes.items(), key=lambda x: -x[1])[:20])
    }

def generar_conclusiones(stats_completitud, stats_fuentesix):
    """Genera conclusiones y recomendaciones"""
    conclusiones = []
    recomendaciones = []
    
    # Análisis de completitud
    fuentesix_stats = stats_completitud["completitud_por_fuente"].get("FUENTES IX", {})
    catcom_stats = stats_completitud["completitud_por_fuente"].get("CATCOM", {})
    
    conclusiones.append({
        "titulo": "Completitud de Datos por Fuente",
        "contenido": f"""
        <p><strong>FUENTES IX</strong> aporta {fuentesix_stats.get('total_obras', 0)} obras, de las cuales:</p>
        <ul>
            <li>{fuentesix_stats.get('representaciones', {}).get('obras_con_reps', 0)} tienen representaciones ({fuentesix_stats.get('representaciones', {}).get('porcentaje_con_reps', 0):.1f}%)</li>
            <li>Total de {fuentesix_stats.get('representaciones', {}).get('total_reps', 0)} representaciones documentadas</li>
            <li>Promedio de {fuentesix_stats.get('representaciones', {}).get('promedio_reps', 0):.2f} representaciones por obra</li>
        </ul>
        <p><strong>CATCOM</strong> tiene {catcom_stats.get('total_obras', 0)} obras, pero menor porcentaje de representaciones documentadas.</p>
        """
    })
    
    # Análisis de campos faltantes
    campos_faltantes_fuentesix = []
    for campo_key, campo_data in fuentesix_stats.get("campos_obra", {}).items():
        if campo_data["porcentaje"] < 50:
            campos_faltantes_fuentesix.append({
                "campo": campo_data["nombre"],
                "completitud": campo_data["porcentaje"]
            })
    
    if campos_faltantes_fuentesix:
        conclusiones.append({
            "titulo": "Campos con Baja Completitud en FUENTES IX",
            "contenido": f"""
            <p>Los siguientes campos tienen menos del 50% de completitud:</p>
            <ul>
                {''.join([f"<li><strong>{c['campo']}</strong>: {c['completitud']:.1f}%</li>" for c in campos_faltantes_fuentesix])}
            </ul>
            """
        })
    
    # Análisis específico FUENTES IX
    stats_fix = stats_fuentesix
    conclusiones.append({
        "titulo": "Análisis Específico de FUENTES IX",
        "contenido": f"""
        <p>Del análisis del volumen FUENTES IX se desprende:</p>
        <ul>
            <li><strong>{stats_fix['obras_sin_autor']['total']}</strong> obras sin autor identificado ({stats_fix['obras_sin_autor']['porcentaje']:.1f}%)</li>
            <li><strong>{stats_fix['obras_sin_representaciones']['total']}</strong> obras sin representaciones documentadas ({stats_fix['obras_sin_representaciones']['porcentaje']:.1f}%)</li>
            <li><strong>{stats_fix['obras_con_referencias_cruzadas']['total']}</strong> obras con referencias cruzadas a otros títulos</li>
            <li><strong>{stats_fix['titulos_alternativos']['total']}</strong> títulos alternativos identificados</li>
        </ul>
        """
    })
    
    # Distribución temporal
    distribucion = stats_fix.get("distribucion_temporal", {})
    if distribucion:
        años_con_datos = sorted(distribucion.keys())
        conclusiones.append({
            "titulo": "Distribución Temporal de Representaciones",
            "contenido": f"""
            <p>Las representaciones documentadas en FUENTES IX abarcan desde <strong>{min(años_con_datos)}</strong> hasta <strong>{max(años_con_datos)}</strong>.</p>
            <p>Picos de actividad:</p>
            <ul>
                {''.join([f"<li><strong>{año}</strong>: {count} representaciones</li>" for año, count in sorted(distribucion.items(), key=lambda x: -x[1])[:5]])}
            </ul>
            """
        })
    
    # Recomendaciones
    recomendaciones.append({
        "titulo": "Búsqueda de Autores Faltantes",
        "contenido": """
        <p>Para completar los autores faltantes en FUENTES IX, buscar en:</p>
        <ul>
            <li><strong>Catálogo de Barrera y Leirado</strong>: Referencia fundamental mencionada en el prefacio</li>
            <li><strong>Catálogos de Fajardo, Medel del Castillo, García de la Huerta</strong>: Citados frecuentemente en FUENTES IX</li>
            <li><strong>Biblioteca Nacional de Madrid</strong>: Catálogo de manuscritos de Julián Paz</li>
            <li><strong>Biblioteca Municipal de Madrid</strong>: Catálogo de Carlos Cambronero (sustituido por Mercedes Agulló y Cobo)</li>
            <li><strong>Biblioteca del Instituto del Teatro de Barcelona</strong>: Catálogo de María del Carmen Simón Palmer</li>
        </ul>
        """
    })
    
    recomendaciones.append({
        "titulo": "Búsqueda de Ediciones Príncipes",
        "contenido": """
        <p>Para identificar ediciones príncipes mencionadas en FUENTES IX:</p>
        <ul>
            <li><strong>Series Diferentes y Escogidas</strong>: 48 tomos publicados entre 1652-1704</li>
            <li><strong>Partes de dramaturgos</strong>: Verificar en colecciones de British Library, Biblioteca Nacional de Madrid</li>
            <li><strong>Comedias sueltas</strong>: Buscar en catálogos de colecciones especializadas (Edward M. Wilson, Don W. Cruickshank)</li>
        </ul>
        """
    })
    
    recomendaciones.append({
        "titulo": "Búsqueda de Manuscritos",
        "contenido": """
        <p>FUENTES IX menciona múltiples manuscritos conservados en:</p>
        <ul>
            <li><strong>B.N.M.</strong> (Biblioteca Nacional de Madrid): Sección de Manuscritos</li>
            <li><strong>B.M.M.</strong> (Biblioteca Municipal de Madrid)</li>
            <li><strong>B.I.T.B.</strong> (Biblioteca del Instituto del Teatro de Barcelona)</li>
            <li><strong>B.L.</strong> (British Library): Sección de Manuscritos (catálogo de Gayangos)</li>
            <li><strong>Archivo de la Cofradía de la Novena</strong>: Mencionado frecuentemente para música teatral</li>
        </ul>
        """
    })
    
    recomendaciones.append({
        "titulo": "Volúmenes Relacionados de la Serie Fuentes",
        "contenido": """
        <p>FUENTES IX consolida datos de otros volúmenes de la serie:</p>
        <ul>
            <li><strong>Fuentes I</strong>: Representaciones palaciegas 1603-1699 (legajo 666 del Archivo del Palacio Real)</li>
            <li><strong>Fuentes IV, V, VI, XI</strong>: Corrales de comedias 1650-1719 (Archivo Municipal de Madrid)</li>
            <li><strong>Fuentes X</strong>: Incluye único dato relevante</li>
            <li><strong>Fuentes XIII</strong>: Arrendos de corrales 1587-1719</li>
        </ul>
        <p>Estos volúmenes pueden contener información adicional no consolidada en FUENTES IX.</p>
        """
    })
    
    recomendaciones.append({
        "titulo": "Investigadores y Estudios Mencionados",
        "contenido": """
        <p>FUENTES IX cita extensamente trabajos de investigadores que pueden tener información adicional:</p>
        <ul>
            <li><strong>Emilio Cotarelo y Mori</strong>: Trabajos fundamentales sobre teatro español</li>
            <li><strong>Edward M. Wilson</strong>: Estudios sobre Calderón y bibliografía</li>
            <li><strong>María Grazia Profeti</strong>: Estudios sobre Diferentes y Pérez de Montalbán</li>
            <li><strong>Ruth Lee Kennedy</strong>: Estudios sobre Moreto</li>
            <li><strong>Louise Kathrin Stein</strong>: Estudios sobre música teatral</li>
            <li><strong>Arnold G. Reichenberger</strong>: Estudios sobre Escogidas</li>
        </ul>
        """
    })
    
    return {
        "conclusiones": conclusiones,
        "recomendaciones": recomendaciones
    }

if __name__ == "__main__":
    print("🔄 Generando estadísticas...\n")
    
    stats_completitud = analizar_completitud()
    stats_fuentesix = analizar_fuentesix_especifico()
    conclusiones = generar_conclusiones(stats_completitud, stats_fuentesix)
    
    resultado = {
        "fecha_generacion": datetime.now().isoformat(),
        "estadisticas_completitud": stats_completitud,
        "analisis_fuentesix": stats_fuentesix,
        "conclusiones": conclusiones
    }
    
    archivo_salida = Path(__file__).parent / "estadisticas_datos.json"
    with open(archivo_salida, 'w', encoding='utf-8') as f:
        json.dump(resultado, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Estadísticas guardadas en {archivo_salida}")
    print(f"\n📊 Resumen:")
    print(f"   - Total obras analizadas: {stats_completitud['estadisticas_generales']['total_obras']}")
    print(f"   - Fuentes: {list(stats_completitud['estadisticas_generales']['por_fuente'].keys())}")
    print(f"   - Conclusiones generadas: {len(conclusiones['conclusiones'])}")
    print(f"   - Recomendaciones generadas: {len(conclusiones['recomendaciones'])}")
