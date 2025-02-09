from rest_framework import status
from django.urls import reverse
from rest_framework.test import APITestCase
from automotivePartsManager.models import CarModel, Part, CustomUser, PartCarModel
from automotivePartsManager.serializers import PartListSerializer
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
            name="Pastilhas de Freio",
            details="Conjunto de 4 pastilhas",
            price=1009.74,
            quantity=37
        )
        self.car_model1 = CarModel.objects.create(
            name="Civic",
            manufacturer="Honda",
            year=2020
        )
        self.car_model2 = CarModel.objects.create(
            name="Corolla",
            manufacturer="Toyota",
            year=2020
        )

        self.url_list = reverse('part-list')
        self.url_detail = reverse('part-detail', args=[self.part1.id])
        self.url_create = reverse('part-list')

    # Teste de listagem de peças para usuário admin autenticado (role: 'admin')
    def test_list_parts_as_admin(self):
        access_token = AccessToken.for_user(self.admin)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        parts = Part.objects.all()
        serializer = PartListSerializer(parts, many=True)
        self.assertEqual(response.data['results'], serializer.data)

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
        response = self.client.post(self.url_create, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Part.objects.get(id=3).name, 'Amortecedor')

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

    # Teste de exclusão de peça com usuário admin (deve ser bem-sucedido)
    def test_delete_part_as_admin(self):
        access_token = AccessToken.for_user(self.admin)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.delete(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Part.objects.filter(id=self.part1.id).exists())

    # Teste de usuário admin associar peça e carro com sucesso
    def test_admin_associate_parts_to_car_models(self):
        access_token = AccessToken.for_user(self.admin)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        
        data = {
            'part_ids': [self.part1.id],
            'car_model_ids': [self.car_model1.id]
        }

        response = self.client.post(reverse('associate-parts-to-car-models'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(PartCarModel.objects.filter(part=self.part1, car_model=self.car_model1).exists())

    # Teste de usuário admin visualizar associações de peças e carros
    def test_admin_can_view_associations(self):
        access_token = AccessToken.for_user(self.admin)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        
        response = self.client.get(reverse('partcarmodel-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    # Teste de usuário admin dessassociar peças e carros
    def test_admin_can_delete_association(self):
        association = PartCarModel.objects.create(part=self.part1, car_model=self.car_model1)
        access_token = AccessToken.for_user(self.admin)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        
        response = self.client.delete(reverse('partcarmodel-detail', args=[association.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(PartCarModel.objects.filter(id=association.id).exists())

    # Teste de usuário admin conseguir ver carros associados a uma peça específica
    def test_admin_can_view_car_models_by_part(self):
        PartCarModel.objects.create(part=self.part1, car_model=self.car_model1)
        access_token = AccessToken.for_user(self.admin)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        
        response = self.client.get(reverse('get-car-models-by-part') + f'?part_id={self.part1.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Teste de usuário admin conseguir ver peças associadas a um carro específico
    def test_admin_can_view_parts_by_car_model(self):
        PartCarModel.objects.create(part=self.part1, car_model=self.car_model1)
        access_token = AccessToken.for_user(self.admin)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        
        response = self.client.get(reverse('get-parts-by-car-model') + f'?car_model_id={self.car_model1.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    