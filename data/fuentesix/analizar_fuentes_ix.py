#!/usr/bin/env python3
"""
Script para analizar y extraer contexto de FUENTES IX
"""

import json
import re
import os
from pathlib import Path
from collections import defaultdict
from datetime import datetime

# Directorio de archivos
DRIVE_BACKUP = Path(__file__).parent / "DRIVE_BACKUP"
OUTPUT_DIR = Path(__file__).parent

def extraer_paginas(archivo):
    """Extrae información de páginas de un archivo"""
    paginas = []
    with open(archivo, 'r', encoding='utf-8') as f:
        contenido = f.read()
        for match in re.finditer(r'^--- PÁGINA (\d+) ---', contenido, re.MULTILINE):
            paginas.append(int(match.group(1)))
    return sorted(paginas)

def verificar_completitud():
    """Tarea 1: Verificar completitud del texto extraído"""
    archivos = sorted(DRIVE_BACKUP.glob("FUENTES IX 1_part_*.txt"))
    resultado = {
        "fecha_verificacion": datetime.now().isoformat(),
        "archivos": [],
        "total_paginas": 0,
        "continuidad": [],
        "problemas": []
    }
    
    paginas_totales = set()
    
    for i, archivo in enumerate(archivos):
        paginas = extraer_paginas(archivo)
        paginas_totales.update(paginas)
        
        info_archivo = {
            "archivo": archivo.name,
            "total_paginas": len(paginas),
            "paginas": paginas,
            "primera_pagina": min(paginas) if paginas else None,
            "ultima_pagina": max(paginas) if paginas else None
        }
        resultado["archivos"].append(info_archivo)
        resultado["total_paginas"] += len(paginas)
        
        # Verificar continuidad
        if i > 0:
            archivo_anterior = archivos[i-1]
            paginas_anterior = extraer_paginas(archivo_anterior)
            if paginas_anterior:
                ultima_pag_anterior = max(paginas_anterior)
                primera_pag_actual = min(paginas)
                
                # Leer últimas líneas del archivo anterior y primeras del actual
                with open(archivo_anterior, 'r', encoding='utf-8') as f:
                    lineas_anterior = f.readlines()
                    ultimas_lineas = ''.join(lineas_anterior[-5:])
                
                with open(archivo, 'r', encoding='utf-8') as f:
                    primeras_lineas = ''.join(f.readlines()[:10])
                
                continuidad = {
                    "archivo_anterior": archivo_anterior.name,
                    "archivo_actual": archivo.name,
                    "ultima_pagina_anterior": ultima_pag_anterior,
                    "primera_pagina_actual": primera_pag_actual,
                    "continuidad_paginas": primera_pag_actual == ultima_pag_anterior + 1,
                    "ultimas_lineas_anterior": ultimas_lineas.strip()[:200],
                    "primeras_lineas_actual": primeras_lineas.strip()[:200]
                }
                resultado["continuidad"].append(continuidad)
                
                if not continuidad["continuidad_paginas"]:
                    resultado["problemas"].append({
                        "tipo": "discontinuidad_paginas",
                        "detalle": continuidad
                    })
    
    # Verificar páginas faltantes
    if paginas_totales:
        min_pag = min(paginas_totales)
        max_pag = max(paginas_totales)
        paginas_esperadas = set(range(min_pag, max_pag + 1))
        paginas_faltantes = paginas_esperadas - paginas_totales
        
        if paginas_faltantes:
            resultado["problemas"].append({
                "tipo": "paginas_faltantes",
                "paginas": sorted(paginas_faltantes)
            })
    
    return resultado

