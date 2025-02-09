from rest_framework import viewsets, filters
from .models import CustomUser, Part, CarModel, PartCarModel
from .serializers import PartListSerializer, PartDetailSerializer, CarModelSerializer, PartCarModelSerializer
from .serializers import UserSerializer
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdmin, IsAdminOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics

class RegisterUserView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class UserManagementViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

class PartViewSet(viewsets.ModelViewSet):
    queryset = Part.objects.all()
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'retrieve':  # GET by ID (detalhe)
            return PartDetailSerializer
        return PartListSerializer  # GET (listar todas as peças)

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['part_number', 'name', 'price']
    search_fields = ['name', 'details']
    ordering_fields = ['price', 'name']

class CarModelViewSet(viewsets.ModelViewSet):
    queryset = CarModel.objects.all()
    serializer_class = CarModelSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['name', 'manufacturer', 'year']
    search_fields = ['name', 'manufacturer']
    ordering_fields = ['name', 'manufacturer', 'year']

class PartCarModelViewSet(viewsets.ModelViewSet):
    queryset = PartCarModel.objects.all()
    serializer_class = PartCarModelSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    serializer_class = PartCarModelSerializer

    @action(detail=False, methods=['post'], url_path='associate')
    def associate_parts_to_car_models(self, request):
        part_ids = request.data.get('part_ids', [])
        car_model_ids = request.data.get('car_model_ids', [])

        if not part_ids or not car_model_ids:
            return Response({"error": "part_ids e car_model_ids são obrigatórios"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            parts = Part.objects.filter(id__in=part_ids)
            car_models = CarModel.objects.filter(id__in=car_model_ids)

            if len(parts) != len(part_ids):
                return Response({"error": "Essa peça não existe"}, status=status.HTTP_404_NOT_FOUND)
            elif len(car_models) != len(car_model_ids):
                return Response({"error": "Esse modelo de carro não existe"}, status=status.HTTP_404_NOT_FOUND)

            associations = []
            for part in parts:
                for car_model in car_models:
                    association, created = PartCarModel.objects.get_or_create(part=part, car_model=car_model)
                    if created:
                        associations.append(association)

            serializer = self.get_serializer(associations, many=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], url_path='parts-by-car-model')
    def get_parts_by_car_model(self, request):
        car_model_id = request.query_params.get('car_model_id')

        if not car_model_id:
            return Response({"error": "car_model_id é obrigatório"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            associations = PartCarModel.objects.filter(car_model_id=car_model_id)
            serializer = self.get_serializer(associations, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], url_path='car-models-by-part')
    def get_car_models_by_part(self, request):
        part_id = request.query_params.get('part_id')

        if not part_id:
            return Response({"error": "part_id é obrigatório"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            associations = PartCarModel.objects.filter(part_id=part_id)
            serializer = self.get_serializer(associations, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)