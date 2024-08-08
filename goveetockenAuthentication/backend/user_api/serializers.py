from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from .models import UserProfile

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    api_key = serializers.CharField(max_length=255, write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'api_key')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        api_key = validated_data.pop('api_key')
        user = User.objects.create_user(**validated_data)
        UserProfile.objects.create(user=user, api_key=api_key)
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if not user or not user.is_active:
            raise serializers.ValidationError('Incorrect credentials')
        return {'user': user}

class UserSerializer(serializers.ModelSerializer):
    api_key = serializers.CharField(source='userprofile.api_key', read_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'api_key')