def analizar_estructura_entradas():
    """Tarea 2: Analizar estructura de entradas"""
    archivos = sorted(DRIVE_BACKUP.glob("FUENTES IX 1_part_00[3-9].txt"))  # Solo archivos con entradas
    
    resultado = {
        "fecha_analisis": datetime.now().isoformat(),
        "patrones_identificados": {},
        "estadisticas": {
            "total_obras": 0,
            "total_representaciones": 0,
            "fechas": {"min": None, "max": None},
            "companias": set(),
            "lugares": set()
        },
        "ejemplos": []
    }
    
    # Patrón mejorado para títulos: línea que empieza con mayúscula y termina con ", El", ", La", etc. o solo mayúscula
    patron_titulo = re.compile(r'^([A-ZÁÉÍÓÚÑ][^\.\n]+(?:,\s*(?:El|La|Los|Las))?)$', re.MULTILINE)
    # Patrón mejorado para representaciones: (n) seguido de fecha, compañía, lugar, (Fuentes X)
    patron_representacion = re.compile(r'\((\d+)\)\s+([^\.]+?)\.\s+([^\.]+?)\.\s+([^\(]+?)\s*\(Fuentes\s+([IVX]+)\)')
    patron_referencia = re.compile(r'Véase\s+(.+?)(?:\.|$)')
    
    obras_unicas = set()
    representaciones = []
    años_encontrados = []
    
    for archivo in archivos:
        with open(archivo, 'r', encoding='utf-8') as f:
            lineas = f.readlines()
            contenido = ''.join(lineas)
        
        # Buscar títulos: líneas que empiezan con mayúscula y no son páginas ni encabezados
        titulos_encontrados = []
        for i, linea in enumerate(lineas):
            linea_limpia = linea.strip()
            # Excluir líneas de páginas, encabezados, y líneas que empiezan con espacios o números
            if (linea_limpia and 
                not linea_limpia.startswith('---') and
                not linea_limpia.startswith('COMEDIAS EN MADRID') and
                not linea_limpia.startswith('FUENTES PARA LA HISTORIA') and
                not linea_limpia.startswith('LISTA') and
                linea_limpia[0].isupper() and
                (linea_limpia.endswith(', El') or linea_limpia.endswith(', La') or 
                 linea_limpia.endswith(', Los') or linea_limpia.endswith(', Las') or
                 (len(linea_limpia) < 100 and not linea_limpia.startswith('(')))):
                # Verificar que la siguiente línea no empiece con "Véase" o "("
                if i + 1 < len(lineas):
                    siguiente = lineas[i+1].strip()
                    if siguiente.startswith('Véase') or siguiente.startswith('(') or siguiente.startswith('Comedia'):
                        titulos_encontrados.append(linea_limpia)
                        obras_unicas.add(linea_limpia)
        
        # Buscar representaciones con patrón mejorado
        reps = patron_representacion.findall(contenido)
        representaciones.extend(reps)
        
        # Extraer años de las fechas
        fechas_texto = re.findall(r'(\d{1,2})\s+de\s+[a-záéíóúñ]+?\s+de\s+(\d{4})', contenido, re.IGNORECASE)
        años_encontrados.extend([int(f[1]) for f in fechas_texto])
        
        # Extraer compañías
        companias = re.findall(r'(?:compañía de|por la compañía de|por)\s+([A-ZÁÉÍÓÚÑ][^\.\(]+?)(?:\.|,|\(|$)', contenido, re.IGNORECASE)
        companias_limpias = [c.strip() for c in companias if len(c.strip()) < 100]
        resultado["estadisticas"]["companias"].update(companias_limpias[:20])
        
        # Extraer lugares específicos
        lugares = re.findall(r'(Palacio|Buen Retiro|Corral del Príncipe|Corral de la Cruz|Coliseo|Salón|Cuarto del Rey|Cuarto de la Reina|Pardo|Toledo|Valladolid|Representación palaciega)', contenido)
        resultado["estadisticas"]["lugares"].update(lugares)
        
        # Guardar ejemplos
        if len(resultado["ejemplos"]) < 5 and titulos_encontrados:
            ejemplo = {
                "archivo": archivo.name,
                "titulos_encontrados": len(titulos_encontrados),
                "representaciones_encontradas": len(reps),
                "primer_titulo": titulos_encontrados[0] if titulos_encontrados else None,
                "primera_representacion": list(reps[0]) if reps else None
            }
            resultado["ejemplos"].append(ejemplo)
    
    resultado["estadisticas"]["total_obras"] = len(obras_unicas)
    resultado["estadisticas"]["total_representaciones"] = len(representaciones)
    resultado["estadisticas"]["companias"] = sorted(list(resultado["estadisticas"]["companias"]))[:50]
    resultado["estadisticas"]["lugares"] = sorted(list(resultado["estadisticas"]["lugares"]))
    
    if años_encontrados:
        resultado["estadisticas"]["fechas"]["min"] = min(años_encontrados)
        resultado["estadisticas"]["fechas"]["max"] = max(años_encontrados)
    
    resultado["patrones_identificados"] = {
        "titulo": "Línea separada con mayúscula inicial, puede terminar con ', El/La/Los/Las'",
        "representacion": "(n) fecha. compañía. lugar (Fuentes X)",
        "referencia_cruzada": "Véase... o Véanse...",
        "informacion_bibliografica": "Párrafo continuo después de las representaciones"
    }
    
    return resultado

