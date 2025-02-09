from rest_framework import status
from django.urls import reverse
from rest_framework.test import APITestCase
from automotivePartsManager.models import Part, CustomUser
from automotivePartsManager.serializers import PartListSerializer
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken

# Teste de end points com usuário comum e usuário não autenticado
class PartViewPermissionsTests(APITestCase):
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
        self.part1 = Part.objects.create(
            part_number="12345",
            name="Filtro de Óleo",
            details="Filtro de alta qualidade",
            price=652.76,
            quantity=32
        )

        self.url = reverse('part-list')
        self.url_detail = reverse('part-detail', args=[self.part1.id])

        # Teste de listagem de peças para usuário comum autenticado (role: 'user')
    def test_list_parts_as_user(self):
        access_token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        parts = Part.objects.all()
        serializer = PartListSerializer(parts, many=True)
        self.assertEqual(response.data['results'], serializer.data)

    # Teste de listagem de peças sem autenticação (deve retornar erro 401)
    def test_list_parts_unauthenticated(self):
        self.client.credentials()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # Teste de criação de peça com usuário comum (deve retornar erro 403)
    def test_create_part_as_user(self):
        access_token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        data = {
            'part_number': '54321',
            'name': 'Amortecedor',
            'details': 'Amortecedor dianteiro',
            'price': 1200.50,
            'quantity': 10
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # Teste de criação de peça sem autenticação (deve retornar erro 401)
    def test_create_part_unauthenticated(self):
        self.client.credentials()
        data = {
            'part_number': '54321',
            'name': 'Amortecedor',
            'details': 'Amortecedor dianteiro',
            'price': 1200.50,
            'quantity': 10
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_update_part_as_user(self):
        access_token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        data = {
            'part_number': '54321',
            'name': 'Amortecedor',
            'details': 'Amortecedor dianteiro',
            'price': 1200.50,
            'quantity': 10
        }
        # Faz a requisição PUT para editar a peça
        response = self.client.put(self.url_detail, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # Teste de edição de peça sem autenticação (deve retornar erro 401)
    def test_update_part_unauthenticated(self):
        self.client.credentials()
        data = {
            'name': 'Filtro de Óleo Premium',
            'details': 'Filtro de alta qualidade aprimorado',
            'price': 700.00,
            'quantity': 30
        }
        response = self.client.put(self.url_detail, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # Teste de exclusão de peça com usuário comum (deve retornar erro 403)
    def test_delete_part_as_user(self):
        access_token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.delete(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Part.objects.filter(id=self.part1.id).exists())

    # Teste de exclusão de peça sem autenticação (deve retornar erro 401)
    def test_delete_part_unauthenticated(self):
        # Remove qualquer autenticação existente
        self.client.credentials()
        response = self.client.delete(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertTrue(Part.objects.filter(id=self.part1.id).exists())
    
    # Teste de filtragem de peça por 'part_number' com usuário comum autenticado (role: 'user')
    def test_filter_part_by_part_number_as_user(self):
        access_token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.get(self.url, {'part_number': '12345'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        parts = Part.objects.filter(part_number='12345')
        serializer = PartListSerializer(parts, many=True)
        self.assertEqual(response.data['results'], serializer.data)
    
    # Teste de filtragem de peça por 'name' com usuário comum autenticado (role: 'user')
    def test_filter_part_by_name_as_user(self):
        access_token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.get(self.url, {'name': 'Filtro de Óleo'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        parts = Part.objects.filter(name='Filtro de Óleo')
        serializer = PartListSerializer(parts, many=True)
        self.assertEqual(response.data['results'], serializer.data)
    
    # Teste de filtragem de peça por 'price' com usuário comum autenticado (role: 'user')
    def test_filter_part_by_price_as_user(self):
        access_token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.get(self.url, {'price': 652.76})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        parts = Part.objects.filter(price=652.76)
        serializer = PartListSerializer(parts, many=True)
        self.assertEqual(response.data['results'], serializer.data)
    
    # Teste de filtragem de peça por 'part_number' sem autenticação (deve retornar erro 401)
    def test_filter_part_by_part_number_unauthenticated(self):
        self.client.credentials()
        response = self.client.get(self.url, {'part_number': '12345'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    # Teste de filtragem de peça por 'name' sem autenticação (deve retornar erro 401)
    def test_filter_part_by_name_unauthenticated(self):
        self.client.credentials()
        response = self.client.get(self.url, {'name': 'Filtro de Óleo'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    # Teste de filtragem de peça por 'price' sem autenticação (deve retornar erro 401)
    def test_filter_part_by_price_unauthenticated(self):
        self.client.credentials()
        response = self.client.get(self.url, {'price': 652.76})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    # Teste de paginação de peças com usuário comum autenticado (role: 'user')
    def test_pagination_parts_as_user(self):
        access_token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['next'], None)
        self.assertEqual(response.data['previous'], None)
        self.assertEqual(len(response.data['results']), 1)
    
    # Teste de paginação de peças sem autenticação (deve retornar erro 401)
    def test_pagination_parts_unauthenticated(self):
        self.client.credentials()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)