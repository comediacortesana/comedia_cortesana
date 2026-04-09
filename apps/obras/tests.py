import json
import tempfile
from pathlib import Path

from django.test import TestCase, Client
from django.core.management import call_command
from django.db import IntegrityError

from apps.autores.models import Autor
from apps.lugares.models import Lugar
from apps.obras.models import Obra, ComentarioUsuario, PropuestaCambioObra
from apps.representaciones.models import Representacion
from apps.usuarios.models import Usuario


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _create_user(username="editor", email="editor@test.com", password="testpass123",
                 is_superuser=False, is_staff=False):
    user = Usuario.objects.create_user(
        username=username, email=email, password=password,
        first_name="Test", last_name="User",
    )
    if is_superuser:
        user.is_superuser = True
    if is_staff:
        user.is_staff = True
    if is_superuser or is_staff:
        user.save()
    return user


def _create_obra(titulo_limpio="La vida es sueño", autor=None, tipo="comedia",
                 fuente="CATCOM"):
    return Obra.objects.create(
        titulo=titulo_limpio,
        titulo_limpio=titulo_limpio,
        tipo_obra=tipo,
        fuente_principal=fuente,
        autor=autor,
    )


SAMPLE_JSON = {
    "metadata": {"version": "1.0", "total_obras": 3},
    "obras": [
        {
            "titulo": "Obra A",
            "titulo_original": "Obra A",
            "tipo_obra": "comedia",
            "fuente": "CATCOM",
            "autor": {"nombre": "Calderón", "epoca": "Siglo de Oro"},
            "representaciones": [
                {
                    "fecha": "9 de enero de 1681",
                    "fecha_formateada": "1681-01-09",
                    "lugar": "Palacio",
                    "tipo_lugar": "palacio",
                    "region": "Comunidad de Madrid",
                    "compania": "Jerónimo García",
                }
            ],
        },
        {
            "titulo": "Obra B",
            "titulo_original": "Obra B",
            "tipo_obra": "auto",
            "fuente": "FUENTESXI",
            "autor": {"nombre": "Lope de Vega"},
        },
        {
            "titulo": "Obra C",
            "titulo_original": "Obra C",
            "tipo_obra": "comedia",
            "fuente": "CATCOM",
            "autor": None,
        },
    ],
}


# ===========================================================================
# 1. Obra model tests
# ===========================================================================

class ObraModelTest(TestCase):

    def test_create_obra(self):
        obra = _create_obra()
        self.assertEqual(str(obra), "La vida es sueño")

    def test_titulo_limpio_unique(self):
        _create_obra(titulo_limpio="Única")
        with self.assertRaises(IntegrityError):
            _create_obra(titulo_limpio="Única")

    def test_autor_fk_set_null_on_delete(self):
        autor = Autor.objects.create(nombre="Calderón")
        obra = _create_obra(autor=autor)
        autor.delete()
        obra.refresh_from_db()
        self.assertIsNone(obra.autor)

    def test_total_representaciones_zero(self):
        obra = _create_obra()
        self.assertEqual(obra.total_representaciones, 0)

    def test_ordering_by_titulo_limpio(self):
        _create_obra(titulo_limpio="Zalamea")
        _create_obra(titulo_limpio="Alcalde")
        titulos = list(Obra.objects.values_list("titulo_limpio", flat=True))
        self.assertEqual(titulos, sorted(titulos))

    def test_primera_ultima_representacion_none(self):
        obra = _create_obra()
        self.assertIsNone(obra.primera_representacion)
        self.assertIsNone(obra.ultima_representacion)

    def test_lugares_representacion_empty(self):
        obra = _create_obra()
        self.assertEqual(obra.lugares_representacion, [])


# ===========================================================================
# 2. /api/datos-obras/ JSON endpoint
# ===========================================================================

class DatosObrasAPITest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_returns_200_no_auth(self):
        resp = self.client.get("/api/datos-obras/")
        self.assertEqual(resp.status_code, 200)

    def test_empty_db_shape(self):
        resp = self.client.get("/api/datos-obras/")
        data = resp.json()
        self.assertIn("metadata", data)
        self.assertIn("obras", data)
        self.assertEqual(data["metadata"]["total_obras"], 0)
        self.assertEqual(data["obras"], [])

    def test_includes_obra_fields(self):
        autor = Autor.objects.create(nombre="Calderón")
        obra = _create_obra(autor=autor)
        resp = self.client.get("/api/datos-obras/")
        data = resp.json()
        self.assertEqual(len(data["obras"]), 1)
        o = data["obras"][0]
        self.assertEqual(o["titulo"], obra.titulo_limpio)
        self.assertEqual(o["tipo_obra"], "comedia")
        self.assertIn("autor", o)
        self.assertEqual(o["autor"]["nombre"], "Calderón")

    def test_includes_representaciones(self):
        obra = _create_obra()
        lugar = Lugar.objects.create(nombre="Palacio", region="Madrid", tipo_lugar="palacio")
        Representacion.objects.create(
            obra=obra, fecha="1681-01-09", lugar=lugar, tipo_lugar="palacio",
        )
        resp = self.client.get("/api/datos-obras/")
        o = resp.json()["obras"][0]
        self.assertEqual(o["total_representaciones"], 1)
        self.assertEqual(len(o["representaciones"]), 1)
        self.assertEqual(o["lugar"], "Palacio")
        self.assertEqual(o["region"], "Madrid")

    def test_metadata_counts(self):
        _create_obra(titulo_limpio="A")
        _create_obra(titulo_limpio="B")
        resp = self.client.get("/api/datos-obras/")
        meta = resp.json()["metadata"]
        self.assertEqual(meta["total_obras"], 2)


