#!/usr/bin/env python3
"""
Script final para extraer obras y representaciones de FUENTES IX
Usa un enfoque más simple y directo
"""

import json
import re
from pathlib import Path
from datetime import datetime

DRIVE_BACKUP = Path(__file__).parent / "DRIVE_BACKUP"
OUTPUT_DIR = Path(__file__).parent

def extraer_obras_simple():
    """Extrae obras usando búsqueda directa en el texto"""
    # Buscar archivos con patrón correcto (incluye "ALL_PAGES_texto_extraido")
    todos_archivos = sorted(DRIVE_BACKUP.glob("FUENTES IX 1_part_*.txt"))
    archivos = [a for a in todos_archivos if any(f'part_00{x}' in a.name for x in ['3', '4', '5', '6', '7', '8', '9'])]
    print(f"Archivos a procesar: {len(archivos)}")
    if archivos:
        print(f"  Primer archivo: {archivos[0].name}")
    
    todas_las_obras = []
    todas_las_representaciones = []
    lugares_set = set()
    companias_set = set()
    mecenas_set = set()
    
    # Patrón para títulos: línea que termina con ", El", ", La", etc.
    patron_titulo = re.compile(r'^([A-ZÁÉÍÓÚÑ][^\.\n]+(?:,\s*(?:El|La|Los|Las))?)$', re.MULTILINE)
    # Patrón para representaciones
    patron_rep = re.compile(r'\((\d+)\)\s+([^\.]+?)\.\s+([^\.]+?)\.\s+([^\(]+?)\s*\(Fuentes\s+([IVX]+)\)')
    
    for archivo in archivos:
        print(f"Procesando {archivo.name}...")
        with open(archivo, 'r', encoding='utf-8') as f:
            lineas = [l.rstrip('\n\r') for l in f.readlines()]
        
        obras_en_archivo = []
        titulos_encontrados = 0
        
        for i, linea in enumerate(lineas):
            linea_limpia = linea.strip()
            
            # Detectar título de obra - verificación más simple
            if (linea_limpia and 
                len(linea_limpia) > 3 and
                len(linea_limpia) < 150 and
                linea_limpia[0].isupper() and
                (linea_limpia.endswith(', El') or linea_limpia.endswith(', La') or 
                 linea_limpia.endswith(', Los') or linea_limpia.endswith(', Las')) and
                not linea_limpia.startswith('---') and
                not linea_limpia.startswith('COMEDIAS') and
                not linea_limpia.startswith('FUENTES') and
                not linea_limpia.startswith('LISTA') and
                not linea_limpia.startswith('(') and
                'PÁGINA' not in linea_limpia):
                
                titulo = linea_limpia
                
                # Leer contenido hasta próxima entrada o página
                contenido_obra = []
                j = i + 1
                while j < len(lineas):
                    siguiente = lineas[j].strip()
                    if (siguiente.startswith('--- PÁGINA') or
                        (siguiente and siguiente[0].isupper() and 
                         (siguiente.endswith(', El') or siguiente.endswith(', La') or
                          siguiente.endswith(', Los') or siguiente.endswith(', Las')) and
                         len(siguiente) < 150)):
                        break
                    if siguiente:
                        contenido_obra.append(siguiente)
                    j += 1
                
                texto_obra = ' '.join(contenido_obra)
                
                # Extraer representaciones
                representaciones = []
                for match in patron_rep.finditer(texto_obra):
                    rep = {
                        "numero": match.group(1),
                        "fecha": match.group(2).strip(),
                        "compania": match.group(3).strip(),
                        "lugar": match.group(4).strip(),
                        "fuente": match.group(5)
                    }
                    representaciones.append(rep)
                    todas_las_representaciones.append({
                        "obra": titulo,
                        **rep
                    })
                    lugares_set.add(rep["lugar"])
                    companias_set.add(rep["compania"])
                
                # Extraer autor
                autor = None
                autor_match = re.search(r'(?:Comedia|Obra|Zarzuela|Auto)\s+(?:de|del|de la)\s+([A-ZÁÉÍÓÚÑ][^,\.\(]+)', texto_obra)
                if autor_match:
                    autor = autor_match.group(1).strip()
                
                # Referencias cruzadas
                referencias = re.findall(r'Véase\s+(.+?)(?:\.|$)', texto_obra)
                
                # Títulos alternativos
                titulos_alt = re.findall(r'(?:título alternativo|también se intitula|con el título de)\s+([^\.]+)', texto_obra, re.IGNORECASE)
                
                # Mecenas
                mecenas_matches = re.findall(r'(?:para celebrar|festejar|en celebridad).*?(?:de|del|de la)\s+([A-ZÁÉÍÓÚÑ][^\.]+)', texto_obra, re.IGNORECASE)
                for m in mecenas_matches:
                    mecenas_set.add(m.strip())
                
                obra = {
                    "titulo": titulo,
                    "autor": autor,
                    "representaciones": representaciones,
                    "referencias_cruzadas": referencias,
                    "titulos_alternativos": titulos_alt,
                    "archivo": archivo.name,
                    "total_representaciones": len(representaciones)
                }
                
                obras_en_archivo.append(obra)
                todas_las_obras.append(obra)
                titulos_encontrados += 1
                
                if titulos_encontrados <= 3:
                    print(f"    → Encontrada: {titulo} ({len(representaciones)} reps)")
        
        print(f"  → {len(obras_en_archivo)} obras encontradas en total")
    
    return {
        "obras": todas_las_obras,
        "representaciones": todas_las_representaciones,
        "lugares": sorted(list(lugares_set)),
        "companias": sorted(list(companias_set)),
        "mecenas": sorted(list(mecenas_set))
    }

if __name__ == "__main__":
    print("Extrayendo obras y representaciones (método mejorado)...")
    resultado = extraer_obras_simple()
    
    print(f"\n✓ Encontradas {len(resultado['obras'])} obras")
    print(f"✓ Encontradas {len(resultado['representaciones'])} representaciones")
    print(f"✓ Encontrados {len(resultado['lugares'])} lugares únicos")
    print(f"✓ Encontradas {len(resultado['companias'])} compañías únicas")
    print(f"✓ Encontrados {len(resultado['mecenas'])} mecenas únicos")
    
    if resultado['obras']:
        print(f"\nPrimeras 3 obras:")
        for obra in resultado['obras'][:3]:
            print(f"  - {obra['titulo']}: {obra['total_representaciones']} representaciones")
    
    # Guardar resultado completo
    with open(OUTPUT_DIR / "contexto_extraido_por_tipo.json", 'w', encoding='utf-8') as f:
        json.dump({
            "fecha_extraccion": datetime.now().isoformat(),
            **resultado
        }, f, ensure_ascii=False, indent=2)
    
    # Actualizar estructura_entradas_analisis
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
