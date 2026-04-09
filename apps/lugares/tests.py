from django.test import TestCase
from django.db import IntegrityError

from apps.lugares.models import Lugar


class LugarModelTest(TestCase):

    def test_create_lugar(self):
        lugar = Lugar.objects.create(
            nombre="palacio real",
            region="Comunidad de Madrid",
            tipo_lugar="palacio",
        )
        self.assertIn("Palacio Real", str(lugar))
        self.assertEqual(lugar.region, "Comunidad de Madrid")

    def test_save_normalizes_nombre_to_title_case(self):
        lugar = Lugar.objects.create(nombre="buen retiro", tipo_lugar="palacio")
        lugar.refresh_from_db()
        self.assertEqual(lugar.nombre, "Buen Retiro")

    def test_unique_together_nombre_region(self):
        Lugar.objects.create(nombre="Palacio", region="Madrid", tipo_lugar="palacio")
        with self.assertRaises(IntegrityError):
            Lugar.objects.create(nombre="Palacio", region="Madrid", tipo_lugar="palacio")

    def test_different_region_allows_same_nombre(self):
        Lugar.objects.create(nombre="Palacio", region="Madrid", tipo_lugar="palacio")
        lugar2 = Lugar.objects.create(nombre="Palacio", region="Valencia", tipo_lugar="palacio")
        self.assertEqual(lugar2.region, "Valencia")

    def test_total_representaciones_empty(self):
        lugar = Lugar.objects.create(nombre="Teatro", tipo_lugar="teatro")
        self.assertEqual(lugar.total_representaciones, 0)

    def test_coordenadas_none_when_not_set(self):
        lugar = Lugar.objects.create(nombre="Plaza", tipo_lugar="plaza")
        self.assertIsNone(lugar.coordenadas)

    def test_coordenadas_tuple_when_set(self):
        lugar = Lugar.objects.create(
            nombre="Corral",
            tipo_lugar="corral",
            coordenadas_lat=40.4168,
            coordenadas_lng=-3.7038,
        )
        self.assertEqual(lugar.coordenadas, (40.4168, -3.7038))
