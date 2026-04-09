from datetime import date

from django.test import TestCase

from apps.autores.models import Autor
from apps.lugares.models import Lugar
from apps.obras.models import Obra
from apps.representaciones.models import Representacion


class RepresentacionModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.autor = Autor.objects.create(nombre="Calderón")
        cls.obra = Obra.objects.create(
            titulo="La vida es sueño",
            titulo_limpio="La vida es sueño",
            tipo_obra="comedia",
            fuente_principal="CATCOM",
            autor=cls.autor,
        )
        cls.lugar = Lugar.objects.create(
            nombre="Palacio Real",
            region="Comunidad de Madrid",
            tipo_lugar="palacio",
        )

    def test_create_representacion(self):
        rep = Representacion.objects.create(
            obra=self.obra,
            fecha="15/03/1635",
            lugar=self.lugar,
            tipo_lugar="palacio",
        )
        self.assertIn("La vida es sueño", str(rep))

    def test_auto_parse_fecha_dd_mm_yyyy(self):
        rep = Representacion.objects.create(
            obra=self.obra,
            fecha="15/03/1635",
        )
        self.assertEqual(rep.fecha_formateada, date(1635, 3, 15))

    def test_auto_parse_fecha_iso(self):
        rep = Representacion.objects.create(
            obra=self.obra,
            fecha="1681-01-09",
        )
        self.assertEqual(rep.fecha_formateada, date(1681, 1, 9))

    def test_unparseable_fecha_leaves_formateada_none(self):
        rep = Representacion.objects.create(
            obra=self.obra,
            fecha="9 de enero de 1681",
        )
        self.assertIsNone(rep.fecha_formateada)

    def test_es_anterior_1650_true(self):
        rep = Representacion.objects.create(
            obra=self.obra,
            fecha="01/01/1640",
        )
        self.assertTrue(rep.es_anterior_1650)
        self.assertTrue(rep.es_anterior_1665)

    def test_es_anterior_1650_false(self):
        rep = Representacion.objects.create(
            obra=self.obra,
            fecha="01/01/1670",
        )
        self.assertFalse(rep.es_anterior_1650)
        self.assertFalse(rep.es_anterior_1665)

    def test_es_anterior_1665_boundary(self):
        rep = Representacion.objects.create(
            obra=self.obra,
            fecha="01/01/1660",
        )
        self.assertFalse(rep.es_anterior_1650)
        self.assertTrue(rep.es_anterior_1665)

    def test_siglo_property(self):
        rep = Representacion.objects.create(obra=self.obra, fecha="01/01/1650")
        self.assertEqual(rep.siglo, "XVII")

    def test_decada_property(self):
        rep = Representacion.objects.create(obra=self.obra, fecha="01/01/1685")
        self.assertEqual(rep.decada, "1680s")

    def test_obra_total_representaciones(self):
        Representacion.objects.create(obra=self.obra, fecha="01/01/1680")
        Representacion.objects.create(obra=self.obra, fecha="02/02/1681")
        self.assertEqual(self.obra.total_representaciones, 2)