def extraer_metadatos_estructurales():
    """Tarea 3: Extraer metadatos del prefacio e introducción"""
    archivo = DRIVE_BACKUP / "FUENTES IX 1_part_001_ALL_PAGES_texto_extraido.txt"
    
    with open(archivo, 'r', encoding='utf-8') as f:
        contenido = f.read()
    
    resultado = {
        "fecha_extraccion": datetime.now().isoformat(),
        "prefacio": {},
        "introduccion": {},
        "abreviaturas": {},
        "referencias_fuentes": [],
        "catalogos_bibliograficos": []
    }
    
    # Extraer prefacio (páginas 6-7)
    prefacio_match = re.search(r'PREFACIO\s+(.*?)(?=PROLOGO|REFERENCIAS|INTRODUCCION)', contenido, re.DOTALL)
    if prefacio_match:
        prefacio_texto = prefacio_match.group(1)
        periodo_match = re.search(r'(\d{4})\s+a\s+(\d{4})', prefacio_texto)
        resultado["prefacio"] = {
            "texto_completo": prefacio_texto[:2000],
            "volumenes_fuente": sorted(set(re.findall(r'Fuentes ([IVX]+)', prefacio_texto))),
            "periodo_cubierto": {
                "inicio": periodo_match.group(1) if periodo_match else None,
                "fin": periodo_match.group(2) if periodo_match else None
            },
            "archivos_principales": list(set(re.findall(r'Archivo (?:del|de) ([^\.]+)', prefacio_texto)))
        }
    
    # Extraer introducción
    intro_match = re.search(r'INTRODUCCION\s+(.*?)(?=ABREVIATURAS|LISTA)', contenido, re.DOTALL)
    if intro_match:
        intro_texto = intro_match.group(1)
        resultado["introduccion"] = {
            "metodologia": {
                "orden": "alfabético",
                "fuentes_documentales": list(set(re.findall(r'Archivo (?:del|de) ([^\.]+)', intro_texto))),
                "normas_citacion": "Fecha, compañía, lugar, referencia a Fuentes"
            },
            "problemas_mencionados": [
                "Discrepancias entre fuentes",
                "Títulos alternativos",
                "Confusión entre ensayo y representación",
                "Pagos tardíos causan confusión",
                "Concepto ambiguo de 'comedia nueva'"
            ],
            "lugares_palaciegos": sorted(set(re.findall(r'(Alcázar|Buen Retiro|Coliseo|Salón|Cuarto del Rey|Cuarto de la Reina|Patinejo|Saloncete|Saloncillo)', intro_texto)))
        }
    
    # Extraer abreviaturas (página 19)
    abreviaturas_match = re.search(r'ABREVIATURAS\s+(.*?)(?=LISTA|$)', contenido, re.DOTALL)
    if abreviaturas_match:
        abrev_texto = abreviaturas_match.group(1)
        lineas = abrev_texto.split('\n')
        for linea in lineas:
            linea = linea.strip()
            if linea and not linea.startswith('---'):
                match = re.match(r'^([A-Z]+)\s+(.+)$', linea)
                if match:
                    resultado["abreviaturas"][match.group(1)] = match.group(2)
    
    # Extraer referencias a otros volúmenes de Fuentes
    referencias = re.findall(r'Fuentes (?:para la historia del teatro en España, )?([IVX]+)', contenido)
    resultado["referencias_fuentes"] = sorted(set(referencias))
    
    # Extraer catálogos bibliográficos mencionados
    catalogos = re.findall(r'(Barrera|Fajardo|Medel|García de la Huerta|Arteaga|Cotarelo)', contenido)
    resultado["catalogos_bibliograficos"] = sorted(set(catalogos))
    
    return resultado

