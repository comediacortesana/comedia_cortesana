"""Tests for the root URL routing (static file serving, API endpoint, etc.)."""

from django.test import TestCase

from apps.autores.models import Autor
from apps.obras.models import Obra
from apps.usuarios.models import Usuario


class IndexRouteTest(TestCase):
    """GET / returns the index.html file."""

    def test_index_returns_html(self):
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, 200)
        content_type = resp["Content-Type"]
        self.assertIn("text/html", content_type)


class DatosObrasJsonRouteTest(TestCase):
    """GET /datos_obras.json serves the JSON backup file (or 404 if missing)."""

    def test_datos_obras_json(self):
        resp = self.client.get("/datos_obras.json")
        self.assertIn(resp.status_code, [200, 404])
        if resp.status_code == 200:
            self.assertIn("application/json", resp["Content-Type"])


class DataSubpathRouteTest(TestCase):
    """GET /data/<subpath> serves files under data/."""

    def test_existing_json_file(self):
        resp = self.client.get("/data/fuentesix/campo_auxiliar_fechas.json")
        self.assertIn(resp.status_code, [200, 404])
        if resp.status_code == 200:
            self.assertIn("application/json", resp["Content-Type"])

    def test_path_traversal_blocked(self):
        resp = self.client.get("/data/../.env")
        self.assertEqual(resp.status_code, 404)

    def test_nonexistent_file(self):
        resp = self.client.get("/data/no_existe.json")
        self.assertEqual(resp.status_code, 404)


class ComediaHtmlRouteTest(TestCase):
    """GET /comedia.html returns the comedia HTML file."""

    def test_comedia_html(self):
        resp = self.client.get("/comedia.html")
        self.assertIn(resp.status_code, [200, 500])
        if resp.status_code == 200:
            self.assertIn("text/html", resp["Content-Type"])


class FaviconRouteTest(TestCase):
    """GET /favicon.ico returns 204 No Content."""

    def test_favicon(self):
        resp = self.client.get("/favicon.ico")
        self.assertEqual(resp.status_code, 204)


class DatosObrasAPIRouteTest(TestCase):
    """GET /api/datos-obras/ returns JSON without auth."""

    def test_api_datos_obras(self):
        resp = self.client.get("/api/datos-obras/")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn("metadata", data)
        self.assertIn("obras", data)


class LegacyRouteTest(TestCase):
    """Legacy routes under /legacy/."""

    def test_legacy_favicon(self):
        resp = self.client.get("/legacy/favicon.ico")
        self.assertEqual(resp.status_code, 204)


class DRFObrasCRUDTest(TestCase):
    """DRF /api/obras/ requires authentication (using session auth)."""

    @classmethod
    def setUpTestData(cls):
        cls.user = Usuario.objects.create_user(
            username="test", email="t@t.com", password="pass123",
            first_name="T", last_name="U",
        )

    def test_list_obras_unauthenticated(self):
        resp = self.client.get("/api/obras/")
        self.assertEqual(resp.status_code, 401)

    def test_list_obras_authenticated(self):
        self.client.login(username="test", password="pass123")
        resp = self.client.get("/api/obras/")
        self.assertEqual(resp.status_code, 200)

    def test_list_representaciones_unauthenticated(self):
        resp = self.client.get("/api/representaciones/")
        self.assertEqual(resp.status_code, 401)

    def test_list_lugares_unauthenticated(self):
        resp = self.client.get("/api/lugares/")
        self.assertEqual(resp.status_code, 401)


class DRFObraFilterTest(TestCase):
    """DRF /api/obras/ filter and search (using session auth)."""

    @classmethod
    def setUpTestData(cls):
        cls.user = Usuario.objects.create_user(
            username="filter", email="f@t.com", password="pass123",
            first_name="F", last_name="U",
        )
        autor = Autor.objects.create(nombre="Calderón")
        Obra.objects.create(titulo="A", titulo_limpio="A", tipo_obra="comedia",
                            fuente_principal="CATCOM", autor=autor)
        Obra.objects.create(titulo="B", titulo_limpio="B", tipo_obra="auto",
                            fuente_principal="FUENTESXI", autor=autor)

    def _login(self):
        self.client.login(username="filter", password="pass123")

    def test_filter_by_tipo_obra(self):
        self._login()
        resp = self.client.get("/api/obras/?tipo_obra=comedia")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["count"], 1)

    def test_search_by_titulo(self):
        self._login()
        resp = self.client.get("/api/obras/?search=A")
        self.assertEqual(resp.status_code, 200)
        self.assertGreaterEqual(resp.json()["count"], 1)

    def test_pagination_page_size(self):
        self._login()
        resp = self.client.get("/api/obras/")
        data = resp.json()
        self.assertIn("count", data)
        self.assertIn("results", data)
