from rest_framework import serializers
from .models import CustomUser, Part, CarModel, PartCarModel

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'username', 'password', 'role')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password'],
            role=validated_data.get('role', 'user')
        )
        return user

class PartListSerializer(serializers.ModelSerializer):
    """ Serializer para listagem de peças (GET /api/parts/) """
    class Meta:
        model = Part
        fields = ('name', 'details', 'price', 'quantity')

class CarModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarModel
        fields = '__all__'

class PartDetailSerializer(serializers.ModelSerializer):
    """ Serializer para detalhar uma peça (GET /api/parts/{id}/) """
    car_models = CarModelSerializer(source='partcarmodel_set.car_model', many=True, read_only=True)

    class Meta:
        model = Part
        fields = '__all__'

class PartCarModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = PartCarModel
        fields = '__all__'
