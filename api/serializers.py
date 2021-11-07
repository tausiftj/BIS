from rest_framework import serializers
from rest_framework.serializers import ValidationError
from api.models import (
    CarBrand,
    CarCity,
    CarModel,
    CarRegistrationNumber,
    City,
    Booking
)
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    email = serializers.CharField(max_length=50, required=False)
    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
            'email',
            'username',
            'is_active',
            'password',
        )

class CarBrandSerializer(serializers.ModelSerializer):

    class Meta:
        model = CarBrand
        exclude = ("created", "updated")


class CarModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = CarModel
        exclude = ("created", "updated")
    
    def to_representation(self, instance):
        self.fields["brand"] = serializers.ReadOnlyField(source="brand.name")
        return super().to_representation(instance)


class CarRegistrationNumberSerializer(serializers.ModelSerializer):

    class Meta:
        model = CarRegistrationNumber
        exclude = ("created", "updated")
    
    def to_representation(self, instance):
        self.fields["model"] = CarModelSerializer(read_only=True)
        return super().to_representation(instance)


class CitySerializer(serializers.ModelSerializer):

    class Meta:
        model = City
        exclude = ("created", "updated")


class CarCitySerializer(serializers.ModelSerializer):

    class Meta:
        model = CarCity
        exclude = ("created", "updated")
    
    def to_representation(self, instance):
        self.fields["car"] = CarModelSerializer(read_only=True)
        return super().to_representation(instance)


class BookingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Booking
        exclude = ('created', 'updated', )
    
    def to_representation(self, instance):
        self.fields["car"] = CarCitySerializer(read_only=True)
        return super().to_representation(instance)


class LoginSerializer(serializers.Serializer):
    """
    API Login Serializer (for otp, password)
    """
    login_key = serializers.CharField()
    password = serializers.CharField(required=False)
    otp_text = serializers.CharField(required=False)
    lat = serializers.CharField(required=False)
    lon = serializers.CharField(required=False)

    def validate(self, validated_data):
        error = {}
        username = validated_data.get('login_key')
        password = validated_data.get('password')

        user = None
        try:
            user = get_user_model().objects.get(username=username)
            if not user.is_active:
                error = {'login_key': 'Account Disabled'}
        except get_user_model().DoesNotExist:
            error.update({'login_key': 'Account Not registered/exists'})

        if not password :
            error.update({
                'password': 'Provide either Password'
            })
        if error:
            raise ValidationError(error)
        return validated_data