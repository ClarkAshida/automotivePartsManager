from rest_framework import status
from django.urls import reverse
from rest_framework.test import APITestCase
from automotivePartsManager.models import CarModel, CustomUser
from automotivePartsManager.serializers import CarModelSerializer
from rest_framework_simplejwt.tokens import AccessToken

# Teste de permissões nos endpoints de CarModel com usuário comum e não autenticado
class CarModelViewPermissionsTests(APITestCase):
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

        self.url = reverse('carmodel-list')
        self.url_detail = reverse('carmodel-detail', args=[self.car_model1.id])

    # Teste de listagem de modelos de carro para usuário comum autenticado (role: 'user')
    def test_list_car_models_as_user(self):
        access_token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        car_models = CarModel.objects.all()
        serializer = CarModelSerializer(car_models, many=True)
        self.assertEqual(response.data['results'], serializer.data)

    # Teste de listagem de modelos de carro sem autenticação (deve retornar erro 401)
    def test_list_car_models_unauthenticated(self):
        self.client.credentials()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # Teste de criação de modelo de carro com usuário comum (deve retornar erro 403)
    def test_create_car_model_as_user(self):
        access_token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        data = {
            'name': 'Fusion',
            'manufacturer': 'Ford',
            'year': 2020
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # Teste de criação de modelo de carro sem autenticação (deve retornar erro 401)
    def test_create_car_model_unauthenticated(self):
        self.client.credentials()
        data = {
            'name': 'Fusion',
            'manufacturer': 'Ford',
            'year': 2020
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # Teste de edição de modelo de carro com usuário comum (deve retornar erro 403)
    def test_update_car_model_as_user(self):
        access_token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        data = {
            'name': 'Civic Sport',
            'manufacturer': 'Honda',
            'year': 2023
        }
        response = self.client.put(self.url_detail, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # Teste de edição de modelo de carro sem autenticação (deve retornar erro 401)
    def test_update_car_model_unauthenticated(self):
        self.client.credentials()
        data = {
            'name': 'Civic Sport',
            'manufacturer': 'Honda',
            'year': 2023
        }
        response = self.client.put(self.url_detail, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # Teste de exclusão de modelo de carro com usuário comum (deve retornar erro 403)
    def test_delete_car_model_as_user(self):
        access_token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.delete(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(CarModel.objects.filter(id=self.car_model1.id).exists())

    # Teste de exclusão de modelo de carro sem autenticação (deve retornar erro 401)
    def test_delete_car_model_unauthenticated(self):
        self.client.credentials()
        response = self.client.delete(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertTrue(CarModel.objects.filter(id=self.car_model1.id).exists())

    # Teste de filtragem de modelo de carro por 'name' com usuário comum autenticado (role: 'user')
    def test_filter_car_model_by_name_as_user(self):
        access_token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.get(self.url, {'name': 'Civic'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        car_models = CarModel.objects.filter(name='Civic')
        serializer = CarModelSerializer(car_models, many=True)
        self.assertEqual(response.data['results'], serializer.data)

    # Teste de filtragem de modelo de carro por 'manufacturer' com usuário comum autenticado (role: 'user')
    def test_filter_car_model_by_manufacturer_as_user(self):
        access_token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.get(self.url, {'manufacturer': 'Honda'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        car_models = CarModel.objects.filter(manufacturer='Honda')
        serializer = CarModelSerializer(car_models, many=True)
        self.assertEqual(response.data['results'], serializer.data)

    # Teste de filtragem de modelo de carro por 'year' com usuário comum autenticado (role: 'user')
    def test_filter_car_model_by_year_as_user(self):
        access_token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.get(self.url, {'year': 2022})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        car_models = CarModel.objects.filter(year=2022)
        serializer = CarModelSerializer(car_models, many=True)
        self.assertEqual(response.data['results'], serializer.data)

    # Teste de filtragem de modelo de carro por 'name' sem autenticação (deve retornar erro 401)
    def test_filter_car_model_by_name_unauthenticated(self):
        self.client.credentials()
        response = self.client.get(self.url, {'name': 'Civic'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # Teste de filtragem de modelo de carro por 'manufacturer' sem autenticação (deve retornar erro 401)
    def test_filter_car_model_by_manufacturer_unauthenticated(self):
        self.client.credentials()
        response = self.client.get(self.url, {'manufacturer': 'Honda'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # Teste de filtragem de modelo de carro por 'year' sem autenticação (deve retornar erro 401)
    def test_filter_car_model_by_year_unauthenticated(self):
        self.client.credentials()
        response = self.client.get(self.url, {'year': 2022})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # Teste de paginação de modelos de carro com usuário comum autenticado (role: 'user')
    def test_pagination_car_models_as_user(self):
        access_token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['next'], None)
        self.assertEqual(response.data['previous'], None)
        self.assertEqual(len(response.data['results']), 1)

    # Teste de paginação de modelos de carro sem autenticação (deve retornar erro 401)
    def test_pagination_car_models_unauthenticated(self):
        self.client.credentials()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
