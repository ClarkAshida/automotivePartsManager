from django.test import TestCase
from automotivePartsManager.models import Part, CarModel, PartCarModel
from automotivePartsManager.serializers import PartCarModelSerializer

class PartCarModelSerializerTest(TestCase):
    """Testes para o serializer PartCarModelSerializer"""

    def setUp(self):
        """Cria uma peça e um modelo de carro para os testes"""
        self.part = Part.objects.create(
            part_number="XPTO1234",
            name="Filtro de Óleo",
            details="Filtro de alta qualidade",
            price=45.00,
            quantity=50
        )
        self.car_model = CarModel.objects.create(
            name="Civic",
            manufacturer="Honda",
            year=2022
        )
        self.part_car = PartCarModel.objects.create(part=self.part, car_model=self.car_model)

    def test_valid_part_car_model_serialization(self):
        """Testa a serialização de uma relação válida entre peça e modelo de carro"""
        serializer = PartCarModelSerializer(self.part_car)
        data = serializer.data

        self.assertEqual(data["part"]["name"], "Filtro de Óleo")
        self.assertEqual(data["car_model"]["name"], "Civic")

