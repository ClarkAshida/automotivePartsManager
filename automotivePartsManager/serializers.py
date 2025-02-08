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

class PartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Part
        fields = '__all__'

class CarModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarModel
        fields = '__all__'

class PartCarModelSerializer(serializers.ModelSerializer):
    part = PartSerializer(read_only=True)
    car_model = CarModelSerializer(read_only=True)
    
    class Meta:
        model = PartCarModel
        fields = '__all__'