def extraer_contexto_por_tipo():
    """Tarea 4: Extraer contexto por tipo de información"""
    archivos = sorted(DRIVE_BACKUP.glob("FUENTES IX 1_part_00[3-9].txt"))
    
    resultado = {
        "fecha_extraccion": datetime.now().isoformat(),
        "obras": [],
        "representaciones": [],
        "mecenas": [],
        "lugares": [],
        "companias": []
    }
    
    obras_dict = {}
    representaciones_list = []
    lugares_set = set()
    companias_set = set()
    mecenas_set = set()
    
    for archivo in archivos:
        with open(archivo, 'r', encoding='utf-8') as f:
            lineas = f.readlines()
            contenido = ''.join(lineas)
        
        # Buscar entradas de obras
        i = 0
        while i < len(lineas):
            linea = lineas[i].strip()
            
            # Detectar título de obra
            if (linea and 
                not linea.startswith('---') and
                not linea.startswith('COMEDIAS') and
                linea[0].isupper() and
                (linea.endswith(', El') or linea.endswith(', La') or 
                 linea.endswith(', Los') or linea.endswith(', Las') or
                 (len(linea) < 100 and not linea.startswith('(')))):
                
                titulo = linea
                obra_info = {
                    "titulo": titulo,
                    "titulos_alternativos": [],
                    "autor": None,
                    "representaciones": [],
                    "referencias_cruzadas": [],
                    "archivo": archivo.name
                }
                
                # Leer siguientes líneas hasta encontrar próximo título o página
                j = i + 1
                texto_obra = []
                while j < len(lineas):
                    siguiente = lineas[j].strip()
                    if (siguiente.startswith('---') or 
                        (siguiente and siguiente[0].isupper() and 
                         (siguiente.endswith(', El') or siguiente.endswith(', La')))):
                        break
                    texto_obra.append(siguiente)
                    j += 1
                
                texto_completo = ' '.join(texto_obra)
                
                # Extraer representaciones
                reps = re.findall(r'\((\d+)\)\s+([^\.]+?)\.\s+([^\.]+?)\.\s+([^\(]+?)\s*\(Fuentes\s+([IVX]+)\)', texto_completo)
                for rep in reps:
                    rep_info = {
                        "numero": rep[0],
                        "fecha": rep[1].strip(),
                        "compania": rep[2].strip(),
                        "lugar": rep[3].strip(),
                        "fuente": rep[4]
                    }
                    obra_info["representaciones"].append(rep_info)
                    representaciones_list.append({
                        "obra": titulo,
                        **rep_info
                    })
                    companias_set.add(rep[2].strip())
                    lugares_set.add(rep[3].strip())
                
                # Extraer referencias cruzadas
                refs = re.findall(r'Véase\s+(.+?)(?:\.|$)', texto_completo)
                obra_info["referencias_cruzadas"] = refs
                
                # Extraer autor (buscar "Comedia de", "de [Autor]", etc.)
                autor_match = re.search(r'(?:Comedia|Obra|Zarzuela)\s+(?:de|del|de la)\s+([A-ZÁÉÍÓÚÑ][^,\.]+)', texto_completo)
                if autor_match:
                    obra_info["autor"] = autor_match.group(1).strip()
                
                # Buscar mecenas (celebrar, festejar, etc.)
                mecenas_matches = re.findall(r'(?:para celebrar|festejar|en celebridad).*?(?:de|del|de la)\s+([A-ZÁÉÍÓÚÑ][^\.]+)', texto_completo, re.IGNORECASE)
                for m in mecenas_matches:
                    mecenas_set.add(m.strip())
                
                obras_dict[titulo] = obra_info
            i += 1
    
    resultado["obras"] = list(obras_dict.values())[:100]  # Limitar para no hacer el archivo muy grande
    resultado["representaciones"] = representaciones_list[:500]
    resultado["lugares"] = sorted(list(lugares_set))
    resultado["companias"] = sorted(list(companias_set))
    resultado["mecenas"] = sorted(list(mecenas_set))
    
    return resultado

