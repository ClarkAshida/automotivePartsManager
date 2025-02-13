from django.test import TestCase
from automotivePartsManager.models import CarModel

class CarModelTest(TestCase):
    """Testes para o modelo CarModel"""

    def test_create_car_model(self):
        """Testa a criação de um modelo de carro"""
        car = CarModel.objects.create(
            name="Civic",
            manufacturer="Honda",
            year=2022
        )
        self.assertEqual(car.name, "Civic")
        self.assertEqual(car.manufacturer, "Honda")
        self.assertEqual(car.year, 2022)

    def test_car_model_string_representation(self):
        """Testa a representação em string do modelo CarModel"""
        car = CarModel.objects.create(
            name="Corolla",
            manufacturer="Toyota",
            year=2023
        )
        self.assertEqual(str(car), "Toyota Corolla (2023)")

    def test_car_model_blank_fields(self):
        """Testa se tentar criar um CarModel sem dados obrigatórios gera erro"""
        with self.assertRaises(Exception):
            CarModel.objects.create(name=None, manufacturer="Honda", year=2022)

        with self.assertRaises(Exception):
            CarModel.objects.create(name="Civic", manufacturer=None, year=2022)

        with self.assertRaises(Exception):
            CarModel.objects.create(name="Civic", manufacturer="Honda", year=None)
