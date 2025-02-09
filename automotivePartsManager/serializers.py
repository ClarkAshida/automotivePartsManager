from rest_framework import serializers
from .models import CustomUser, Part, CarModel, PartCarModel

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'username', 'password', 'role')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        request = self.context.get('request')

        if validated_data.get('role', 'user') == 'admin':
            if not request or not request.user.is_authenticated or not request.user.is_staff:
                raise serializers.ValidationError({'role': 'Apenas administradores podem criar usuários admin.'})

        return CustomUser.objects.create_user(**validated_data)
    
    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("A senha deve ter pelo menos 8 caracteres.")
        return value

class PartListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Part
        fields = ('name', 'details', 'price', 'quantity')
    
    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("O preço deve ser maior que zero.")
        return value

    def validate_quantity(self, value):
        if value < 0:
            raise serializers.ValidationError("A quantidade não pode ser negativa.")
        return value

class CarModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarModel
        fields = '__all__'

class PartDetailSerializer(serializers.ModelSerializer):
    car_models = CarModelSerializer(source='partcarmodel_set.car_model', many=True, read_only=True)

    class Meta:
        model = Part
        fields = '__all__'

class PartCarModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = PartCarModel
        fields = '__all__'
    
    def validate(self, data):
        if PartCarModel.objects.filter(part=data['part'], car_model=data['car_model']).exists():
            raise serializers.ValidationError("Essa peça já está associada a esse modelo de carro.")
        return data
