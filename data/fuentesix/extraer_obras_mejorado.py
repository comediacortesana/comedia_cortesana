#!/usr/bin/env python3
"""
Script mejorado para extraer obras y representaciones de FUENTES IX
"""

import json
import re
from pathlib import Path
from datetime import datetime

DRIVE_BACKUP = Path(__file__).parent / "DRIVE_BACKUP"
OUTPUT_DIR = Path(__file__).parent

def parsear_entrada_obra(lineas, inicio_idx):
    """Parsea una entrada completa de obra"""
    if inicio_idx >= len(lineas):
        return None, inicio_idx
    
    # El título está en la línea actual
    titulo = lineas[inicio_idx].strip()
    
    # Leer líneas siguientes hasta encontrar próxima entrada o página
    idx = inicio_idx + 1
    contenido_obra = []
    
    while idx < len(lineas):
        linea = lineas[idx].strip()
        
        # Detener si encontramos nueva entrada (título que termina con , El/La/Los/Las)
        if (linea and 
            not linea.startswith('---') and
            not linea.startswith('COMEDIAS') and
            not linea.startswith('FUENTES') and
            linea[0].isupper() and
            (linea.endswith(', El') or linea.endswith(', La') or 
             linea.endswith(', Los') or linea.endswith(', Las')) and
            len(linea) < 150):
            break
        
        # Detener si encontramos nueva página
        if linea.startswith('--- PÁGINA'):
            idx += 1
            continue
        
        contenido_obra.append(linea)
        idx += 1
    
    texto_completo = ' '.join(contenido_obra)
    
    # Extraer representaciones
    representaciones = []
    patron_rep = re.compile(r'\((\d+)\)\s+([^\.]+?)\.\s+([^\.]+?)\.\s+([^\(]+?)\s*\(Fuentes\s+([IVX]+)\)')
    for match in patron_rep.finditer(texto_completo):
        rep = {
            "numero": match.group(1),
            "fecha": match.group(2).strip(),
            "compania": match.group(3).strip(),
            "lugar": match.group(4).strip(),
            "fuente": match.group(5)
        }
        representaciones.append(rep)
    
    # Extraer referencias cruzadas
    referencias = re.findall(r'Véase\s+(.+?)(?:\.|$)', texto_completo)
    
    # Extraer autor
    autor = None
    autor_match = re.search(r'(?:Comedia|Obra|Zarzuela|Auto)\s+(?:de|del|de la)\s+([A-ZÁÉÍÓÚÑ][^,\.\(]+)', texto_completo)
    if autor_match:
        autor = autor_match.group(1).strip()
    
    # Extraer títulos alternativos
    titulos_alt = []
    alt_matches = re.findall(r'(?:título alternativo|también se intitula|con el título de|título de)\s+([^\.]+)', texto_completo, re.IGNORECASE)
    titulos_alt.extend([a.strip() for a in alt_matches])
    
    obra = {
        "titulo": titulo,
        "autor": autor,
        "representaciones": representaciones,
        "referencias_cruzadas": referencias,
        "titulos_alternativos": titulos_alt,
        "texto_completo": texto_completo[:500]  # Limitar tamaño
    }
    
    return obra, idx

def extraer_todas_las_obras():
    """Extrae todas las obras de los archivos"""
    archivos = sorted(DRIVE_BACKUP.glob("FUENTES IX 1_part_00[3-9].txt"))
    
    todas_las_obras = []
    todas_las_representaciones = []
    lugares_set = set()
    companias_set = set()
    mecenas_set = set()
    
    for archivo in archivos:
        print(f"Procesando {archivo.name}...")
        with open(archivo, 'r', encoding='utf-8') as f:
            lineas = f.readlines()
        
        idx = 0
        while idx < len(lineas):
            linea = lineas[idx].strip()
            
            # Detectar inicio de entrada de obra
            if (linea and 
                not linea.startswith('---') and
                not linea.startswith('COMEDIAS') and
                not linea.startswith('FUENTES') and
                not linea.startswith('LISTA') and
                linea[0].isupper() and
                (linea.endswith(', El') or linea.endswith(', La') or 
                 linea.endswith(', Los') or linea.endswith(', Las')) and
                len(linea) < 150):
                
                obra, nuevo_idx = parsear_entrada_obra(lineas, idx)
                if obra:
                    obra["archivo"] = archivo.name
                    todas_las_obras.append(obra)
                    
                    # Agregar representaciones a lista global
                    for rep in obra["representaciones"]:
                        rep_con_obra = rep.copy()
                        rep_con_obra["obra"] = obra["titulo"]
                        todas_las_representaciones.append(rep_con_obra)
                        
                        # Extraer lugares y compañías
                        lugares_set.add(rep["lugar"])
                        companias_set.add(rep["compania"])
                    
                    # Buscar mecenas en el texto
                    texto = obra.get("texto_completo", "")
                    mecenas_matches = re.findall(r'(?:para celebrar|festejar|en celebridad|en honor).*?(?:de|del|de la)\s+([A-ZÁÉÍÓÚÑ][^\.]+)', texto, re.IGNORECASE)
                    for m in mecenas_matches:
                        mecenas_set.add(m.strip())
                
                idx = nuevo_idx
            else:
                idx += 1
    
    return {
        "obras": todas_las_obras,
        "representaciones": todas_las_representaciones,
        "lugares": sorted(list(lugares_set)),
        "companias": sorted(list(companias_set)),
        "mecenas": sorted(list(mecenas_set))
    }

if __name__ == "__main__":
    print("Extrayendo obras y representaciones...")
    resultado = extraer_todas_las_obras()
    
    print(f"✓ Encontradas {len(resultado['obras'])} obras")
    print(f"✓ Encontradas {len(resultado['representaciones'])} representaciones")
    print(f"✓ Encontrados {len(resultado['lugares'])} lugares únicos")
    print(f"✓ Encontradas {len(resultado['companias'])} compañías únicas")
    print(f"✓ Encontrados {len(resultado['mecenas'])} mecenas únicos")
    
    # Guardar resultado completo
    with open(OUTPUT_DIR / "contexto_extraido_por_tipo.json", 'w', encoding='utf-8') as f:
        json.dump({
            "fecha_extraccion": datetime.now().isoformat(),
            **resultado
        }, f, ensure_ascii=False, indent=2)
    
    # Guardar estadísticas para estructura_entradas_analisis
    estructura_mejorada = {
        "fecha_analisis": datetime.now().isoformat(),
        "estadisticas": {
            "total_obras": len(resultado['obras']),
            "total_representaciones": len(resultado['representaciones']),
            "total_lugares": len(resultado['lugares']),
            "total_companias": len(resultado['companias']),
            "total_mecenas": len(resultado['mecenas']),
            "lugares": resultado['lugares'][:50],
            "companias": resultado['companias'][:50]
        },
        "patrones_identificados": {
            "titulo": "Línea separada terminando con ', El/La/Los/Las'",
            "representacion": "(n) fecha. compañía. lugar (Fuentes X)",
            "referencia_cruzada": "Véase...",
            "informacion_bibliografica": "Párrafo continuo después de representaciones"
        },
        "ejemplos": resultado['obras'][:5] if resultado['obras'] else []
    }
    
    with open(OUTPUT_DIR / "estructura_entradas_analisis.json", 'w', encoding='utf-8') as f:
        json.dump(estructura_mejorada, f, ensure_ascii=False, indent=2, default=str)
    
    print("\n✅ Extracción completada!")
