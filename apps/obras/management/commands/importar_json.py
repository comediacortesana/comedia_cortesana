"""
Management command para importar datos_obras.json en la DB (SQLite / PostgreSQL).

Uso:
    python manage.py importar_json                       # importa datos_obras.json
    python manage.py importar_json --archivo otro.json   # importa otro archivo
    python manage.py importar_json --limpiar             # borra todo antes de importar
    python manage.py importar_json --solo-nuevas         # solo inserta obras que no existan
"""

import json
from datetime import datetime
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from apps.autores.models import Autor
from apps.lugares.models import Lugar
from apps.obras.models import Obra
from apps.representaciones.models import Representacion


def normalizar_fuente(valor):
    if not valor:
        return ""
    limpio = valor.strip().upper().replace(" ", "")
    if limpio in ("FUENTESXI", "FUENTESIX"):
        return "FUENTESXI"
    return valor.strip()


def safe_int(valor, default=None):
    if valor is None:
        return default
    try:
        return int(valor)
    except (ValueError, TypeError):
        return default


def safe_bool(valor):
    if isinstance(valor, bool):
        return valor
    if isinstance(valor, str):
        return valor.strip().lower() in ("true", "sí", "si", "yes", "1")
    return bool(valor) if valor else False


def parsear_fecha(texto):
    """Intenta convertir texto de fecha a date object."""
    if not texto:
        return None
    texto = texto.strip()
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y"):
        try:
            return datetime.strptime(texto, fmt).date()
        except ValueError:
            continue
    return None


