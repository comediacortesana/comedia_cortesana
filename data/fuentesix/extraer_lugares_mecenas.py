#!/usr/bin/env python3
import json
import re
import unicodedata
from collections import defaultdict
from datetime import datetime
from pathlib import Path


BASE_DIR = Path('/Users/ivansimo/Documents/2025/ITEM/COMEDIA26/comedia_cortesana/data/fuentesix')
OUTPUT_PATH = BASE_DIR / 'analisis_lugares_mecenas.json'
FUENTE_LABEL = 'Fuentes IX'


def load_json(path: Path):
    return json.loads(path.read_text(encoding='utf-8'))


def normalize_text(value: str) -> str:
    if value is None:
        return ''
    text = str(value).strip().lower()
    text = ''.join(
        ch for ch in unicodedata.normalize('NFD', text)
        if unicodedata.category(ch) != 'Mn'
    )
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def split_sentences(text: str):
    if not text:
        return []
    normalized = re.sub(r'\s+', ' ', text).strip()
    parts = re.split(r'(?<=[\.\?\!])\s+', normalized)
    return [p.strip() for p in parts if p.strip()]


def collect_extraction_files():
    patterns = [
        'extraccion_part_*_con_metadata_con_referencias_paginas_sintesis_validacion.json',
        'extraccion_part_*_con_metadata_con_referencias_paginas.json',
        'extraccion_part_*_con_metadata_analisis_ia.json',
        'extraccion_part_*_con_metadata.json',
        'extraccion_part_*.json',
    ]
    files = []
    for pattern in patterns:
        files.extend(BASE_DIR.glob(pattern))
    # unique + stable order
    unique = {}
    for path in sorted(files):
        unique[path.name] = path
    return list(unique.values())


def build_places_index(places_hierarchy, lugares_procesados):
    places_by_id = {}
    variant_index = defaultdict(set)

    categorias = places_hierarchy.get('lugares_teatrales', {}).get('categorias', {})
    for categoria_id, categoria in categorias.items():
        lugares = categoria.get('lugares', {})
        for lugar_id, lugar in lugares.items():
            entry = dict(lugar)
            entry['id'] = lugar_id
            entry['categoria_id'] = categoria_id
            entry['categoria_nombre'] = categoria.get('nombre', categoria_id)
            places_by_id[lugar_id] = entry

            nombres = [lugar.get('nombre', '')] + lugar.get('variantes', [])
            for nombre in nombres:
                norm = normalize_text(nombre)
                if norm:
                    variant_index[norm].add(lugar_id)

    # merge lugares_procesados as fallback variants
    lugares_norm = lugares_procesados.get('lugares_normalizados', {})
    for lugar_id, lugar in lugares_norm.items():
        if lugar_id not in places_by_id:
            entry = dict(lugar)
            entry['id'] = lugar_id
            entry['categoria_id'] = lugar.get('categoria', 'sin_categoria')
            entry['categoria_nombre'] = lugar.get('categoria', 'Sin categoría')
            places_by_id[lugar_id] = entry
        nombres = [lugar.get('nombre', '')] + lugar.get('variantes', [])
        for nombre in nombres:
            norm = normalize_text(nombre)
            if norm:
                variant_index[norm].add(lugar_id)

    return places_by_id, variant_index


def extract_text_fields(item):
    texts = []
    for key in ('texto_original', 'sintesis'):
        if item.get(key):
            texts.append(item.get(key))
    frases = item.get('frases')
    if isinstance(frases, list):
        texts.extend([f for f in frases if f])

    datos_json = item.get('datos_json') or {}
    if isinstance(datos_json, dict):
        if datos_json.get('texto_original'):
            texts.append(datos_json.get('texto_original'))
    metadata = item.get('metadata') or {}
    if isinstance(metadata, dict) and metadata.get('texto_original'):
        texts.append(metadata.get('texto_original'))

    return texts


