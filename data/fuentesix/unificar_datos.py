#!/usr/bin/env python3
"""
Script para unificar datos de FUENTES IX con datos_obras.json
Mantiene separación entre CATCOM y FUENTESIX
"""

import json
import re
from pathlib import Path
from datetime import datetime
from collections import defaultdict

# Rutas
BASE_DIR = Path(__file__).parent.parent.parent
DATOS_OBRAS = BASE_DIR / "filtro_basico" / "datos_obras.json"
CONTEXTO_FUENTESIX = Path(__file__).parent / "contexto_extraido_por_tipo.json"
OUTPUT_DIR = BASE_DIR / "filtro_basico"

def normalizar_titulo(titulo):
    """Normaliza título: quita ', El/La/Los/Las' y limpia"""
    if not titulo:
        return ""
    # Quitar artículo al final
    titulo_limpio = re.sub(r',\s*(El|La|Los|Las)$', '', titulo.strip())
    # Normalizar espacios y mayúsculas
    titulo_limpio = ' '.join(titulo_limpio.split())
    return titulo_limpio

def extraer_anio_de_fecha(fecha_str):
    """Extrae año de una fecha en formato español"""
    if not fecha_str:
        return None
    # Buscar año de 4 dígitos
    match = re.search(r'(\d{4})', str(fecha_str))
    if match:
        año = int(match.group(1))
        if 1500 <= año <= 2000:
            return año
    return None

def convertir_representacion_fuentesix(rep_fuentesix, obra_titulo):
    """Convierte representación de formato FUENTES IX a formato datos_obras.json"""
    fecha_original = rep_fuentesix.get("fecha", "").strip()
    fecha_formateada = None
    
    # Intentar parsear fecha
    año = extraer_anio_de_fecha(fecha_original)
    if año:
        # Intentar extraer mes y día si están disponibles
        meses = {
            'enero': '01', 'febrero': '02', 'marzo': '03', 'abril': '04',
            'mayo': '05', 'junio': '06', 'julio': '07', 'agosto': '08',
            'septiembre': '09', 'octubre': '10', 'noviembre': '11', 'diciembre': '12'
        }
        mes_match = re.search(r'(\d{1,2})\s+de\s+([a-záéíóúñ]+)', fecha_original.lower())
        if mes_match:
            dia = mes_match.group(1).zfill(2)
            mes_nombre = mes_match.group(2)
            mes = meses.get(mes_nombre, '01')
            fecha_formateada = f"{año}-{mes}-{dia}"
        else:
            fecha_formateada = f"{año}-01-01"
    
    lugar = rep_fuentesix.get("lugar", "").strip()
    compania = rep_fuentesix.get("compania", "").strip()
    
    # Determinar tipo de lugar
    tipo_lugar = ""
    if "Palacio" in lugar or "Buen Retiro" in lugar:
        tipo_lugar = "palacio"
    elif "Corral" in lugar:
        tipo_lugar = "corral"
    elif "Coliseo" in lugar:
        tipo_lugar = "teatro"
    else:
        tipo_lugar = "otro"
    
    # Extraer región/ciudad
    region = ""
    ciudad = ""
    if "Madrid" in lugar or "Palacio" in lugar or "Buen Retiro" in lugar:
        ciudad = "Madrid"
        region = "Comunidad de Madrid"
    elif "Toledo" in lugar:
        ciudad = "Toledo"
        region = "Castilla-La Mancha"
    elif "Valladolid" in lugar:
        ciudad = "Valladolid"
        region = "Castilla y León"
    elif "Pardo" in lugar:
        ciudad = "El Pardo"
        region = "Comunidad de Madrid"
    
    return {
        "fecha": fecha_original,
        "fecha_formateada": fecha_formateada,
        "compania": compania,
        "director_compañia": compania,  # Asumir que compañía = director
        "lugar": lugar,
        "tipo_lugar": tipo_lugar,
        "region": region,
        "ciudad": ciudad,
        "fuente": f"Fuentes {rep_fuentesix.get('fuente', 'IX')}",
        "observaciones": f"Número de representación: {rep_fuentesix.get('numero', 'N/A')}",
        "mecenas": "",
        "organizadores_fiesta": [],
        "personajes_historicos": [],
        "tipo_funcion": "representación_normal",
        "publico": "corte" if tipo_lugar == "palacio" else "público"
    }

