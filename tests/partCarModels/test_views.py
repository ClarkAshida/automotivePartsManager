from rest_framework import status
from django.urls import reverse
from rest_framework.test import APITestCase
from automotivePartsManager.models import CarModel, Part, CustomUser, PartCarModel
from rest_framework_simplejwt.tokens import AccessToken

class PartCarModelViewTests(APITestCase):
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
            part_number="54321",
            name="Filtro de Ar",
            details="Filtro de alta qualidade",
            price=652.76,
            quantity=32
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
        self.associate_parts_to_car_models_url = reverse('associate-parts-to-car-models')
        self.partcarmodel_list_url = reverse('partcarmodel-list')
        self.get_car_models_by_part_url = reverse('get-car-models-by-part')
        self.get_parts_by_car_model_url = reverse('get-parts-by-car-model')

    # Teste de usuário admin associar peça e carro com sucesso
    def test_admin_associate_parts_to_car_models(self):
        access_token = AccessToken.for_user(self.admin)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        
        data = {
            'part_ids': [self.part1.id],
            'car_model_ids': [self.car_model1.id]
        }

        response = self.client.post(self.associate_parts_to_car_models_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(PartCarModel.objects.filter(part=self.part1, car_model=self.car_model1).exists())

    # Teste de usuário admin visualizar associações de peças e carros
    def test_admin_can_view_associations(self):
        access_token = AccessToken.for_user(self.admin)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        
        response = self.client.get(self.partcarmodel_list_url)
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
        
        response = self.client.get(f'{self.get_car_models_by_part_url}?part_id={self.part1.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Teste de usuário admin conseguir ver peças associadas a um carro específico
    def test_admin_can_view_parts_by_car_model(self):
        PartCarModel.objects.create(part=self.part1, car_model=self.car_model1)
        access_token = AccessToken.for_user(self.admin)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        
        response = self.client.get(f'{self.get_parts_by_car_model_url}?car_model_id={self.car_model1.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Teste de usuário admin criar associação sem part_id e car_model_id
    def test_admin_associate_parts_to_car_models_without_data(self):
        access_token = AccessToken.for_user(self.admin)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        
        data = {}

        response = self.client.post(self.associate_parts_to_car_models_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("part_ids e car_model_ids são obrigatórios.", response.data['error'])
        
    # Teste de usuário admin criar associação com dados inválidos (part_id é obrigatório)
    def test_admin_associate_parts_to_car_models_with_invalid_data(self):
        access_token = AccessToken.for_user(self.admin)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        
        data = {
            'car_model_ids': [self.car_model1.id]
        }

        response = self.client.post(self.associate_parts_to_car_models_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Essa peça não existe.", response.data['error'])

    # Teste de usuário admin criar associação com dados inválidos (car_model_id é obrigatório)
    def test_admin_associate_parts_to_car_models_with_invalid_data(self):
        access_token = AccessToken.for_user(self.admin)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        
        data = {
            'part_ids': [self.part1.id]
        }

        response = self.client.post(self.associate_parts_to_car_models_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Esse modelo de carro não existe", response.data['error'])

    # Teste de usuário admin criar associação com dados inválidos (part_id não existe)
    def test_admin_associate_parts_to_car_models_with_invalid_data(self):
        access_token = AccessToken.for_user(self.admin)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        
        data = {
            'part_ids': [999],
            'car_model_ids': [self.car_model1.id]
        }

        response = self.client.post(self.associate_parts_to_car_models_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # Teste de usuário admin criar associação com dados inválidos (car_model_id não existe)
    def test_admin_associate_parts_to_car_models_with_invalid_data(self):
        access_token = AccessToken.for_user(self.admin)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        
        data = {
            'part_ids': [self.part1.id],
            'car_model_ids': [999]
        }

        response = self.client.post(self.associate_parts_to_car_models_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
