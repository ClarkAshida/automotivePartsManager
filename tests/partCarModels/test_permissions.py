from rest_framework import status
from django.urls import reverse
from rest_framework.test import APITestCase
from automotivePartsManager.models import CarModel, Part, CustomUser, PartCarModel
from rest_framework_simplejwt.tokens import AccessToken

# Teste de end points com usuário comum e usuário não autenticado
class PartCarModelViewPermissionsTests(APITestCase):
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
        self.car_model1 = CarModel.objects.create(
            name="Civic",
            manufacturer="Honda",
            year=2020
        )
        self.associate_parts_to_car_models_url = reverse('associate-parts-to-car-models')
        self.partcarmodel_list_url = reverse('partcarmodel-list')
        self.get_car_models_by_part_url = reverse('get-car-models-by-part')
        self.get_parts_by_car_model_url = reverse('get-parts-by-car-model')

    # Teste de usuário comum não conseguir associar peça e carro
    def test_user_cannot_associate_parts_to_car_models(self):
        access_token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        
        data = {
            'part_ids': [self.part1.id],
            'car_model_ids': [self.car_model1.id]
        }

        response = self.client.post(self.associate_parts_to_car_models_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # Teste de usuário não autenticado não conseguir associar peça e carro
    def test_unauthenticated_cannot_associate_parts_to_car_models(self):
        self.client.credentials()
        
        data = {
            'part_ids': [self.part1.id],
            'car_model_ids': [self.car_model1.id]
        }

        response = self.client.post(self.associate_parts_to_car_models_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # Teste de usuário comum conseguir visualizar associação de peças e carros
    def test_user_can_view_associations(self):
        access_token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        
        response = self.client.get(self.partcarmodel_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Teste de usuário não autenticado não conseguir visualizar associação de peças e carros
    def test_unauthenticated_cannot_view_associations(self):
        self.client.credentials()
        
        response = self.client.get(self.partcarmodel_list_url)
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
        
        response = self.client.get(f'{self.get_car_models_by_part_url}?part_id={self.part1.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Teste de usuário não autenticado não conseguir ver carros associados a uma peça específica
    def test_unauthenticated_cannot_view_car_models_by_part(self):
        PartCarModel.objects.create(part=self.part1, car_model=self.car_model1)
        self.client.credentials()
        
        response = self.client.get(f'{self.get_car_models_by_part_url}?part_id={self.part1.id}')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # Teste de usuário comum conseguir ver peças associadas a um carro específico
    def test_user_can_view_parts_by_car_model(self):
        PartCarModel.objects.create(part=self.part1, car_model=self.car_model1)
        access_token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        
        response = self.client.get(f'{self.get_parts_by_car_model_url}?car_model_id={self.car_model1.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Teste de usuário não autenticado não conseguir ver peças associadas a um carro específico
    def test_unauthenticated_cannot_view_parts_by_car_model(self):
        PartCarModel.objects.create(part=self.part1, car_model=self.car_model1)
        self.client.credentials()
        
        response = self.client.get(f'{self.get_parts_by_car_model_url}?car_model_id={self.car_model1.id}')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # Teste de usuário comum não conseguir editar associação
    def test_user_cannot_edit_association(self):
        association = PartCarModel.objects.create(part=self.part1, car_model=self.car_model1)
        access_token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        
        response = self.client.put(reverse('partcarmodel-detail', args=[association.id]), {'part': self.part1.id, 'car_model': self.car_model1.id}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(PartCarModel.objects.get(id=association.id).part, self.part1)
        self.assertEqual(PartCarModel.objects.get(id=association.id).car_model, self.car_model1)
        self.assertEqual(PartCarModel.objects.count(), 1)
    
    # Teste de usuário não autenticado não conseguir editar associação
    def test_unauthenticated_cannot_edit_association(self):
        association = PartCarModel.objects.create(part=self.part1, car_model=self.car_model1)
        self.client.credentials()
        
        response = self.client.put(reverse('partcarmodel-detail', args=[association.id]), {'part': self.part1.id, 'car_model': self.car_model1.id}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(PartCarModel.objects.get(id=association.id).part, self.part1)
        self.assertEqual(PartCarModel.objects.get(id=association.id).car_model, self.car_model1)
        self.assertEqual(PartCarModel.objects.count(), 1)