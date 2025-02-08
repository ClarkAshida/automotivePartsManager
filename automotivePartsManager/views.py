from rest_framework import viewsets
from .models import CustomUser, Part, CarModel, PartCarModel
from .serializers import PartSerializer, CarModelSerializer, PartCarModelSerializer
from .serializers import UserSerializer
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdmin
from rest_framework import generics


class RegisterUserView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny] # Qualquer um pode se registrar (apenas users comuns), preciso ver como cadastrar um usuário admin

class PartViewSet(viewsets.ModelViewSet):
    queryset = Part.objects.all()
    serializer_class = PartSerializer
    permission_classes = [IsAuthenticated, IsAdmin]


class CarModelViewSet(viewsets.ModelViewSet):
    queryset = CarModel.objects.all()
    serializer_class = CarModelSerializer
    permission_classes = [IsAuthenticated, IsAdmin]  # Apenas admins podem modificar


class PartCarModelViewSet(viewsets.ModelViewSet):
    queryset = PartCarModel.objects.all()
    serializer_class = PartCarModelSerializer