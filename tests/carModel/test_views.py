from rest_framework import status
from django.urls import reverse
from rest_framework.test import APITestCase
from automotivePartsManager.models import CarModel, CustomUser
from automotivePartsManager.serializers import CarModelSerializer
from rest_framework_simplejwt.tokens import AccessToken

# Testes de end points com usuário admin
class CarModelViewTests(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email="user@email.com",
            username="user",
            password="User!123",
            role="user"
        )
        self.admin = CustomUser.objects.create_user(
            email="admin@email.com",
            username="admin",
            password="Admin!123",
            role="admin"
        )
        self.car_model1 = CarModel.objects.create(
            name="Civic",
            manufacturer="Honda",
            year=2022
        )
        self.car_model2 = CarModel.objects.create(
            name="Corolla",
            manufacturer="Toyota",
            year=2021
        )
        self.url = reverse('carmodel-list')
        self.url_detail = reverse('carmodel-detail', args=[self.car_model1.id])

    # Teste de listagem de modelos de carro para usuário admin autenticado (role: 'admin')
    def test_list_car_models_as_admin(self):
        access_token = AccessToken.for_user(self.admin)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        car_models = CarModel.objects.all()
        serializer = CarModelSerializer(car_models, many=True)
        self.assertEqual(response.data['results'], serializer.data)

    # Teste de detalhar um modelo de carro para usuário admin autenticado (role: 'admin')
    def test_retrieve_car_model_as_admin(self):
        access_token = AccessToken.for_user(self.admin)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.get(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = CarModelSerializer(self.car_model1)
        self.assertEqual(response.data, serializer.data)

    # Teste de criação de modelo de carro com usuário admin autenticado (role: 'admin')
    def test_create_car_model_as_admin(self):
        access_token = AccessToken.for_user(self.admin)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        data = {
            'name': 'Fusion',
            'manufacturer': 'Ford',
            'year': 2020
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CarModel.objects.get(name='Fusion').name, 'Fusion')

    # Teste de criação de modelo de carro com dados inválidos (role: 'admin')
    def test_create_car_model_with_invalid_data_as_admin(self):
        access_token = AccessToken.for_user(self.admin)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        data = {
            'name': '',
            'manufacturer': 'Ford',
            'year': 'invalid_year'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(CarModel.objects.count(), 2)

    # Teste de update de modelo de carro com usuário admin autenticado (role: 'admin')
    def test_update_car_model_as_admin(self):
        access_token = AccessToken.for_user(self.admin)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        data = {
            'name': 'Civic Sport',
            'manufacturer': 'Honda',
            'year': 2023
        }
        response = self.client.put(self.url_detail, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.car_model1.refresh_from_db()
        self.assertEqual(self.car_model1.name, 'Civic Sport')
        self.assertEqual(self.car_model1.manufacturer, 'Honda')
        self.assertEqual(self.car_model1.year, 2023)
    
    # Teste de update de modelo de carro com dados inválidos (role: 'admin')
    def test_update_car_model_with_invalid_data_as_admin(self):
        access_token = AccessToken.for_user(self.admin)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        data = {
            'name': '',
            'manufacturer': 'Honda',
            'year': 2023
        }
        response = self.client.put(self.url_detail, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Teste de exclusão de modelo de carro com usuário admin (deve ser bem-sucedido)
    def test_delete_car_model_as_admin(self):
        access_token = AccessToken.for_user(self.admin)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.delete(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(CarModel.objects.filter(id=self.car_model1.id).exists())

    # Teste de filtragem de modelo de carro por 'name' com usuário admin autenticado (role: 'admin')
    def test_filter_car_model_by_name_as_admin(self):
        access_token = AccessToken.for_user(self.admin)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.get(self.url, {'name': 'Corolla'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        car_models = CarModel.objects.filter(name='Corolla')
        serializer = CarModelSerializer(car_models, many=True)
        self.assertEqual(response.data['results'], serializer.data)

    # Teste de filtragem de modelo de carro por 'manufacturer' com usuário admin autenticado (role: 'admin')
    def test_filter_car_model_by_manufacturer_as_admin(self):
        access_token = AccessToken.for_user(self.admin)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.get(self.url, {'manufacturer': 'Toyota'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        car_models = CarModel.objects.filter(manufacturer='Toyota')
        serializer = CarModelSerializer(car_models, many=True)
        self.assertEqual(response.data['results'], serializer.data)

    # Teste de filtragem de modelo de carro por 'year' com usuário admin autenticado (role: 'admin')
    def test_filter_car_model_by_year_as_admin(self):
        access_token = AccessToken.for_user(self.admin)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.get(self.url, {'year': 2022})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        car_models = CarModel.objects.filter(year=2022)
        serializer = CarModelSerializer(car_models, many=True)
        self.assertEqual(response.data['results'], serializer.data)

    # Teste de paginação de modelos de carro com usuário admin autenticado (role: 'admin')
    def test_pagination_car_models_as_admin(self):
        access_token = AccessToken.for_user(self.admin)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)
        self.assertEqual(response.data['next'], None)
        self.assertEqual(response.data['previous'], None)
        self.assertEqual(len(response.data['results']), 2)