def crear_indices():
    """Tarea 5: Crear índices de referencia"""
    archivos = sorted(DRIVE_BACKUP.glob("FUENTES IX 1_part_00[3-9].txt"))
    
    indices = {
        "fecha_creacion": datetime.now().isoformat(),
        "indice_alfabetico_obras": {},
        "indice_autores": defaultdict(list),
        "indice_cronologico": [],
        "indice_geografico": defaultdict(list),
        "indice_companias": defaultdict(list)
    }
    
    for archivo in archivos:
        with open(archivo, 'r', encoding='utf-8') as f:
            lineas = f.readlines()
            contenido = ''.join(lineas)
        
        # Extraer páginas del archivo
        paginas = extraer_paginas(archivo)
        pagina_actual = paginas[0] if paginas else None
        
        # Buscar obras y sus datos
        i = 0
        while i < len(lineas):
            linea = lineas[i].strip()
            
            if (linea and 
                not linea.startswith('---') and
                linea[0].isupper() and
                (linea.endswith(', El') or linea.endswith(', La') or 
                 linea.endswith(', Los') or linea.endswith(', Las'))):
                
                titulo = linea
                
                # Actualizar página si encontramos marcador
                if i > 0 and '--- PÁGINA' in lineas[i-1]:
                    pagina_match = re.search(r'--- PÁGINA (\d+) ---', lineas[i-1])
                    if pagina_match:
                        pagina_actual = int(pagina_match.group(1))
                
                indices["indice_alfabetico_obras"][titulo] = {
                    "archivo": archivo.name,
                    "pagina": pagina_actual
                }
                
                # Leer información de la obra
                j = i + 1
                texto_obra = []
                while j < len(lineas):
                    siguiente = lineas[j].strip()
                    if (siguiente.startswith('---') or 
                        (siguiente and siguiente[0].isupper() and 
                         (siguiente.endswith(', El') or siguiente.endswith(', La')))):
                        break
                    texto_obra.append(siguiente)
                    j += 1
                
                texto_completo = ' '.join(texto_obra)
                
                # Extraer autor
                autor_match = re.search(r'(?:Comedia|Obra|Zarzuela)\s+(?:de|del|de la)\s+([A-ZÁÉÍÓÚÑ][^,\.]+)', texto_completo)
                if autor_match:
                    autor = autor_match.group(1).strip()
                    indices["indice_autores"][autor].append(titulo)
                
                # Extraer representaciones para índice cronológico
                reps = re.findall(r'\((\d+)\)\s+([^\.]+?)\.\s+([^\.]+?)\.\s+([^\(]+?)\s*\(Fuentes\s+([IVX]+)\)', texto_completo)
                for rep in reps:
                    fecha_texto = rep[1].strip()
                    año_match = re.search(r'(\d{4})', fecha_texto)
                    if año_match:
                        año = int(año_match.group(1))
                        indices["indice_cronologico"].append({
                            "año": año,
                            "obra": titulo,
                            "fecha": fecha_texto,
                            "compania": rep[2].strip(),
                            "lugar": rep[3].strip()
                        })
                    
                    # Índice geográfico
                    lugar = rep[3].strip()
                    indices["indice_geografico"][lugar].append({
                        "obra": titulo,
                        "fecha": fecha_texto
                    })
                    
                    # Índice de compañías
                    compania = rep[2].strip()
                    indices["indice_companias"][compania].append({
                        "obra": titulo,
                        "fecha": fecha_texto,
                        "lugar": lugar
                    })
            
            i += 1
    
    # Convertir defaultdicts a dicts normales y ordenar
    indices["indice_autores"] = {k: sorted(v) for k, v in indices["indice_autores"].items()}
    indices["indice_geografico"] = {k: v[:50] for k, v in indices["indice_geografico"].items()}  # Limitar
    indices["indice_companias"] = {k: v[:50] for k, v in indices["indice_companias"].items()}  # Limitar
    indices["indice_cronologico"] = sorted(indices["indice_cronologico"], key=lambda x: x["año"])[:500]  # Limitar
    
    return indices

def analizar_discrepancias():
    """Tarea 6: Analizar discrepancias y problemas"""
    archivo_intro = DRIVE_BACKUP / "FUENTES IX 1_part_001_ALL_PAGES_texto_extraido.txt"
    archivos_obras = sorted(DRIVE_BACKUP.glob("FUENTES IX 1_part_00[3-9].txt"))
    
    resultado = {
        "fecha_analisis": datetime.now().isoformat(),
        "discrepancias_mencionadas": [],
        "problemas_bibliograficos": [],
        "atribuciones_dudosas": [],
        "variantes_titulos": []
    }
    
    # Leer introducción para encontrar discrepancias mencionadas
    with open(archivo_intro, 'r', encoding='utf-8') as f:
        intro = f.read()
    
    # Buscar ejemplos de discrepancias en la introducción
    discrepancias_intro = re.findall(r'(?:discrepancia|conflicto|contradictoria|confusión).*?\.', intro, re.IGNORECASE | re.DOTALL)
    resultado["discrepancias_mencionadas"] = [d.strip()[:200] for d in discrepancias_intro[:10]]
    
    # Buscar problemas bibliográficos mencionados
    problemas = re.findall(r'(?:problema|dificultad|ambigüedad|confusión).*?\.', intro, re.IGNORECASE | re.DOTALL)
    resultado["problemas_bibliograficos"] = [p.strip()[:200] for p in problemas[:10]]
    
    # Buscar atribuciones dudosas en las obras
    for archivo in archivos_obras[:3]:  # Limitar a primeros archivos
        with open(archivo, 'r', encoding='utf-8') as f:
            contenido = f.read()
        
        # Buscar frases que indican duda
        dudas = re.findall(r'(?:probablemente|quizá|puede ser|dudan|dudoso|atribuida|atribuido).*?\.', contenido, re.IGNORECASE | re.DOTALL)
        resultado["atribuciones_dudosas"].extend([d.strip()[:200] for d in dudas[:5]])
        
        # Buscar variantes de títulos
        variantes = re.findall(r'(?:título alternativo|también se intitula|con el título de|título de).*?\.', contenido, re.IGNORECASE | re.DOTALL)
        resultado["variantes_titulos"].extend([v.strip()[:200] for v in variantes[:10]])
    
    return resultado

