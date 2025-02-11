import unittest
from django.test import TestCase
from automotivePartsManager.models import Part

class PartModelTest(TestCase):
    """Testes para o modelo Part"""

    def test_create_part(self):
        """Testa a criação de uma peça"""
        part = Part.objects.create(
            part_number="XPTO1234",
            name="Filtro de Óleo",
            details="Filtro de alta qualidade",
            price=45.00,
            quantity=50
        )
        self.assertEqual(part.part_number, "XPTO1234")
        self.assertEqual(part.name, "Filtro de Óleo")
        self.assertEqual(part.price, 45.00)
        self.assertEqual(part.quantity, 50)

    def test_part_string_representation(self):
        """Testa a representação em string do modelo Part"""
        part = Part.objects.create(
            part_number="ABC123",
            name="Pastilha de Freio",
            details="Conjunto de 4 pastilhas",
            price=120.00,
            quantity=30
        )
        self.assertEqual(str(part), "Pastilha de Freio (ABC123)")

    def test_default_quantity(self):
        """Testa se a quantidade padrão é 0 quando não especificada"""
        part = Part.objects.create(
            part_number="XYZ789",
            name="Óleo de Motor",
            details="Óleo sintético 5W30",
            price=80.00
        )
        self.assertEqual(part.quantity, 0)
