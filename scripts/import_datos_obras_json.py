#!/usr/bin/env python
"""
Importa datos desde datos_obras.json a modelos Django (SQLite o PostgreSQL).
"""

import json
import os
import sys
from pathlib import Path

import django

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "teatro_espanol.settings")
django.setup()

from apps.autores.models import Autor
from apps.obras.models import Obra


VALID_TIPO_OBRA = {"comedia", "auto", "zarzuela", "entremes", "tragedia", "loa", "sainete", "baile", "otro"}
VALID_FUENTE = {"FUENTESXI", "CATCOM", "AMBAS"}


def normalize_tipo_obra(value: str) -> str:
    if not value:
        return "otro"
    value = value.strip().lower()
    return value if value in VALID_TIPO_OBRA else "otro"


def normalize_fuente(value: str) -> str:
    if not value:
        return "CATCOM"
    value = value.strip().upper()
    if value == "FUENTES IX":
        return "FUENTESXI"
    return value if value in VALID_FUENTE else "CATCOM"


def to_int_or_none(value):
    if value in ("", None):
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def main():
    json_path = BASE_DIR / "datos_obras.json"
    if not json_path.exists():
        print(f"ERROR: no existe {json_path}")
        return 1

    with json_path.open("r", encoding="utf-8") as f:
        payload = json.load(f)

    obras = payload.get("obras", [])
    print(f"Obras en JSON: {len(obras)}")

    created, updated = 0, 0

    for item in obras:
        titulo = (item.get("titulo") or "").strip()
        titulo_limpio = (item.get("titulo_original") or item.get("titulo") or "").strip()
        if not titulo_limpio:
            continue

        autor = None
        autor_data = item.get("autor") or {}
        autor_nombre = (autor_data.get("nombre") or "").strip()
        if autor_nombre:
            autor, _ = Autor.objects.get_or_create(
                nombre=autor_nombre,
                defaults={
                    "nombre_completo": (autor_data.get("nombre_completo") or "").strip(),
                    "fecha_nacimiento": (autor_data.get("fecha_nacimiento") or "").strip(),
                    "fecha_muerte": (autor_data.get("fecha_muerte") or "").strip(),
                    "biografia": (autor_data.get("biografia") or "").strip(),
                    "epoca": (autor_data.get("epoca") or "Siglo de Oro").strip(),
                },
            )

        defaults = {
            "titulo": titulo or titulo_limpio,
            "titulo_alternativo": (item.get("titulo_alternativo") or "").strip(),
            "autor": autor,
            "tipo_obra": normalize_tipo_obra(item.get("tipo_obra")),
            "genero": (item.get("genero") or "").strip(),
            "subgenero": (item.get("subgenero") or "").strip(),
            "edicion_principe": (item.get("edicion_principe") or "").strip(),
            "notas_bibliograficas": (item.get("notas_bibliograficas") or "").strip(),
            "fuente_principal": normalize_fuente(item.get("fuente")),
            "origen_datos": ((item.get("origen_datos") or "web").strip().lower() if (item.get("origen_datos") or "web").strip().lower() in {"web", "pdf", "manual"} else "web"),
            "pagina_pdf": to_int_or_none(item.get("pagina_pdf")),
            "texto_original_pdf": (item.get("texto_original_pdf") or "").strip(),
            "tema": (item.get("tema") or "").strip(),
            "musica_conservada": bool(item.get("musica_conservada", False)),
            "compositor": (item.get("compositor") or "").strip(),
            "bibliotecas_musica": (item.get("bibliotecas_musica") or "").strip(),
            "bibliografia_musica": (item.get("bibliografia_musica") or "").strip(),
            "mecenas": (item.get("mecenas") or "").strip(),
            "fecha_creacion_estimada": (item.get("fecha_creacion") or "").strip(),
            "idioma": ((item.get("idioma") or "español").strip().lower() or "español"),
            "versos": to_int_or_none(item.get("versos")),
            "actos": to_int_or_none(item.get("actos")),
            "notas": (item.get("notas") or "").strip(),
            "manuscritos_conocidos": (item.get("manuscritos_conocidos") or "").strip(),
            "ediciones_conocidas": (item.get("ediciones_conocidas") or "").strip(),
            "observaciones": (item.get("observaciones") or "").strip(),
        }

        obra, was_created = Obra.objects.update_or_create(
            titulo_limpio=titulo_limpio,
            defaults=defaults,
        )
        if was_created:
            created += 1
        else:
            updated += 1

    print(f"Importación completada: creadas={created}, actualizadas={updated}, total_db={Obra.objects.count()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
