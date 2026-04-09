"""
Management command para exportar la DB a datos_obras.json.

Genera el mismo formato { metadata, obras } que espera index.html,
reutilizando la lógica de serialización de views_api_json.py.

Uso:
    python manage.py exportar_json                           # escribe datos_obras.json en raíz
    python manage.py exportar_json --salida /tmp/export.json # ruta personalizada
    python manage.py exportar_json --indent 0                # sin indentación (más compacto)
"""

import json
from datetime import datetime
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand

from apps.autores.models import Autor
from apps.lugares.models import Lugar
from apps.obras.models import Obra
from apps.representaciones.models import Representacion
from apps.obras.views_api_json import (
    _serializar_autor,
    _serializar_representacion,
    _normalizar_fuente_display,
)


class Command(BaseCommand):
    help = "Exporta todas las obras de la DB a datos_obras.json"

    def add_arguments(self, parser):
        parser.add_argument(
            "--salida",
            default="",
            help="Ruta de salida (default: datos_obras.json en raíz del proyecto)",
        )
        parser.add_argument(
            "--indent",
            type=int,
            default=2,
            help="Indentación JSON (0 = compacto, default: 2)",
        )
        parser.add_argument(
            "--tambien-frontend",
            action="store_true",
            help="También copiar a frontend/github-pages/datos_obras.json",
        )

    def handle(self, *args, **options):
        salida = options["salida"]
        if not salida:
            salida = str(settings.BASE_DIR / "datos_obras.json")

        indent = options["indent"] or None

        self.stdout.write("Consultando base de datos...")

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
            "fecha_actualizacion": datetime.now().strftime("%Y-%m-%d"),
            "fecha_completa": datetime.now().isoformat(),
            "total_obras": len(resultado),
            "total_autores": Autor.objects.count(),
            "total_lugares": Lugar.objects.count(),
            "total_representaciones": Representacion.objects.count(),
            "fuente": "Django DB",
            "fuentes": ["FUENTES IX", "CATCOM", "AMBAS"],
        }

        payload = {"metadata": metadata, "obras": resultado}

        salida_path = Path(salida)
        salida_path.parent.mkdir(parents=True, exist_ok=True)
        with open(salida_path, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=indent)

        size_kb = salida_path.stat().st_size / 1024
        self.stdout.write(self.style.SUCCESS(
            f"Exportado {len(resultado)} obras -> {salida_path} ({size_kb:.1f} KB)"
        ))

        if options["tambien_frontend"]:
            frontend_path = settings.BASE_DIR / "frontend" / "github-pages" / "datos_obras.json"
            frontend_path.parent.mkdir(parents=True, exist_ok=True)
            with open(frontend_path, "w", encoding="utf-8") as f:
                json.dump(payload, f, ensure_ascii=False, indent=indent)
            self.stdout.write(self.style.SUCCESS(f"Copiado a {frontend_path}"))

        return str(salida_path)