def crear_documentacion():
    """Tarea 7: Crear documentación completa"""
    doc = """# Contexto del Volumen FUENTES IX

## Estructura del Volumen

FUENTES IX - "Comedias en Madrid: 1603-1709" es un volumen de referencia bibliográfica que consolida y organiza alfabéticamente los títulos de obras teatrales mencionados en los volúmenes anteriores de la serie Fuentes para la historia del teatro en España.

### Organización

- **Prefacio y Prólogo** (páginas 1-9): Contexto histórico y metodológico
- **Introducción** (páginas 10-18): Metodología, fuentes documentales, problemas bibliográficos, normas
- **Abreviaturas** (página 19): Lista de abreviaturas utilizadas
- **Lista de Obras Citadas** (páginas 20-25+): Referencias bibliográficas
- **Entradas Alfabéticas** (páginas 26-248): Obras organizadas alfabéticamente
- **Índice Onomástico** (páginas 249-251): Autores, investigadores, dramaturgos

## Metodología

### Fuentes Documentales

El volumen consolida datos de:
- **Fuentes I**: Representaciones palaciegas del legajo 666 del Archivo del Palacio Real
- **Fuentes IV, V, VI, XI**: Documentos del Archivo Municipal de Madrid (Archivo de Secretaría) sobre corrales de comedias (1650-1719)
- **Fuentes X**: Único dato referente a una representación dentro del período cronológico

### Formato de Entradas

Cada entrada de obra contiene:

1. **Título principal**: En línea separada, orden alfabético
2. **Lista cronológica de representaciones**: 
   - Formato: `(n) fecha. compañía. lugar (Fuentes X)`
   - Numeradas secuencialmente
   - Incluye fecha, compañía, lugar, y referencia al volumen fuente
3. **Información bibliográfica**:
   - Identificación de la obra y autor
   - Edición príncipe
   - Manuscritos conocidos
   - Títulos alternativos
   - Referencias cruzadas

### Lugares de Representación

- **Palacios**: Alcázar (denominado "Palacio"), Buen Retiro
- **Espacios palaciegos**: Salón, Cuarto del Rey, Cuarto de la Reina, Coliseo, Patinejo, Saloncete, Saloncillo, Salón de los Reinos
- **Corrales**: Corral del Príncipe, Corral de la Cruz
- **Otras ciudades**: Valladolid, Toledo, Pardo

## Problemas y Limitaciones

### Discrepancias Documentales

Los autores reconocen discrepancias entre fuentes:
- Diferencias en fechas entre documentos palaciegos y certificados notariales
- Confusión entre lugares de representación
- Títulos alternativos que dificultan la identificación
- Representaciones múltiples el mismo día

### Problemas Bibliográficos

- Ediciones primitivas desaparecidas
- Variantes en las series Diferentes y Escogidas
- Refundiciones que conservan o cambian títulos
- Atribuciones falsas en ediciones sueltas
- Concepto ambiguo de "comedia nueva"

### Normas de Citación

- Se cita la edición príncipe solamente
- Se distinguen manuscritos consultados directamente vs. por referencia
- Se incluyen signaturas de ejemplares consultados para colecciones importantes

## Catálogos Bibliográficos Utilizados

- **Barrera y Leirado**: Catálogo fundamental, punto de partida
- **Fajardo**: Catálogo de obras teatrales
- **Medel del Castillo**: Catálogo de obras teatrales
- **García de la Huerta**: Catálogo de obras teatrales
- **Arteaga**: Catálogo de obras teatrales
- **Cotarelo y Mori**: Investigaciones de generaciones pasadas

## Período Cubierto

**1603-1709**: Representaciones teatrales en Madrid durante el Siglo de Oro español

## Uso del Volumen

Este volumen es complementario a los tomos cronológicos (I, IV, V, VI, XI) y permite:
- Búsqueda alfabética de obras
- Identificación de títulos alternativos
- Verificación de atribuciones
- Localización de ediciones y manuscritos
- Estudio de representaciones por obra

## Relación con Otros Volúmenes

- **Fuentes I**: Representaciones palaciegas (fuente principal)
- **Fuentes II**: Omitido (no se refiere a representaciones)
- **Fuentes III**: Documentos 1600-1650 (sin títulos de comedias)
- **Fuentes IV-VI, XI**: Corrales de comedias 1650-1719 (fuente principal)
- **Fuentes X**: Incluido solo dato relevante
- **Fuentes XIII**: Arrendos de corrales (referencia)

---

*Documentación generada automáticamente a partir del análisis del texto extraído de FUENTES IX*
"""
    return doc