class Command(BaseCommand):
    help = "Importa datos_obras.json a la DB relacional (obras, autores, lugares, representaciones)"

    def add_arguments(self, parser):
        parser.add_argument(
            "--archivo",
            default="datos_obras.json",
            help="Ruta al archivo JSON (default: datos_obras.json en raíz del proyecto)",
        )
        parser.add_argument(
            "--limpiar",
            action="store_true",
            help="Eliminar TODOS los datos antes de importar",
        )
        parser.add_argument(
            "--solo-nuevas",
            action="store_true",
            help="Solo importar obras que no existan (por titulo_limpio)",
        )

    def handle(self, *args, **options):
        archivo = Path(options["archivo"])
        if not archivo.is_absolute():
            archivo = settings.BASE_DIR / archivo

        if not archivo.exists():
            raise CommandError(f"Archivo no encontrado: {archivo}")

        self.stdout.write(f"Leyendo {archivo}...")
        with open(archivo, "r", encoding="utf-8") as f:
            data = json.load(f)

        if isinstance(data, dict) and "obras" in data:
            obras_json = data["obras"]
            metadata = data.get("metadata", {})
        elif isinstance(data, list):
            obras_json = data
            metadata = {}
        else:
            raise CommandError("Formato JSON no reconocido")

        self.stdout.write(f"  {len(obras_json)} obras en el archivo")

        if options["limpiar"]:
            self.stdout.write(self.style.WARNING("Limpiando tablas..."))
            Representacion.objects.all().delete()
            Obra.objects.all().delete()
            Lugar.objects.all().delete()
            Autor.objects.all().delete()
            self.stdout.write("  Tablas limpiadas")

        titulos_existentes = set()
        if options["solo_nuevas"]:
            titulos_existentes = set(
                Obra.objects.values_list("titulo_limpio", flat=True)
            )
            self.stdout.write(f"  {len(titulos_existentes)} obras ya existentes (se omitirán)")

        stats = {
            "autores_creados": 0,
            "lugares_creados": 0,
            "obras_creadas": 0,
            "obras_actualizadas": 0,
            "obras_omitidas": 0,
            "representaciones_creadas": 0,
            "errores": 0,
        }

        cache_autores = {}
        cache_lugares = {}

        for obj_autor in Autor.objects.all():
            cache_autores[obj_autor.nombre.lower().strip()] = obj_autor

        for obj_lugar in Lugar.objects.all():
            clave = f"{obj_lugar.nombre.lower().strip()}|{obj_lugar.region.lower().strip()}"
            cache_lugares[clave] = obj_lugar

        self.stdout.write("Importando obras...")

        with transaction.atomic():
            for i, obra_json in enumerate(obras_json):
                try:
                    self._importar_obra(
                        obra_json,
                        cache_autores,
                        cache_lugares,
                        titulos_existentes,
                        options["solo_nuevas"],
                        stats,
                    )
                except Exception as e:
                    stats["errores"] += 1
                    titulo = obra_json.get("titulo") or obra_json.get("Título") or f"(sin título, idx {i})"
                    self.stderr.write(f"  Error en '{titulo}': {e}")

                if (i + 1) % 500 == 0:
                    self.stdout.write(f"  ...{i + 1}/{len(obras_json)} procesadas")

        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS("=== Resumen ==="))
        self.stdout.write(f"  Autores creados:           {stats['autores_creados']}")
        self.stdout.write(f"  Lugares creados:           {stats['lugares_creados']}")
        self.stdout.write(f"  Obras creadas:             {stats['obras_creadas']}")
        self.stdout.write(f"  Obras actualizadas:        {stats['obras_actualizadas']}")
        self.stdout.write(f"  Obras omitidas:            {stats['obras_omitidas']}")
        self.stdout.write(f"  Representaciones creadas:  {stats['representaciones_creadas']}")
        if stats["errores"]:
            self.stdout.write(self.style.ERROR(f"  Errores:                   {stats['errores']}"))
        self.stdout.write("")
        self.stdout.write(f"  Total en DB: {Obra.objects.count()} obras, "
                          f"{Autor.objects.count()} autores, "
                          f"{Lugar.objects.count()} lugares, "
                          f"{Representacion.objects.count()} representaciones")

    def _obtener_o_crear_autor(self, autor_data, cache, stats):
        if not autor_data:
            return None

        if isinstance(autor_data, str):
            nombre = autor_data.strip()
            autor_data = {"nombre": nombre}
        elif isinstance(autor_data, dict):
            nombre = (
                autor_data.get("nombre")
                or autor_data.get("nombre_completo")
                or autor_data.get("Nombre Completo")
                or ""
            ).strip()
        else:
            return None

        if not nombre or nombre.lower() in ("anónimo", "anonimo", "desconocido", ""):
            nombre = "Anónimo"

        clave = nombre.lower().strip()
        if clave in cache:
            return cache[clave]

        obj, created = Autor.objects.get_or_create(
            nombre=nombre,
            defaults={
                "nombre_completo": (autor_data.get("nombre_completo") or "").strip(),
                "fecha_nacimiento": (autor_data.get("fecha_nacimiento") or "").strip(),
                "fecha_muerte": (autor_data.get("fecha_muerte") or "").strip(),
                "biografia": (autor_data.get("biografia") or "").strip(),
                "epoca": (autor_data.get("epoca") or autor_data.get("Época") or "").strip(),
            },
        )
        cache[clave] = obj
        if created:
            stats["autores_creados"] += 1
        return obj

    def _obtener_o_crear_lugar(self, nombre_lugar, region, tipo_lugar, cache, stats):
        nombre_lugar = (nombre_lugar or "").strip()
        region = (region or "").strip()
        tipo_lugar = (tipo_lugar or "").strip().lower()

        if not nombre_lugar:
            return None

        clave = f"{nombre_lugar.lower()}|{region.lower()}"
        if clave in cache:
            return cache[clave]

        tipo_valido = tipo_lugar if tipo_lugar in dict(Lugar.TIPO_LUGAR_CHOICES) else "otro"

        obj, created = Lugar.objects.get_or_create(
            nombre=nombre_lugar.strip().title(),
            region=region,
            defaults={
                "tipo_lugar": tipo_valido,
                "pais": "España",
            },
        )
        cache[clave] = obj
        if created:
            stats["lugares_creados"] += 1
        return obj

    def _importar_obra(self, obra_json, cache_autores, cache_lugares, titulos_existentes, solo_nuevas, stats):
        get = lambda *keys: next(
            (obra_json[k] for k in keys if k in obra_json and obra_json[k] not in (None, "", [])),
            None,
        )

        titulo = get("titulo", "Título", "T?tulo") or ""
        titulo_original = get("titulo_original", "Título Original") or titulo
        titulo_limpio = titulo_original.strip() or titulo.strip()

        if not titulo_limpio:
            stats["errores"] += 1
            return

        if solo_nuevas and titulo_limpio in titulos_existentes:
            stats["obras_omitidas"] += 1
            return

        autor_obj = self._obtener_o_crear_autor(
            get("autor", "Autor"), cache_autores, stats
        )

        tipo_obra_raw = (get("tipo_obra", "Tipo de Obra") or "otro").strip().lower()
        tipos_validos = dict(Obra.TIPO_OBRA_CHOICES)
        tipo_obra = tipo_obra_raw if tipo_obra_raw in tipos_validos else "otro"

        fuente_raw = normalizar_fuente(get("fuente", "Fuente Principal", "Fuente") or "")
        fuentes_validas = dict(Obra.FUENTE_CHOICES)
        fuente = fuente_raw if fuente_raw in fuentes_validas else "CATCOM"

        origen_raw = (get("origen_datos", "Origen de Datos") or "web").strip().lower()
        origenes_validos = dict(Obra.ORIGEN_DATOS_CHOICES)
        origen = origen_raw if origen_raw in origenes_validos else "web"

        defaults = {
            "titulo": titulo.strip(),
            "titulo_alternativo": (get("titulo_alternativo", "Títulos Alternativos") or "").strip(),
            "autor": autor_obj,
            "tipo_obra": tipo_obra,
            "genero": (get("genero", "Género") or "").strip(),
            "subgenero": (get("subgenero", "Subgénero") or "").strip(),
            "fuente_principal": fuente,
            "origen_datos": origen,
            "pagina_pdf": safe_int(get("pagina_pdf", "Página PDF")),
            "texto_original_pdf": (get("texto_original_pdf", "Texto Original del PDF") or "").strip(),
            "tema": (get("tema", "Tema") or "").strip(),
            "musica_conservada": safe_bool(get("musica_conservada", "Música Conservada")),
            "compositor": (get("compositor", "Compositor") or "").strip(),
            "bibliotecas_musica": (get("bibliotecas_musica", "Bibliotecas con Música") or "").strip(),
            "bibliografia_musica": (get("bibliografia_musica", "Bibliografía Musical") or "").strip(),
            "mecenas": (get("mecenas", "Mecenas") or "").strip(),
            "fecha_creacion_estimada": (get("fecha_creacion", "Fecha de Creación", "fecha") or "").strip(),
            "idioma": (get("idioma", "Idioma") or "español").strip(),
            "versos": safe_int(get("versos", "Número de Versos")),
            "actos": safe_int(get("actos", "Número de Actos")),
            "notas": (get("notas", "Notas") or "").strip(),
            "notas_bibliograficas": (get("notas_bibliograficas", "Notas Bibliográficas") or "").strip(),
            "edicion_principe": (get("edicion_principe", "Edición Príncipe") or "").strip(),
            "manuscritos_conocidos": (get("manuscritos_conocidos", "Manuscritos Conocidos") or "").strip(),
            "ediciones_conocidas": (get("ediciones_conocidas", "Ediciones Conocidas") or "").strip(),
            "observaciones": (get("observaciones", "Observaciones") or "").strip(),
        }

        obra_obj, created = Obra.objects.update_or_create(
            titulo_limpio=titulo_limpio,
            defaults=defaults,
        )

        if created:
            stats["obras_creadas"] += 1
        else:
            stats["obras_actualizadas"] += 1

        representaciones = get("representaciones") or []
        if not isinstance(representaciones, list):
            representaciones = []

        if representaciones:
            obra_obj.representaciones.all().delete()

        for rep_json in representaciones:
            if not isinstance(rep_json, dict):
                continue

            lugar_nombre = (rep_json.get("lugar") or "").strip()
            region = (rep_json.get("region") or "").strip()
            tipo_lugar_rep = (rep_json.get("tipo_lugar") or "").strip()

            lugar_obj = self._obtener_o_crear_lugar(
                lugar_nombre, region, tipo_lugar_rep, cache_lugares, stats
            )

            fecha_texto = (rep_json.get("fecha") or "").strip()
            fecha_formateada = parsear_fecha(rep_json.get("fecha_formateada") or "")

            tipo_lugar_val = tipo_lugar_rep.lower() if tipo_lugar_rep else ""
            tipos_validos_rep = dict(Representacion.TIPO_LUGAR_CHOICES)
            tipo_lugar_final = tipo_lugar_val if tipo_lugar_val in tipos_validos_rep else ""

            Representacion.objects.create(
                obra=obra_obj,
                fecha=fecha_texto,
                fecha_formateada=fecha_formateada,
                compañia=(rep_json.get("compania") or "").strip(),
                lugar=lugar_obj,
                tipo_lugar=tipo_lugar_final,
                director_compañia=(rep_json.get("director_compañia") or rep_json.get("director_compania") or "").strip(),
                fuente=(rep_json.get("fuente") or "").strip(),
                observaciones=(rep_json.get("observaciones") or "").strip(),
                mecenas=(rep_json.get("mecenas") or "").strip(),
                gestor_administrativo=(rep_json.get("gestor_administrativo") or "").strip(),
                personajes_historicos=json.dumps(rep_json.get("personajes_historicos") or [], ensure_ascii=False),
                organizadores_fiesta=json.dumps(rep_json.get("organizadores_fiesta") or [], ensure_ascii=False),
                tipo_funcion=(rep_json.get("tipo_funcion") or "").strip(),
                publico=(rep_json.get("publico") or "").strip(),
                entrada=(rep_json.get("entrada") or "").strip(),
                duracion=(rep_json.get("duracion") or "").strip(),
                notas=(rep_json.get("notas") or "").strip(),
                pagina_pdf=safe_int(rep_json.get("pagina_pdf")),
                es_anterior_1650=safe_bool(rep_json.get("es_anterior_1650")),
                es_anterior_1665=safe_bool(rep_json.get("es_anterior_1665")),
            )
            stats["representaciones_creadas"] += 1
