import unittest
from django.db.utils import IntegrityError
from django.test import TestCase
from automotivePartsManager.models import Part, CarModel, PartCarModel

class PartCarModelTest(TestCase):
    """Testes para o modelo PartCarModel"""

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

    def test_create_part_car_model(self):
        """Testa a criação de uma relação entre peça e modelo de carro"""
        part_car = PartCarModel.objects.create(part=self.part, car_model=self.car_model)
        self.assertEqual(part_car.part, self.part)
        self.assertEqual(part_car.car_model, self.car_model)

    def test_part_car_model_unique_constraint(self):
        """Testa a restrição de unicidade entre peça e modelo de carro"""
        PartCarModel.objects.create(part=self.part, car_model=self.car_model)
        
        with self.assertRaises(IntegrityError):  # Deve falhar ao tentar criar um registro duplicado
            PartCarModel.objects.create(part=self.part, car_model=self.car_model)

    def test_part_car_model_string_representation(self):
        """Testa a representação em string do modelo PartCarModel"""
        part_car = PartCarModel.objects.create(part=self.part, car_model=self.car_model)
        self.assertEqual(str(part_car), "Filtro de Óleo - Civic")
