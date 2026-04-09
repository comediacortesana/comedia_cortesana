"""
Management command para publicar datos_obras.json en GitHub via Contents API.

Flujo:
    1. Ejecuta exportar_json para generar el JSON fresco
    2. Sube el archivo al repo via GitHub Contents API (PUT)
    3. Opcionalmente sube también a frontend/github-pages/datos_obras.json

Requisitos (variables de entorno):
    GITHUB_TOKEN   -- Personal Access Token con scope "repo"
    GITHUB_REPO    -- owner/repo  (ej: ivansimo/comedia_cortesana)
    GITHUB_BRANCH  -- rama destino (default: main)

Uso:
    python manage.py publicar_github
    python manage.py publicar_github --solo-exportar   # genera JSON sin subir
    python manage.py publicar_github --mensaje "v2.1"  # commit message personalizado
"""

import base64
import json
from datetime import datetime
from pathlib import Path

import requests
from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError


GITHUB_API = "https://api.github.com"


def _get_env(name, default=None):
    """Lee config de settings (decouple) o falla con mensaje claro."""
    from decouple import config as decouple_config, UndefinedValueError
    try:
        return decouple_config(name, default=default)
    except UndefinedValueError:
        if default is not None:
            return default
        raise


def _github_headers(token):
    return {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }


def _upload_file(token, repo, branch, repo_path, local_path, message):
    """Sube (crea o actualiza) un archivo en GitHub via Contents API."""
    url = f"{GITHUB_API}/repos/{repo}/contents/{repo_path}"
    headers = _github_headers(token)

    current_sha = None
    resp = requests.get(url, headers=headers, params={"ref": branch}, timeout=30)
    if resp.status_code == 200:
        current_sha = resp.json().get("sha")

    content_bytes = Path(local_path).read_bytes()
    payload = {
        "message": message,
        "content": base64.b64encode(content_bytes).decode("ascii"),
        "branch": branch,
    }
    if current_sha:
        payload["sha"] = current_sha

    resp = requests.put(url, headers=headers, json=payload, timeout=60)
    if resp.status_code not in (200, 201):
        raise CommandError(
            f"GitHub API error {resp.status_code} al subir {repo_path}: {resp.text[:500]}"
        )
    return resp.json()


class Command(BaseCommand):
    help = "Exporta datos_obras.json y lo publica en GitHub"

    def add_arguments(self, parser):
        parser.add_argument(
            "--solo-exportar",
            action="store_true",
            help="Solo genera el JSON local sin subirlo a GitHub",
        )
        parser.add_argument(
            "--mensaje",
            default="",
            help="Mensaje de commit personalizado",
        )
        parser.add_argument(
            "--tambien-frontend",
            action="store_true",
            default=True,
            help="También subir frontend/github-pages/datos_obras.json (default: True)",
        )

    def handle(self, *args, **options):
        json_path = settings.BASE_DIR / "datos_obras.json"

        self.stdout.write("Paso 1: Exportando JSON desde la DB...")
        call_command("exportar_json", salida=str(json_path), tambien_frontend=True)

        if options["solo_exportar"]:
            self.stdout.write(self.style.SUCCESS("JSON generado (sin subir a GitHub)."))
            return

        token = _get_env("GITHUB_TOKEN", default="")
        repo = _get_env("GITHUB_REPO", default="")
        branch = _get_env("GITHUB_BRANCH", default="main")

        if not token or not repo:
            raise CommandError(
                "Faltan variables de entorno GITHUB_TOKEN y/o GITHUB_REPO. "
                "Configúralas en .env o en App Service > Configuration."
            )

        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        n_obras = data.get("metadata", {}).get("total_obras", "?")

        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        if options["mensaje"]:
            commit_msg = options["mensaje"]
        else:
            commit_msg = f"Actualizar datos_obras.json ({n_obras} obras) - {now}"

        self.stdout.write(f"Paso 2: Subiendo a {repo} (rama {branch})...")

        _upload_file(token, repo, branch, "datos_obras.json", json_path, commit_msg)
        self.stdout.write(self.style.SUCCESS("  datos_obras.json subido."))

        if options["tambien_frontend"]:
            frontend_path = settings.BASE_DIR / "frontend" / "github-pages" / "datos_obras.json"
            if frontend_path.exists():
                _upload_file(
                    token, repo, branch,
                    "frontend/github-pages/datos_obras.json",
                    frontend_path,
                    commit_msg,
                )
                self.stdout.write(self.style.SUCCESS(
                    "  frontend/github-pages/datos_obras.json subido."
                ))

        self.stdout.write(self.style.SUCCESS(
            f"\nPublicación completada: {n_obras} obras -> github.com/{repo}"
        ))
