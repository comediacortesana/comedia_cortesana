#!/usr/bin/env python3
"""
Script para actualizar catálogos auxiliares con datos de FUENTES IX
"""

import json
import re
from pathlib import Path
from datetime import datetime
from collections import defaultdict

BASE_DIR = Path(__file__).parent.parent.parent
FUENTESIX_DIR = Path(__file__).parent
CONTEXTO_FUENTESIX = FUENTESIX_DIR / "contexto_extraido_por_tipo.json"
DATOS_OBRAS = BASE_DIR / "filtro_basico" / "datos_obras.json"

def extraer_anio_de_fecha(fecha_str):
    """Extrae año de una fecha"""
    if not fecha_str:
        return None
    match = re.search(r'(\d{4})', str(fecha_str))
    if match:
        año = int(match.group(1))
        if 1500 <= año <= 2000:
            return año
    return None

def normalizar_titulo(titulo):
    """Normaliza título"""
    if not titulo:
        return ""
    titulo_limpio = re.sub(r',\s*(El|La|Los|Las)$', '', titulo.strip())
    return ' '.join(titulo_limpio.split())

def actualizar_campo_auxiliar_fechas():
    """Actualiza campo_auxiliar_fechas.json con años de representaciones"""
    print("📅 Actualizando campo_auxiliar_fechas.json...")
    
    # Cargar existente
    archivo_existente = FUENTESIX_DIR / "campo_auxiliar_fechas.json"
    obras_existentes = {}
    
    if archivo_existente.exists():
        with open(archivo_existente, 'r', encoding='utf-8') as f:
            data_existente = json.load(f)
            obras_existentes = data_existente.get("obras", {})
        print(f"   ✓ {len(obras_existentes)} obras existentes cargadas")
    
    # Cargar datos de FUENTES IX
    with open(CONTEXTO_FUENTESIX, 'r', encoding='utf-8') as f:
        contexto = json.load(f)
    
    obras_fuentesix = contexto.get("obras", [])
    nuevas_obras = 0
    actualizadas = 0
    
    for obra in obras_fuentesix:
        titulo_original = obra.get("titulo", "")
        titulo_norm = normalizar_titulo(titulo_original)
        
        if not titulo_norm:
            continue
        
        # Buscar año en representaciones
        año_encontrado = None
        primera_rep = None
        
        for rep in obra.get("representaciones", []):
            fecha = rep.get("fecha", "")
            año = extraer_anio_de_fecha(fecha)
            if año:
                año_encontrado = año
                primera_rep = rep
                break
        
        if año_encontrado:
            if titulo_norm not in obras_existentes:
                obras_existentes[titulo_norm] = {
                    "anio_auxiliar": año_encontrado,
                    "fuente": "Fuentes IX",
                    "pagina_pdf": None,
                    "contexto": f"Primera representación: {primera_rep.get('fecha', '')} - {primera_rep.get('lugar', '')}" if primera_rep else "",
                    "menciones": len(obra.get("representaciones", []))
                }
                nuevas_obras += 1
            else:
                # Actualizar si el año es más temprano
                año_existente = obras_existentes[titulo_norm].get("anio_auxiliar")
                if not año_existente or año_encontrado < año_existente:
                    obras_existentes[titulo_norm]["anio_auxiliar"] = año_encontrado
                    obras_existentes[titulo_norm]["menciones"] = obras_existentes[titulo_norm].get("menciones", 0) + len(obra.get("representaciones", []))
                    actualizadas += 1
    
    # Guardar
    resultado = {
        "metadata": {
            "fuente": "Fuentes IX",
            "total_obras": len(obras_existentes),
            "fecha_actualizacion": datetime.now().isoformat(),
            "obras_nuevas": nuevas_obras,
            "obras_actualizadas": actualizadas
        },
        "obras": obras_existentes
    }
    
    with open(archivo_existente, 'w', encoding='utf-8') as f:
        json.dump(resultado, f, ensure_ascii=False, indent=2)
    
    print(f"   ✅ Actualizado: {len(obras_existentes)} obras ({nuevas_obras} nuevas, {actualizadas} actualizadas)")

