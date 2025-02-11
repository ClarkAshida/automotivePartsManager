from django.test import TestCase
from automotivePartsManager.models import CarModel
from automotivePartsManager.serializers import CarModelSerializer

class CarModelSerializerTest(TestCase):
    """Testes para o serializer CarModelSerializer"""

    def test_valid_data(self):
        """Testa a serialização de dados válidos"""
        data = {
            "name": "Civic",
            "manufacturer": "Honda",
            "year": 2022
        }
        serializer = CarModelSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data["name"], "Civic")
        self.assertEqual(serializer.validated_data["manufacturer"], "Honda")
        self.assertEqual(serializer.validated_data["year"], 2022)

    def test_missing_fields(self):
        """Testa se faltar campos obrigatórios o serializer retorna erro"""
        data = {"name": "Civic"}  # Sem 'manufacturer' e 'year'
        serializer = CarModelSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("manufacturer", serializer.errors)
        self.assertIn("year", serializer.errors)

    def test_invalid_year(self):
        """Testa se um ano inválido gera erro"""
        data = {
            "name": "Civic",
            "manufacturer": "Honda",
            "year": "ano_invalido"  # Deve ser um número
        }
        serializer = CarModelSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("year", serializer.errors)

    def test_serialization(self):
        """Testa se um objeto CarModel é serializado corretamente"""
        car = CarModel.objects.create(name="Corolla", manufacturer="Toyota", year=2023)
        serializer = CarModelSerializer(car)
        data = serializer.data

        self.assertEqual(data["name"], "Corolla")
        self.assertEqual(data["manufacturer"], "Toyota")
        self.assertEqual(data["year"], 2023)