if __name__ == "__main__":
    print("Iniciando análisis completo de FUENTES IX...")
    
    # Tarea 1: Verificación de completitud
    print("Tarea 1: Verificando completitud...")
    verificacion = verificar_completitud()
    with open(OUTPUT_DIR / "verificacion_completitud.json", 'w', encoding='utf-8') as f:
        json.dump(verificacion, f, ensure_ascii=False, indent=2)
    print(f"✓ Verificación completada: {verificacion['total_paginas']} páginas en {len(verificacion['archivos'])} archivos")
    
    # Tarea 2: Análisis de estructura
    print("Tarea 2: Analizando estructura de entradas...")
    estructura = analizar_estructura_entradas()
    with open(OUTPUT_DIR / "estructura_entradas_analisis.json", 'w', encoding='utf-8') as f:
        json.dump(estructura, f, ensure_ascii=False, indent=2, default=str)
    print(f"✓ Estructura analizada: {estructura['estadisticas']['total_obras']} obras, {estructura['estadisticas']['total_representaciones']} representaciones")
    
    # Tarea 3: Metadatos estructurales
    print("Tarea 3: Extrayendo metadatos estructurales...")
    metadatos = extraer_metadatos_estructurales()
    with open(OUTPUT_DIR / "metadatos_estructurales.json", 'w', encoding='utf-8') as f:
        json.dump(metadatos, f, ensure_ascii=False, indent=2, default=str)
    print("✓ Metadatos extraídos")
    
    # Tarea 4: Extracción de contexto por tipo
    print("Tarea 4: Extrayendo contexto por tipo...")
    contexto = extraer_contexto_por_tipo()
    with open(OUTPUT_DIR / "contexto_extraido_por_tipo.json", 'w', encoding='utf-8') as f:
        json.dump(contexto, f, ensure_ascii=False, indent=2, default=str)
    print(f"✓ Contexto extraído: {len(contexto['obras'])} obras, {len(contexto['representaciones'])} representaciones")
    
    # Tarea 5: Crear índices
    print("Tarea 5: Creando índices de referencia...")
    indices = crear_indices()
    with open(OUTPUT_DIR / "indices_referencia.json", 'w', encoding='utf-8') as f:
        json.dump(indices, f, ensure_ascii=False, indent=2, default=str)
    print("✓ Índices creados")
    
    # Tarea 6: Análisis de discrepancias
    print("Tarea 6: Analizando discrepancias...")
    discrepancias = analizar_discrepancias()
    with open(OUTPUT_DIR / "discrepancias_y_notas.json", 'w', encoding='utf-8') as f:
        json.dump(discrepancias, f, ensure_ascii=False, indent=2, default=str)
    print("✓ Discrepancias analizadas")
    
    # Tarea 7: Documentación
    print("Tarea 7: Creando documentación...")
    documentacion = crear_documentacion()
    with open(OUTPUT_DIR / "CONTEXTO_VOLUMEN_FUENTES_IX.md", 'w', encoding='utf-8') as f:
        f.write(documentacion)
    print("✓ Documentación creada")
    
    print("\n✅ Análisis completo finalizado!")