def collect_items_from_file(path: Path):
    data = load_json(path)
    items = []
    if isinstance(data, dict):
        metadata_archivo = data.get('metadata_archivo') or {}
        archivo_fuente = metadata_archivo.get('archivo_fuente') or ''
        if archivo_fuente and 'FUENTES IX' not in archivo_fuente:
            return [], data
        for key in ('representaciones', 'obras', 'lugares'):
            if isinstance(data.get(key), list):
                items.extend(data.get(key))
    elif isinstance(data, list):
        items = data
    return items, data


def extract_mentions(items, places_by_id, variant_index, source_name):
    place_mentions = []
    mecenas_mentions = []

    mecenas_patterns = [
        r'\bmecenas\b',
        r'\bpatrono\b',
        r'\bpatronazgo\b',
        r'\bprotector(?:a)?\b',
        r'\bpatrocinio\b',
        r'\bpatrocinador(?:a)?\b',
        r'\ba\s+expensas\s+de\b',
        r'\bpor\s+mandato\s+de\b',
        r'\bpor\s+mandado\s+de\b',
        r'\bpor\s+orden\s+de\b',
        r'\ben\s+honor\s+de\b',
        r'\bfiesta\s+en\s+honor\s+de\b',
        r'\bfiesta\s+por\s+orden\s+de\b',
    ]
    mecenas_regex = re.compile('|'.join(mecenas_patterns), re.IGNORECASE)
    titulo_regex = re.compile(
        r'\b(rey|reina|duque|duquesa|conde|condesa|marques|marquesa|arzobispo|cardenal)\b',
        re.IGNORECASE
    )
    nombre_regex = re.compile(r'\bde\s+[A-ZÁÉÍÓÚÑ][A-Za-zÁÉÍÓÚÑáéíóúñ\s]+')

    for item in items:
        if not isinstance(item, dict):
            continue
        datos_json = item.get('datos_json') or {}
        metadata = item.get('metadata') or {}

        obra_titulo = (
            datos_json.get('obra_titulo')
            or item.get('obra_titulo')
            or item.get('titulo')
            or item.get('Título')
            or ''
        )
        pagina_pdf = (
            datos_json.get('pagina_pdf')
            or metadata.get('pagina_pdf')
            or item.get('pagina_pdf')
        )

        lugar_nombre = (
            datos_json.get('lugar_nombre')
            or datos_json.get('lugar')
            or datos_json.get('lugar_representacion')
            or ''
        )

        texts = extract_text_fields(item)
        sentences = []
        for text in texts:
            sentences.extend(split_sentences(text))

        # Place mentions: explicit lugar_nombre
        if lugar_nombre:
            norm = normalize_text(lugar_nombre)
            for lugar_id in variant_index.get(norm, []):
                place = places_by_id.get(lugar_id, {})
                place_mentions.append({
                    'place_id': lugar_id,
                    'place_name': place.get('nombre', lugar_nombre),
                    'match': lugar_nombre,
                    'source': source_name,
                    'fuente': FUENTE_LABEL,
                    'pagina_pdf': pagina_pdf,
                    'obra_titulo': obra_titulo,
                    'tipo': item.get('tipo') or item.get('tipo_registro'),
                    'id_temporal': item.get('id_temporal'),
                    'contexto': item.get('texto_original') or datos_json.get('texto_original') or '',
                })

        # Place mentions: scan sentences for variants
        for sentence in sentences:
            norm_sentence = normalize_text(sentence)
            if not norm_sentence:
                continue
            for variant_norm, lugar_ids in variant_index.items():
                if variant_norm and variant_norm in norm_sentence:
                    for lugar_id in lugar_ids:
                        place = places_by_id.get(lugar_id, {})
                        place_mentions.append({
                            'place_id': lugar_id,
                            'place_name': place.get('nombre', ''),
                            'match': variant_norm,
                            'source': source_name,
                            'fuente': FUENTE_LABEL,
                            'pagina_pdf': pagina_pdf,
                            'obra_titulo': obra_titulo,
                            'tipo': item.get('tipo') or item.get('tipo_registro'),
                            'id_temporal': item.get('id_temporal'),
                            'contexto': sentence,
                        })

            # Mecenas/anecdotario
            if mecenas_regex.search(sentence) or titulo_regex.search(sentence):
                nombres = nombre_regex.findall(sentence)
                mecenas_mentions.append({
                    'source': source_name,
                    'fuente': FUENTE_LABEL,
                    'pagina_pdf': pagina_pdf,
                    'obra_titulo': obra_titulo,
                    'tipo': item.get('tipo') or item.get('tipo_registro'),
                    'id_temporal': item.get('id_temporal'),
                    'contexto': sentence,
                    'patrones': list(set(mecenas_regex.findall(sentence))),
                    'titulos': list(set(titulo_regex.findall(sentence))),
                    'nombres': list(set([n.strip() for n in nombres])),
                })

    return place_mentions, mecenas_mentions