# ===========================================================================
# 3. importar_json management command
# ===========================================================================

class ImportarJsonCommandTest(TestCase):

    def _write_fixture(self, data):
        f = tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False, encoding="utf-8"
        )
        json.dump(data, f, ensure_ascii=False)
        f.close()
        return f.name

    def test_import_creates_obras(self):
        path = self._write_fixture(SAMPLE_JSON)
        call_command("importar_json", archivo=path, verbosity=0)
        self.assertEqual(Obra.objects.count(), 3)

    def test_import_creates_autores(self):
        path = self._write_fixture(SAMPLE_JSON)
        call_command("importar_json", archivo=path, verbosity=0)
        self.assertTrue(Autor.objects.filter(nombre="Calderón").exists())
        self.assertTrue(Autor.objects.filter(nombre="Lope de Vega").exists())

    def test_import_creates_representaciones(self):
        path = self._write_fixture(SAMPLE_JSON)
        call_command("importar_json", archivo=path, verbosity=0)
        self.assertEqual(Representacion.objects.count(), 1)

    def test_import_creates_lugares(self):
        path = self._write_fixture(SAMPLE_JSON)
        call_command("importar_json", archivo=path, verbosity=0)
        self.assertTrue(Lugar.objects.filter(nombre__icontains="Palacio").exists())

    def test_limpiar_clears_existing(self):
        _create_obra(titulo_limpio="Preexistente")
        path = self._write_fixture(SAMPLE_JSON)
        call_command("importar_json", archivo=path, limpiar=True, verbosity=0)
        self.assertFalse(Obra.objects.filter(titulo_limpio="Preexistente").exists())
        self.assertEqual(Obra.objects.count(), 3)

    def test_solo_nuevas_skips_existing(self):
        path = self._write_fixture(SAMPLE_JSON)
        call_command("importar_json", archivo=path, verbosity=0)
        count_before = Obra.objects.count()
        call_command("importar_json", archivo=path, solo_nuevas=True, verbosity=0)
        self.assertEqual(Obra.objects.count(), count_before)

    def test_handles_null_autor(self):
        data = {
            "metadata": {},
            "obras": [{"titulo": "X", "titulo_original": "X", "tipo_obra": "comedia",
                        "fuente": "CATCOM", "autor": None}],
        }
        path = self._write_fixture(data)
        call_command("importar_json", archivo=path, verbosity=0)
        obra = Obra.objects.get(titulo_limpio="X")
        if obra.autor:
            self.assertEqual(obra.autor.nombre, "Anónimo")
        else:
            self.assertIsNone(obra.autor)

    def test_handles_missing_fields(self):
        data = {
            "metadata": {},
            "obras": [{"titulo": "Mínima"}],
        }
        path = self._write_fixture(data)
        call_command("importar_json", archivo=path, verbosity=0)
        self.assertTrue(Obra.objects.filter(titulo_limpio="Mínima").exists())


# ===========================================================================
# 4. Comments
# ===========================================================================

class CommentsTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = _create_user()
        cls.admin = _create_user("admin", "admin@test.com", is_superuser=True, is_staff=True)
        cls.obra = _create_obra()

    def _login(self, user):
        self.client.login(username=user.username, password="testpass123")

    def test_create_comment_unauthenticated(self):
        resp = self.client.post(
            f"/obras/{self.obra.id}/comentario/",
            data=json.dumps({"titulo": "Test", "comentario": "Hola", "catalogo": "catcom"}),
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, 401)

    def test_create_and_list_comment(self):
        self._login(self.user)
        resp = self.client.post(
            f"/obras/{self.obra.id}/comentario/",
            data=json.dumps({"titulo": "Nota", "comentario": "Buen dato"}),
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertTrue(data["success"])
        self.assertEqual(ComentarioUsuario.objects.count(), 1)

        resp2 = self.client.get(f"/obras/{self.obra.id}/comentarios/")
        self.assertEqual(resp2.status_code, 200)
        self.assertTrue(resp2.json()["success"])

    def test_delete_own_comment(self):
        self._login(self.user)
        com = ComentarioUsuario.objects.create(
            usuario=self.user, catalogo="catcom",
            titulo="Borrar", comentario="Adiós",
        )
        com.obras_seleccionadas.add(self.obra)
        resp = self.client.post(f"/obras/comentario/{com.id}/eliminar/")
        self.assertEqual(resp.status_code, 200)
        self.assertFalse(ComentarioUsuario.objects.filter(id=com.id).exists())

    def test_delete_others_comment_forbidden(self):
        com = ComentarioUsuario.objects.create(
            usuario=self.admin, catalogo="catcom",
            titulo="Admin", comentario="No borrar",
        )
        self._login(self.user)
        resp = self.client.post(f"/obras/comentario/{com.id}/eliminar/")
        self.assertEqual(resp.status_code, 403)

    def test_export_all_comments(self):
        ComentarioUsuario.objects.create(
            usuario=self.user, catalogo="catcom",
            titulo="Test", comentario="Contenido", es_publico=True,
        )
        resp = self.client.get("/obras/comentarios/exportar-todos/")
        self.assertEqual(resp.status_code, 200)
        self.assertIn("text/plain", resp["Content-Type"])

    def test_export_ia_requires_auth(self):
        resp = self.client.get("/obras/comentarios/exportar-ia/")
        self.assertEqual(resp.status_code, 401)

    def test_export_ia_authenticated(self):
        self._login(self.user)
        resp = self.client.get("/obras/comentarios/exportar-ia/")
        self.assertEqual(resp.status_code, 200)
        self.assertIn("text/plain", resp["Content-Type"])


# ===========================================================================
# 5. Edit proposals
# ===========================================================================

class ProposalTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = _create_user()
        cls.admin = _create_user("admin", "admin@test.com", is_superuser=True, is_staff=True)
        cls.obra = _create_obra()

    def _login(self, user):
        self.client.login(username=user.username, password="testpass123")

    def test_create_proposal_requires_auth(self):
        resp = self.client.post(
            "/obras/propuestas/",
            data=json.dumps({"obra_id": self.obra.id, "campo": "titulo", "valor_nuevo": "Nuevo"}),
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, 401)

    def test_create_proposal_authenticated(self):
        self._login(self.user)
        resp = self.client.post(
            "/obras/propuestas/",
            data=json.dumps({"obra_id": self.obra.id, "campo": "titulo",
                             "valor_anterior": "Viejo", "valor_nuevo": "Nuevo"}),
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertTrue(data["success"])
        self.assertEqual(PropuestaCambioObra.objects.count(), 1)

    def test_list_proposals_for_obra(self):
        self._login(self.user)
        PropuestaCambioObra.objects.create(
            obra=self.obra, campo="titulo",
            valor_anterior="A", valor_nuevo="B",
            propuesta_por=self.user,
        )
        resp = self.client.get(f"/obras/propuestas/obra/{self.obra.id}/")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertTrue(data["success"])
        self.assertEqual(len(data["propuestas"]), 1)

    def test_vote_on_proposal(self):
        self._login(self.user)
        prop = PropuestaCambioObra.objects.create(
            obra=self.obra, campo="titulo",
            valor_anterior="A", valor_nuevo="B",
            propuesta_por=self.admin,
        )
        resp = self.client.post(
            f"/obras/propuestas/{prop.id}/votar/",
            data=json.dumps({"voto": "a_favor", "comentario": "De acuerdo"}),
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.json()["success"])

    def test_resolve_proposal_non_superuser_forbidden(self):
        prop = PropuestaCambioObra.objects.create(
            obra=self.obra, campo="titulo",
            valor_anterior="A", valor_nuevo="B",
            propuesta_por=self.user,
        )
        self._login(self.user)
        resp = self.client.post(
            f"/obras/propuestas/{prop.id}/resolver/",
            data=json.dumps({"accion": "aprobar"}),
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, 403)

    def test_resolve_proposal_as_admin(self):
        prop = PropuestaCambioObra.objects.create(
            obra=self.obra, campo="titulo",
            valor_anterior="A", valor_nuevo="B",
            propuesta_por=self.user,
        )
        self._login(self.admin)
        resp = self.client.post(
            f"/obras/propuestas/{prop.id}/resolver/",
            data=json.dumps({"accion": "aprobar"}),
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.json()["success"])
        prop.refresh_from_db()
        self.assertEqual(prop.estado, "aprobada_superuser")

    def test_reject_proposal_as_admin(self):
        prop = PropuestaCambioObra.objects.create(
            obra=self.obra, campo="titulo",
            valor_anterior="A", valor_nuevo="B",
            propuesta_por=self.user,
        )
        self._login(self.admin)
        resp = self.client.post(
            f"/obras/propuestas/{prop.id}/resolver/",
            data=json.dumps({"accion": "rechazar"}),
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, 200)
        prop.refresh_from_db()
        self.assertEqual(prop.estado, "rechazada")
