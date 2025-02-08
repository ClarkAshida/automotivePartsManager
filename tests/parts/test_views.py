from rest_framework import status
from django.urls import reverse
from rest_framework.test import APITestCase
from automotivePartsManager.models import Part, CustomUser
from automotivePartsManager.serializers import PartListSerializer, PartDetailSerializer
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken

class PartAPITests(APITestCase):
    def setUp(self):
        # Criação de dados iniciais para os testes
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
            name="Pastilhas de Freio",
            details="Conjunto de 4 pastilhas",
            price=1009.74,
            quantity=37
        )

        # URL para listagem de peças
        self.url_list = reverse('part-list')
        self.url_detail = reverse('part-detail', args=[self.part1.id])

    # Teste de listagem de peças para usuário comum autenticado (role: 'user')
    def test_list_parts_as_user(self):
        # Gera um token JWT para o usuário comum
        access_token = AccessToken.for_user(self.user)
        # Autentica o cliente de teste com o token JWT
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        # Faz a requisição GET para listar as peças
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        parts = Part.objects.all()
        serializer = PartListSerializer(parts, many=True)
        self.assertEqual(response.data['results'], serializer.data)

    # Teste de listagem de peças sem autenticação (deve retornar erro 401)
    def test_list_parts_unauthenticated(self):
        # Remove qualquer autenticação existente
        self.client.credentials()
        # Faz a requisição GET para listar as peças
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # Teste de listagem de peças para usuário admin autenticado (role: 'admin')
    def test_list_parts_as_admin(self):
        # Gera um token JWT para o usuário admin
        access_token = AccessToken.for_user(self.admin)
        # Autentica o cliente de teste com o token JWT
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        # Faz a requisição GET para listar as peças
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        parts = Part.objects.all()
        serializer = PartListSerializer(parts, many=True)
        self.assertEqual(response.data['results'], serializer.data)