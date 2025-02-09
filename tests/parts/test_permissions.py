from rest_framework import status
from django.urls import reverse
from rest_framework.test import APITestCase
from automotivePartsManager.models import CarModel, Part, CustomUser, PartCarModel
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

        # Teste de listagem de peças para usuário comum autenticado (role: 'user')
    def test_list_parts_as_user(self):
        access_token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        parts = Part.objects.all()
        serializer = PartListSerializer(parts, many=True)
        self.assertEqual(response.data['results'], serializer.data)

    # Teste de listagem de peças sem autenticação (deve retornar erro 401)
    def test_list_parts_unauthenticated(self):
        self.client.credentials()
        response = self.client.get(self.url_list)
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
        response = self.client.post(self.url_create, data, format='json')
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
        response = self.client.post(self.url_create, data, format='json')
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

    # Teste de usuário comum não conseguir associar peça e carro
    def test_user_cannot_associate_parts_to_car_models(self):
        access_token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        
        data = {
            'part_ids': [self.part1.id],
            'car_model_ids': [self.car_model1.id]
        }

        response = self.client.post(reverse('associate-parts-to-car-models'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # Teste de usuário não autenticado não conseguir associar peça e carro
    def test_unauthenticated_cannot_associate_parts_to_car_models(self):
        self.client.credentials()
        
        data = {
            'part_ids': [self.part1.id],
            'car_model_ids': [self.car_model1.id]
        }

        response = self.client.post(reverse('associate-parts-to-car-models'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # Teste de usuário comum conseguir visualizar associação de peças e carros
    def test_user_can_view_associations(self):
        access_token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        
        response = self.client.get(reverse('partcarmodel-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Teste de usuário não autenticado não conseguir visualizar associação de peças e carros
    def test_unauthenticated_cannot_view_associations(self):
        self.client.credentials()
        
        response = self.client.get(reverse('partcarmodel-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    # Teste de usuário comum não conseguir desassociar peças e carros
    def test_user_cannot_delete_association(self):
        association = PartCarModel.objects.create(part=self.part1, car_model=self.car_model1)
        access_token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        
        response = self.client.delete(reverse('partcarmodel-detail', args=[association.id]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    # Teste de usuário não autorizado dessassociar peças e carros
    def test_unauthenticated_cannot_delete_association(self):
        association = PartCarModel.objects.create(part=self.part1, car_model=self.car_model1)
        self.client.credentials()
        
        response = self.client.delete(reverse('partcarmodel-detail', args=[association.id]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # Teste de usuário comum conseguir ver carros associados a uma peça específica
    def test_user_can_view_car_models_by_part(self):
        PartCarModel.objects.create(part=self.part1, car_model=self.car_model1)
        access_token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        
        response = self.client.get(reverse('get-car-models-by-part') + f'?part_id={self.part1.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Teste de usuário não autenticado não conseguir ver carros associados a uma peça específica
    def test_unauthenticated_cannot_view_car_models_by_part(self):
        PartCarModel.objects.create(part=self.part1, car_model=self.car_model1)
        self.client.credentials()
        
        response = self.client.get(reverse('get-car-models-by-part') + f'?part_id={self.part1.id}')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # Teste de usuário comum conseguir ver peças associadas a um carro específico
    def test_user_can_view_parts_by_car_model(self):
        PartCarModel.objects.create(part=self.part1, car_model=self.car_model1)
        access_token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        
        response = self.client.get(reverse('get-parts-by-car-model') + f'?car_model_id={self.car_model1.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Teste de usuário não autenticado não conseguir ver peças associadas a um carro específico
    def test_unauthenticated_cannot_view_parts_by_car_model(self):
        PartCarModel.objects.create(part=self.part1, car_model=self.car_model1)
        self.client.credentials()
        
        response = self.client.get(reverse('get-parts-by-car-model') + f'?car_model_id={self.car_model1.id}')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)