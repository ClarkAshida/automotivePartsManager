import unittest
from django.test import TestCase
from automotivePartsManager.models import Part, CarModel, PartCarModel
from automotivePartsManager.serializers import PartListSerializer, PartDetailSerializer

class PartListSerializerTest(TestCase):
    """Testes para o serializer PartListSerializer"""

    def test_valid_data(self):
        """Testa a serialização de dados válidos"""
        data = {
            "name": "Filtro de Óleo",
            "details": "Filtro de alta qualidade",
            "price": 45.00,
            "quantity": 10
        }
        serializer = PartListSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_price(self):
        """Testa a validação de preço negativo"""
        data = {
            "name": "Filtro de Óleo",
            "details": "Filtro de alta qualidade",
            "price": -10.00,  # Preço inválido
            "quantity": 10
        }
        serializer = PartListSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("O preço deve ser maior que zero.", serializer.errors["price"])

    def test_invalid_quantity(self):
        """Testa a validação de quantidade negativa"""
        data = {
            "name": "Filtro de Óleo",
            "details": "Filtro de alta qualidade",
            "price": 45.00,
            "quantity": -5  # Quantidade inválida
        }
        serializer = PartListSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("A quantidade não pode ser negativa.", serializer.errors["quantity"])

class PartDetailSerializerTest(TestCase):
    """Testes para o serializer PartDetailSerializer"""

    def setUp(self):
        """Cria um objeto Part e CarModel para os testes"""
        self.part = Part.objects.create(
            part_number="XPTO1234",
            name="Filtro de Óleo",
            details="Filtro de alta qualidade",
            price=45.00,
            quantity=10
        )
        self.car_model = CarModel.objects.create(
            name="Civic", manufacturer="Honda", year=2022
        )
        PartCarModel.objects.create(part=self.part, car_model=self.car_model)

    def test_part_detail_serializer(self):
        """Testa a serialização de um objeto Part com relação a CarModel"""
        serializer = PartDetailSerializer(self.part)
        data = serializer.data

        self.assertEqual(data["part_number"], "XPTO1234")
        self.assertEqual(data["name"], "Filtro de Óleo")
        self.assertEqual(data["price"], "45.00")
        self.assertEqual(data["quantity"], 10)
