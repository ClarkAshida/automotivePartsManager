from rest_framework import status
from django.urls import reverse
from rest_framework.test import APITestCase
from automotivePartsManager.models import Part, CustomUser
from automotivePartsManager.serializers import PartListSerializer, PartDetailSerializer
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken

# Testes de end points com usuário admin
class PartViewTests(APITestCase):
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
        self.part2 = Part.objects.create(
            part_number="67890",
            name="Bateria",
            details="Bateria de 60Ah",
            price=500.00,
            quantity=15
        )
        self.url = reverse('part-list')
        self.url_detail = reverse('part-detail', args=[self.part1.id])

    # Teste de listagem de peças para usuário admin autenticado (role: 'admin')
    def test_list_parts_as_admin(self):
        access_token = AccessToken.for_user(self.admin)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        parts = Part.objects.all()
        serializer = PartListSerializer(parts, many=True)
        self.assertEqual(response.data['results'], serializer.data)

    # Teste de detalhar peça para usuário admin autenticado (role: 'admin')
    def test_retrieve_part_as_admin(self):
        access_token = AccessToken.for_user(self.admin)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.get(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = PartDetailSerializer(self.part1)
        self.assertEqual(response.data, serializer.data)

    # Teste de criação de peças com usuário admin autenticado (role: 'admin')
    def test_create_part_as_admin(self):
        access_token = AccessToken.for_user(self.admin)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        data = {
            'part_number': '54321',
            'name': 'Amortecedor',
            'details': 'Amortecedor dianteiro',
            'price': 1200.50,
            'quantity': 10
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Part.objects.get(id=3).name, 'Amortecedor')

    # Teste de criação de peças com usuário com dados inválidos (role: 'admin')
    def test_create_part_with_invalid_data_as_admin(self):
        access_token = AccessToken.for_user(self.admin)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        data = {
            'part_number': '',
            'name': '',
            'details': 'Amortecedor dianteiro',
            'price': 1200.50
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Part.objects.count(), 2)

    # Teste de update de peças com usuário admin autenticado (role: 'admin')
    def test_update_part_as_admin(self):
        access_token = AccessToken.for_user(self.admin)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        data = {
            'name': 'Filtro de Óleo Premium',
            'details': 'Filtro de alta qualidade aprimorado',
            'price': 700.00,
            'quantity': 30
        }
        response = self.client.put(self.url_detail, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.part1.refresh_from_db()
        self.assertEqual(self.part1.name, 'Filtro de Óleo Premium')
        self.assertEqual(self.part1.details, 'Filtro de alta qualidade aprimorado')
        self.assertEqual(self.part1.price, 700.00)
        self.assertEqual(self.part1.quantity, 30)

    # Teste de update de peças com usuário com dados inválidos (role: 'admin')
    def test_update_part_with_invalid_data_as_admin(self):
        access_token = AccessToken.for_user(self.admin)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        data = {
            'name': '',
            'details': 'Filtro de alta qualidade aprimorado',
            'price': 700.00,
            'quantity': 30
        }
        response = self.client.put(self.url_detail, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Teste de exclusão de peça com usuário admin (deve ser bem-sucedido)
    def test_delete_part_as_admin(self):
        access_token = AccessToken.for_user(self.admin)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.delete(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Part.objects.filter(id=self.part1.id).exists())

    # Teste de filtragem de peça por 'part_number' com usuário admin autenticado (role: 'admin')
    def test_filter_part_by_part_number_as_admin(self):
        access_token = AccessToken.for_user(self.admin)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.get(self.url, {'part_number': '67890'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        parts = Part.objects.filter(part_number='67890')
        serializer = PartListSerializer(parts, many=True)
        self.assertEqual(response.data['results'], serializer.data)
    
    # Teste de filtragem de peça por 'name' com usuário admin autenticado (role: 'admin')
    def test_filter_part_by_name_as_admin(self):
        access_token = AccessToken.for_user(self.admin)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.get(self.url, {'name': 'Filtro de Óleo'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        parts = Part.objects.filter(name='Filtro de Óleo')
        serializer = PartListSerializer(parts, many=True)
        self.assertEqual(response.data['results'], serializer.data)
    
    # Teste de filtragem de peça por 'price' com usuário admin autenticado (role: 'admin')
    def test_filter_part_by_price_as_admin(self):
        access_token = AccessToken.for_user(self.admin)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.get(self.url, {'price': 652.76})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        parts = Part.objects.filter(price=652.76)
        serializer = PartListSerializer(parts, many=True)
        self.assertEqual(response.data['results'], serializer.data)
    
    # Teste de paginação de peças com usuário admin autenticado (role: 'admin')
    def test_pagination_parts_as_admin(self):
        access_token = AccessToken.for_user(self.admin)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)
        self.assertEqual(response.data['next'], None)
        self.assertEqual(response.data['previous'], None)
        self.assertEqual(len(response.data['results']), 2)