def actualizar_lugares_mecenas():
    """Actualiza analisis_lugares_mecenas.json con nuevos lugares"""
    print("📍 Actualizando analisis_lugares_mecenas.json...")
    
    # Cargar existente
    archivo_existente = FUENTESIX_DIR / "analisis_lugares_mecenas.json"
    categorias_existentes = {}
    
    if archivo_existente.exists():
        with open(archivo_existente, 'r', encoding='utf-8') as f:
            data_existente = json.load(f)
            categorias_existentes = data_existente.get("categorias", {})
        print(f"   ✓ {len(categorias_existentes)} categorías existentes cargadas")
    
    # Cargar datos de FUENTES IX
    with open(CONTEXTO_FUENTESIX, 'r', encoding='utf-8') as f:
        contexto = json.load(f)
    
    lugares_unicos = set(contexto.get("lugares", []))
    lugares_por_tipo = defaultdict(list)
    
    # Clasificar lugares
    for lugar in lugares_unicos:
        lugar_limpio = lugar.strip()
        if not lugar_limpio:
            continue
        
        tipo = "otro"
        if "Palacio" in lugar_limpio or "Buen Retiro" in lugar_limpio:
            tipo = "palacio"
        elif "Corral" in lugar_limpio:
            tipo = "corral"
        elif "Coliseo" in lugar_limpio:
            tipo = "teatro"
        elif "Cuarto" in lugar_limpio:
            tipo = "palacio"
        elif "Salón" in lugar_limpio or "Saloncete" in lugar_limpio or "Saloncillo" in lugar_limpio:
            tipo = "palacio"
        
        lugares_por_tipo[tipo].append({
            "id": f"fuentesix_{lugar_limpio.lower().replace(' ', '_')}",
            "nombre": lugar_limpio,
            "ciudad": "Madrid" if any(x in lugar_limpio for x in ["Palacio", "Buen Retiro", "Corral", "Madrid"]) else "",
            "menciones": 1  # Simplificado, se podría contar mejor
        })
    
    # Actualizar categorías existentes o crear nuevas
    if "palacios" not in categorias_existentes:
        categorias_existentes["palacios"] = {
            "nombre": "Palacios Reales",
            "descripcion": "Representaciones en palacios reales",
            "tipo": "palacio",
            "lugares": []
        }
    
    if "corrales" not in categorias_existentes:
        categorias_existentes["corrales"] = {
            "nombre": "Corrales de Comedias",
            "descripcion": "Corrales de comedias de Madrid",
            "tipo": "corral",
            "lugares": []
        }
    
    # Añadir lugares nuevos (evitar duplicados)
    lugares_existentes_palacios = {l["nombre"] for l in categorias_existentes["palacios"].get("lugares", [])}
    lugares_existentes_corrales = {l["nombre"] for l in categorias_existentes["corrales"].get("lugares", [])}
    
    for lugar in lugares_por_tipo.get("palacio", []):
        if lugar["nombre"] not in lugares_existentes_palacios:
            categorias_existentes["palacios"]["lugares"].append(lugar)
    
    for lugar in lugares_por_tipo.get("corral", []):
        if lugar["nombre"] not in lugares_existentes_corrales:
            categorias_existentes["corrales"]["lugares"].append(lugar)
    
    # Guardar
    resultado = {
        "metadata": {
            "fecha_generacion": datetime.now().isoformat(),
            "fuente": "Fuentes IX",
            "total_items": sum(len(cat.get("lugares", [])) for cat in categorias_existentes.values()),
            "categorias_count": len(categorias_existentes)
        },
        "categorias": categorias_existentes
    }
    
    with open(archivo_existente, 'w', encoding='utf-8') as f:
        json.dump(resultado, f, ensure_ascii=False, indent=2)
    
    print(f"   ✅ Actualizado: {len(categorias_existentes)} categorías")

if __name__ == "__main__":
    print("🔄 Actualizando catálogos auxiliares...\n")
    
    try:
        actualizar_campo_auxiliar_fechas()
        print()
        actualizar_lugares_mecenas()
        print("\n✅ Actualización de catálogos completada!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