def convertir_obra_fuentesix(obra_fuentesix, id_base):
    """Convierte obra de formato FUENTES IX a formato datos_obras.json"""
    titulo_original = obra_fuentesix.get("titulo", "").strip()
    titulo_normalizado = normalizar_titulo(titulo_original)
    
    # Extraer autor
    autor_nombre = obra_fuentesix.get("autor")
    if autor_nombre:
        # Limpiar autor (puede venir como "Calderón impresa en...")
        autor_match = re.search(r'^([A-ZÁÉÍÓÚÑ][^,\.]+)', str(autor_nombre))
        if autor_match:
            autor_nombre = autor_match.group(1).strip()
        else:
            autor_nombre = autor_nombre.strip()
    else:
        autor_nombre = "Anónimo"
    
    # Convertir representaciones
    representaciones = []
    for rep in obra_fuentesix.get("representaciones", []):
        rep_convertida = convertir_representacion_fuentesix(rep, titulo_normalizado)
        representaciones.append(rep_convertida)
    
    # Títulos alternativos
    titulos_alt = obra_fuentesix.get("titulos_alternativos", [])
    titulo_alternativo = "; ".join([t.strip() for t in titulos_alt if t.strip()])
    
    # Extraer año de primera representación si existe
    fecha_creacion = None
    if representaciones:
        primera_rep = representaciones[0]
        año = extraer_anio_de_fecha(primera_rep.get("fecha"))
        if año:
            fecha_creacion = str(año)
    
    obra = {
        "id": id_base,
        "titulo": titulo_normalizado,
        "titulo_original": titulo_original,
        "titulo_alternativo": titulo_alternativo,
        "autor": {
            "nombre": autor_nombre,
            "nombre_completo": autor_nombre,
            "fecha_nacimiento": "",
            "fecha_muerte": "",
            "biografia": "",
            "epoca": "Siglo de Oro"
        },
        "tipo_obra": "comedia",  # Asumir comedia por defecto
        "genero": "",
        "subgenero": "",
        "fuente": "FUENTES IX",
        "origen_datos": "pdf",
        "pagina_pdf": None,
        "texto_original_pdf": obra_fuentesix.get("texto_completo", "")[:500] if "texto_completo" in obra_fuentesix else "",
        "fecha_creacion": fecha_creacion or "",
        "tema": "",
        "actos": None,
        "versos": None,
        "idioma": "Español",
        "musica_conservada": False,
        "compositor": "",
        "bibliotecas_musica": "",
        "bibliografia_musica": "",
        "mecenas": "",
        "edicion_principe": "",
        "notas_bibliograficas": "",
        "manuscritos_conocidos": "",
        "ediciones_conocidas": "",
        "notas": f"Extraído de FUENTES IX - {obra_fuentesix.get('archivo', 'desconocido')}",
        "observaciones": "",
        "total_representaciones": len(representaciones),
        "representaciones": representaciones,
        "lugar": representaciones[0].get("lugar", "") if representaciones else "",
        "tipo_lugar": representaciones[0].get("tipo_lugar", "") if representaciones else "",
        "region": representaciones[0].get("region", "") if representaciones else "",
        "compania": representaciones[0].get("compania", "") if representaciones else "",
        "director_compañia": representaciones[0].get("director_compañia", "") if representaciones else ""
    }
    
    return obra, titulo_normalizado

