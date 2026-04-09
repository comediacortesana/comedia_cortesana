import json

from django.test import TestCase

from apps.autores.models import Autor
from apps.usuarios.models import Usuario


# ===========================================================================
# Autor Model Tests
# ===========================================================================

class AutorModelTest(TestCase):

    def test_create_autor(self):
        autor = Autor.objects.create(nombre="Calderón", epoca="Siglo de Oro")
        self.assertEqual(str(autor), "Calderón")
        self.assertEqual(autor.epoca, "Siglo de Oro")

    def test_total_obras_empty(self):
        autor = Autor.objects.create(nombre="Lope de Vega")
        self.assertEqual(autor.total_obras, 0)

    def test_nombre_completo(self):
        autor = Autor.objects.create(
            nombre="Calderón",
            nombre_completo="Pedro Calderón de la Barca",
            fecha_nacimiento="1600",
            fecha_muerte="1681",
        )
        self.assertEqual(autor.nombre_completo, "Pedro Calderón de la Barca")

    def test_ordering_by_nombre(self):
        Autor.objects.create(nombre="Zorrilla")
        Autor.objects.create(nombre="Calderón")
        Autor.objects.create(nombre="Lope")
        nombres = list(Autor.objects.values_list("nombre", flat=True))
        self.assertEqual(nombres, sorted(nombres))


# ===========================================================================
# Autor DRF CRUD Tests (/api/autores/) -- using session auth
# ===========================================================================

class AutorDRFCRUDTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = Usuario.objects.create_user(
            username="editor", email="editor@test.com",
            password="testpass123", first_name="E", last_name="D",
        )

    def _login(self):
        self.client.login(username="editor", password="testpass123")

    def test_list_requires_auth(self):
        resp = self.client.get("/api/autores/")
        self.assertEqual(resp.status_code, 401)

    def test_list_autores(self):
        Autor.objects.create(nombre="Calderón", epoca="Siglo de Oro")
        Autor.objects.create(nombre="Lope de Vega")
        self._login()
        resp = self.client.get("/api/autores/")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn("results", data)
        self.assertEqual(data["count"], 2)

    def test_filter_by_epoca(self):
        Autor.objects.create(nombre="Calderón", epoca="Siglo de Oro")
        Autor.objects.create(nombre="Otro", epoca="Moderno")
        self._login()
        resp = self.client.get("/api/autores/?epoca=Siglo+de+Oro")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["count"], 1)

    def test_search_by_nombre(self):
        Autor.objects.create(nombre="Calderón de la Barca")
        Autor.objects.create(nombre="Lope de Vega")
        self._login()
        resp = self.client.get("/api/autores/?search=Calderón")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["count"], 1)

    def test_create_autor(self):
        self._login()
        resp = self.client.post(
            "/api/autores/",
            data=json.dumps({"nombre": "Tirso de Molina", "epoca": "Siglo de Oro"}),
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, 201)
        self.assertTrue(Autor.objects.filter(nombre="Tirso de Molina").exists())

    def test_pagination(self):
        for i in range(25):
            Autor.objects.create(nombre=f"Autor {i:02d}")
        self._login()
        resp = self.client.get("/api/autores/")
        data = resp.json()
        self.assertEqual(len(data["results"]), 20)
        self.assertIsNotNone(data["next"])