def main():
    places_hierarchy_path = BASE_DIR / 'places_hierarchy.json'
    lugares_procesados_path = BASE_DIR / 'lugares_procesados.json'

    places_hierarchy = load_json(places_hierarchy_path) if places_hierarchy_path.exists() else {}
    lugares_procesados = load_json(lugares_procesados_path) if lugares_procesados_path.exists() else {}

    places_by_id, variant_index = build_places_index(places_hierarchy, lugares_procesados)

    files = collect_extraction_files()
    all_place_mentions = []
    all_mecenas_mentions = []
    total_items = 0

    for path in files:
        items, _ = collect_items_from_file(path)
        total_items += len(items)
        place_mentions, mecenas_mentions = extract_mentions(items, places_by_id, variant_index, path.name)
        all_place_mentions.extend(place_mentions)
        all_mecenas_mentions.extend(mecenas_mentions)

    places_with_mentions = defaultdict(list)
    for mention in all_place_mentions:
        places_with_mentions[mention['place_id']].append(mention)

    categorias_tree = {}
    categorias = places_hierarchy.get('lugares_teatrales', {}).get('categorias', {})
    for categoria_id, categoria in categorias.items():
        lugares = categoria.get('lugares', {})
        categorias_tree[categoria_id] = {
            'nombre': categoria.get('nombre', categoria_id),
            'descripcion': categoria.get('descripcion', ''),
            'tipo': categoria.get('tipo', ''),
            'lugares': [
                {
                    'id': lugar_id,
                    'nombre': lugar.get('nombre', ''),
                    'ciudad': (lugar.get('coordenadas') or {}).get('ciudad', ''),
                    'menciones': len(places_with_mentions.get(lugar_id, [])),
                }
                for lugar_id, lugar in lugares.items()
            ],
        }

    output = {
        'metadata': {
            'fecha_generacion': datetime.utcnow().isoformat() + 'Z',
            'fuente': FUENTE_LABEL,
            'archivos_analizados': [p.name for p in files],
            'total_items': total_items,
            'total_menciones_lugares': len(all_place_mentions),
            'total_menciones_mecenas': len(all_mecenas_mentions),
        },
        'categorias': categorias_tree,
        'lugares': {
            place_id: {
                **place,
                'menciones': places_with_mentions.get(place_id, []),
            }
            for place_id, place in places_by_id.items()
        },
        'menciones_lugares': all_place_mentions,
        'mecenas_anecdotario': all_mecenas_mentions,
    }

    OUTPUT_PATH.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f'✅ Archivo generado: {OUTPUT_PATH}')
    print(f'   Lugares: {len(places_by_id)}')
    print(f'   Menciones lugares: {len(all_place_mentions)}')
    print(f'   Menciones mecenas/anecdotario: {len(all_mecenas_mentions)}')


if __name__ == '__main__':
    main()