def unificar_datos():
    """Función principal para unificar datos"""
    print("🔄 Iniciando unificación de datos...")
    
    # 1. Cargar datos existentes
    print("📖 Cargando datos_obras.json...")
    with open(DATOS_OBRAS, 'r', encoding='utf-8') as f:
        datos_existentes = json.load(f)
    
    obras_existentes = datos_existentes.get("obras", [])
    print(f"   ✓ {len(obras_existentes)} obras existentes cargadas")
    
    # Crear mapa de obras existentes por título normalizado
    mapa_existentes = {}
    for obra in obras_existentes:
        titulo_norm = normalizar_titulo(obra.get("titulo", ""))
        if titulo_norm:
            if titulo_norm not in mapa_existentes:
                mapa_existentes[titulo_norm] = []
            mapa_existentes[titulo_norm].append(obra)
    
    # 2. Cargar datos de FUENTES IX
    print("📖 Cargando contexto_extraido_por_tipo.json...")
    with open(CONTEXTO_FUENTESIX, 'r', encoding='utf-8') as f:
        contexto_fuentesix = json.load(f)
    
    obras_fuentesix = contexto_fuentesix.get("obras", [])
    print(f"   ✓ {len(obras_fuentesix)} obras de FUENTES IX cargadas")
    
    # 3. Procesar obras de FUENTES IX
    print("\n🔄 Procesando obras de FUENTES IX...")
    obras_nuevas = []
    obras_actualizadas = []
    obras_duplicadas = []
    
    # Obtener último ID
    max_id = max([obra.get("id", 0) for obra in obras_existentes], default=0)
    siguiente_id = max_id + 1
    
    for obra_fuentesix in obras_fuentesix:
        obra_convertida, titulo_norm = convertir_obra_fuentesix(obra_fuentesix, siguiente_id)
        
        # Buscar si existe obra con mismo título
        if titulo_norm in mapa_existentes:
            # Existe duplicado - combinar datos
            obras_existentes_encontradas = mapa_existentes[titulo_norm]
            
            for obra_existente in obras_existentes_encontradas:
                fuente_existente = normalizarFuente(obra_existente.get("fuente", ""))
                
                if fuente_existente == "CATCOM":
                    # Combinar: marcar como AMBAS y añadir representaciones
                    print(f"   🔀 Combinando: {titulo_norm} (CATCOM + FUENTES IX)")
                    
                    # Marcar como AMBAS
                    obra_existente["fuente"] = "AMBAS"
                    
                    # Añadir representaciones de FUENTES IX (evitar duplicados)
                    reps_existentes = {json.dumps(r, sort_keys=True) for r in obra_existente.get("representaciones", [])}
                    for rep_nueva in obra_convertida.get("representaciones", []):
                        rep_key = json.dumps(rep_nueva, sort_keys=True)
                        if rep_key not in reps_existentes:
                            obra_existente["representaciones"].append(rep_nueva)
                    
                    # Actualizar total
                    obra_existente["total_representaciones"] = len(obra_existente["representaciones"])
                    
                    # Actualizar campos si están vacíos en CATCOM
                    if not obra_existente.get("autor", {}).get("nombre") or obra_existente.get("autor", {}).get("nombre") == "Anónimo":
                        if obra_convertida.get("autor", {}).get("nombre") != "Anónimo":
                            obra_existente["autor"] = obra_convertida["autor"]
                    
                    if not obra_existente.get("fecha_creacion"):
                        obra_existente["fecha_creacion"] = obra_convertida.get("fecha_creacion", "")
                    
                    obras_actualizadas.append(titulo_norm)
                    break
                elif fuente_existente == "FUENTES IX" or fuente_existente == "FUENTESIX":
                    # Ya existe de FUENTES IX - no duplicar
                    obras_duplicadas.append(titulo_norm)
                    break
        else:
            # Nueva obra - añadir
            obras_nuevas.append(obra_convertida)
            siguiente_id += 1
    
    print(f"\n📊 Resumen de procesamiento:")
    print(f"   ✓ Nuevas obras: {len(obras_nuevas)}")
    print(f"   ✓ Obras actualizadas (combinadas): {len(obras_actualizadas)}")
    print(f"   ⚠ Obras duplicadas (omitidas): {len(obras_duplicadas)}")
    
    # 4. Crear resultado final
    print("\n📝 Creando archivo unificado...")
    
    # Añadir nuevas obras
    obras_finales = obras_existentes + obras_nuevas
    
    # Actualizar metadata
    fuentes_unicas = set()
    for obra in obras_finales:
        fuente = normalizarFuente(obra.get("fuente", ""))
        if fuente:
            fuentes_unicas.add(fuente)
    
    metadata_actualizada = {
        **datos_existentes.get("metadata", {}),
        "version": "1.1",
        "fecha_actualizacion": datetime.now().strftime("%Y-%m-%d"),
        "fecha_completa": datetime.now().isoformat(),
        "total_obras": len(obras_finales),
        "fuentes": sorted(list(fuentes_unicas)),
        "descripcion": "Obras del teatro español del Siglo de Oro - Base de datos DELIA (Unificado con FUENTES IX)",
        "ultima_unificacion": {
            "fecha": datetime.now().isoformat(),
            "obras_nuevas_fuentesix": len(obras_nuevas),
            "obras_combinadas": len(obras_actualizadas),
            "obras_duplicadas_omitidas": len(obras_duplicadas)
        }
    }
    
    resultado = {
        "metadata": metadata_actualizada,
        "obras": obras_finales
    }
    
    # 5. Guardar resultado
    archivo_salida = OUTPUT_DIR / "datos_obras.json"
    print(f"💾 Guardando en {archivo_salida}...")
    
    with open(archivo_salida, 'w', encoding='utf-8') as f:
        json.dump(resultado, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Archivo guardado: {len(obras_finales)} obras totales")
    print(f"   - CATCOM: {sum(1 for o in obras_finales if normalizarFuente(o.get('fuente', '')) == 'CATCOM')}")
    print(f"   - FUENTES IX: {sum(1 for o in obras_finales if normalizarFuente(o.get('fuente', '')) == 'FUENTES IX')}")
    print(f"   - AMBAS: {sum(1 for o in obras_finales if normalizarFuente(o.get('fuente', '')) == 'AMBAS')}")
    
    return resultado

def normalizarFuente(valor):
    """Normaliza el valor de fuente"""
    if not valor:
        return ""
    limpio = str(valor).strip().upper().replace(" ", "")
    if "FUENTESIX" in limpio or "FUENTESXI" in limpio:
        return "FUENTES IX"
    return valor.strip()

if __name__ == "__main__":
    try:
        resultado = unificar_datos()
        print("\n✅ Unificación completada exitosamente!")
    except Exception as e:
        print(f"\n❌ Error durante la unificación: {e}")
        import traceback
        traceback.print_exc()
