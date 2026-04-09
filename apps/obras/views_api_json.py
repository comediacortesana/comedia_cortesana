"""
Vista API que genera el JSON completo de obras en el formato que index.html espera.

Endpoint: /api/datos-obras/
Devuelve: { metadata: {...}, obras: [...] }
"""

import json

from django.http import JsonResponse
from django.views.decorators.http import require_GET

from apps.autores.models import Autor
from apps.lugares.models import Lugar
from apps.obras.models import Obra
from apps.representaciones.models import Representacion


def _serializar_autor(autor):
    if not autor:
        return None
    return {
        "nombre": autor.nombre or "",
        "nombre_completo": autor.nombre_completo or "",
        "fecha_nacimiento": autor.fecha_nacimiento or "",
        "fecha_muerte": autor.fecha_muerte or "",
        "biografia": autor.biografia or "",
        "epoca": autor.epoca or "",
    }


def _serializar_representacion(rep):
    lugar_nombre = ""
    region = ""
    pais = ""
    if rep.lugar:
        lugar_nombre = rep.lugar.nombre or ""
        region = rep.lugar.region or ""
        pais = rep.lugar.pais or "España"

    fecha_fmt = ""
    if rep.fecha_formateada:
        fecha_fmt = rep.fecha_formateada.isoformat()

    return {
        "fecha": rep.fecha or "",
        "fecha_formateada": fecha_fmt,
        "compania": rep.compañia or "",
        "director_compañia": rep.director_compañia or "",
        "lugar": lugar_nombre,
        "tipo_lugar": rep.tipo_lugar or "",
        "region": region,
        "pais": pais,
        "fuente": rep.fuente or "",
        "observaciones": rep.observaciones or "",
        "mecenas": rep.mecenas or "",
        "gestor_administrativo": rep.gestor_administrativo or "",
        "personajes_historicos": _parse_json_field(rep.personajes_historicos),
        "organizadores_fiesta": _parse_json_field(rep.organizadores_fiesta),
        "tipo_funcion": rep.tipo_funcion or "",
        "publico": rep.publico or "",
        "entrada": rep.entrada or "",
        "duracion": rep.duracion or "",
        "notas": rep.notas or "",
        "pagina_pdf": rep.pagina_pdf,
        "es_anterior_1650": rep.es_anterior_1650,
        "es_anterior_1665": rep.es_anterior_1665,
    }


def _parse_json_field(valor):
    if not valor:
        return []
    if isinstance(valor, list):
        return valor
    try:
        parsed = json.loads(valor)
        return parsed if isinstance(parsed, list) else []
    except (json.JSONDecodeError, TypeError):
        return []


def _normalizar_fuente_display(fuente):
    if not fuente:
        return ""
    limpio = fuente.strip().upper().replace(" ", "")
    if limpio in ("FUENTESXI", "FUENTESIX"):
        return "FUENTES IX"
    if limpio == "CATCOM":
        return "CATCOM"
    if limpio == "AMBAS":
        return "AMBAS"
    return fuente


@require_GET
def datos_obras_api(request):
    """Devuelve todas las obras con representaciones en formato JSON para index.html."""
    obras = (
        Obra.objects
        .select_related("autor")
        .prefetch_related("representaciones__lugar")
        .order_by("id")
    )

    resultado = []
    for obra in obras:
        reps = obra.representaciones.all()

        lugar_principal = ""
        region_principal = ""
        tipo_lugar_principal = ""
        compania_principal = ""
        if reps:
            primera = reps[0]
            if primera.lugar:
                lugar_principal = primera.lugar.nombre or ""
                region_principal = primera.lugar.region or ""
            tipo_lugar_principal = primera.tipo_lugar or ""
            compania_principal = primera.compañia or ""

        obra_dict = {
            "id": obra.id,
            "titulo": obra.titulo_limpio or obra.titulo,
            "titulo_original": obra.titulo,
            "titulo_alternativo": obra.titulo_alternativo or "",
            "autor": _serializar_autor(obra.autor),
            "tipo_obra": obra.tipo_obra or "",
            "genero": obra.genero or "",
            "subgenero": obra.subgenero or "",
            "fuente": _normalizar_fuente_display(obra.fuente_principal),
            "origen_datos": obra.origen_datos or "",
            "pagina_pdf": obra.pagina_pdf,
            "texto_original_pdf": obra.texto_original_pdf or "",
            "tema": obra.tema or "",
            "musica_conservada": "Sí" if obra.musica_conservada else "No",
            "compositor": obra.compositor or "",
            "bibliotecas_musica": obra.bibliotecas_musica or "",
            "bibliografia_musica": obra.bibliografia_musica or "",
            "mecenas": obra.mecenas or "",
            "fecha_creacion": obra.fecha_creacion_estimada or "",
            "idioma": obra.idioma or "",
            "versos": obra.versos,
            "actos": obra.actos,
            "notas": obra.notas or "",
            "notas_bibliograficas": obra.notas_bibliograficas or "",
            "edicion_principe": obra.edicion_principe or "",
            "manuscritos_conocidos": obra.manuscritos_conocidos or "",
            "ediciones_conocidas": obra.ediciones_conocidas or "",
            "observaciones": obra.observaciones or "",
            "lugar": lugar_principal,
            "region": region_principal,
            "tipo_lugar": tipo_lugar_principal,
            "compania": compania_principal,
            "total_representaciones": reps.count(),
            "representaciones": [_serializar_representacion(r) for r in reps],
        }
        resultado.append(obra_dict)

    metadata = {
        "version": "2.0",
        "total_obras": len(resultado),
        "total_autores": Autor.objects.count(),
        "total_lugares": Lugar.objects.count(),
        "total_representaciones": Representacion.objects.count(),
        "fuente": "Django DB",
        "fuentes": ["FUENTES IX", "CATCOM", "AMBAS"],
    }

    return JsonResponse(
        {"metadata": metadata, "obras": resultado},
        json_dumps_params={"ensure_ascii": False},
    )
