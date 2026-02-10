#!/usr/bin/env python3
import json
import re
import unicodedata
from datetime import datetime
from pathlib import Path


BASE_DIR = Path('/Users/ivansimo/Documents/2025/ITEM/COMEDIA26/comedia_cortesana/data/fuentesix')
OUTPUT_PATH = BASE_DIR / 'analisis_fechas_fuentesix.json'
FUENTE_LABEL = 'Fuentes IX'


MESES = [
    'enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio',
    'julio', 'agosto', 'septiembre', 'setiembre', 'octubre', 'noviembre', 'diciembre'
]


def load_json(path: Path):
    return json.loads(path.read_text(encoding='utf-8'))


def normalize_text(value: str) -> str:
    if value is None:
        return ''
    text = str(value).strip()
    text = ''.join(
        ch for ch in unicodedata.normalize('NFD', text)
        if unicodedata.category(ch) != 'Mn'
    )
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
    unique = {}
    for path in sorted(files):
        unique[path.name] = path
    return list(unique.values())


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


def find_date_mentions(sentence: str):
    if not sentence:
        return []
    normalized = normalize_text(sentence).lower()
    months = '|'.join(MESES)
    patterns = [
        rf'\b(\d{{1,2}})\s+de\s+({months})\s+de\s+(\d{{4}})\b',
        rf'\b({months})\s+de\s+(\d{{4}})\b',
        r'\b(1[0-9]{3}|20[0-9]{2})\b',
    ]
    matches = []
    for pattern in patterns:
        for m in re.finditer(pattern, normalized):
            matches.append(m.group(0))
    return matches


def main():
    files = collect_extraction_files()
    mentions = []
    total_items = 0

    for path in files:
        items, _ = collect_items_from_file(path)
        total_items += len(items)
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
            tipo = item.get('tipo') or item.get('tipo_registro')

            texts = extract_text_fields(item)
            sentences = []
            for text in texts:
                sentences.extend(split_sentences(text))

            for sentence in sentences:
                found = find_date_mentions(sentence)
                if not found:
                    continue
                for date_str in found:
                    year_match = re.search(r'(1[0-9]{3}|20[0-9]{2})', date_str)
                    year = int(year_match.group(1)) if year_match else None
                    mentions.append({
                        'fuente': FUENTE_LABEL,
                        'source': path.name,
                        'obra_titulo': obra_titulo,
                        'pagina_pdf': pagina_pdf,
                        'tipo': tipo,
                        'id_temporal': item.get('id_temporal'),
                        'fecha_mencionada': date_str,
                        'anio': year,
                        'contexto': sentence,
                    })

    output = {
        'metadata': {
            'fecha_generacion': datetime.utcnow().isoformat() + 'Z',
            'fuente': FUENTE_LABEL,
            'archivos_analizados': [p.name for p in files],
            'total_items': total_items,
            'total_menciones_fechas': len(mentions),
        },
        'menciones_fechas': mentions,
    }

    OUTPUT_PATH.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f'✅ Archivo generado: {OUTPUT_PATH}')
    print(f'   Menciones fechas: {len(mentions)}')


if __name__ == '__main__':
    main()
