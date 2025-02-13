import time
from datetime import timedelta
from django.conf import settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from automotivePartsManager.models import CustomUser
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

class JWTAuthenticationTests(APITestCase):
    def setUp(self):
        self.user_data = {
            'email': 'newuser@email.com',
            'username': 'testuser',
            'password': 'Test!123',
            'role': 'user',
        }
        self.user = CustomUser.objects.create_user(
                email=self.user_data['email'],
                username=self.user_data['username'],
                password=self.user_data['password'],
                role=self.user_data['role']
            )
        self.login_url = reverse('token_obtain_pair')
        self.refresh_url = reverse('token_refresh')
        self.protected_url = reverse('carmodel-list')
    
    # Teste de registro de usuário e login com dados registrados
    def test_user_registration_and_obtain_token(self):
        response = self.client.post(reverse('register'), {
            'email': 'newuser2@email.com',
            'username': 'testuser2',
            'password': 'Test!123',
            'role': 'user',
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        self.assertEqual(CustomUser.objects.count(), 2)
        login_response = self.client.post(self.login_url, {
            'email': 'newuser2@email.com',
            'password': 'Test!123'
        }, format='json')
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        self.assertIn('access', login_response.data)
        self.assertIn('refresh', login_response.data)

    # Teste de registro de usuário com dados inválidos
    def test_user_registration_invalid_data(self):
        response = self.client.post(reverse('register'), {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            str(response.data['email'][0]), 'Este campo é obrigatório.'
        )
        self.assertEqual(
            str(response.data['password'][0]), 'Este campo é obrigatório.'
        )
    
    # Teste de obtenção de token com dados de registro válido
    def test_user_login(self):
        response = self.client.post(self.login_url, {
            'email': self.user_data['email'],
            'password': self.user_data['password']
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
    
    # Teste de obtenção de token com dados de login inválido
    def test_user_login_invalid_data(self):
        response = self.client.post(self.login_url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {
            'email': ['Este campo é obrigatório.'],
            'password': ['Este campo é obrigatório.']
        })
    
    # Teste de expiração do token de acesso (simulada)
    def test_expired_access_token(self):
        expired_token = AccessToken.for_user(self.user)
        expired_token.set_exp(lifetime=timedelta(seconds=-1))  # Simula a expiração do token
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {expired_token}')
        response = self.client.get(self.protected_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # Teste de geração de novo token de acesso usando refresh token
    def test_refresh_access_token(self):
        login_response = self.client.post(self.login_url, {
            'email': self.user_data['email'],
            'password': self.user_data['password']
        }, format='json')

        refresh_token = login_response.data['refresh']
        
        refresh_response = self.client.post(self.refresh_url, {'refresh': refresh_token}, format='json')
        self.assertEqual(refresh_response.status_code, status.HTTP_200_OK)
        self.assertIn('access', refresh_response.data)

    # Teste de tentativa de uso de refresh token expirado (simulada)
    def test_expired_refresh_token(self):
        refresh_token = RefreshToken.for_user(self.user)
        refresh_token.set_exp(lifetime=timedelta(seconds=-1))  # Simula a expiração do refresh token

        response = self.client.post(self.refresh_url, {'refresh': str(refresh_token)}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # Teste de tentativa de login com credenciais inválidas
    def test_invalid_login(self):
        response = self.client.post(self.login_url, {
            'email': 'invalid@email.com',
            'password': 'WrongPass!123'
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotIn('access', response.data)
        self.assertNotIn('refresh', response.data)
    
    # Teste de tentativa de uso de token inválido
    def test_invalid_access_token(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer invalidtoken')
        response = self.client.get(self.protected_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # Teste de tentativa de acesso sem token
    def test_access_protected_endpoint_without_token(self):
        self.client.credentials()
        response = self.client.get(self.protected_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)