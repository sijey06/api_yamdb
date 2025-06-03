import re

from django.core.exceptions import ValidationError
from rest_framework import serializers

from api.base_components import BaseAllFieldsSerializer
from reviews.constants import LENGTH_EMAIL, LENGTH_USERNAME
from .models import UserProfile


class UserProfileCreateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    username = serializers.CharField()

    class Meta:
        fields = ('username', 'email')
        model = UserProfile

    def validate_username(self, value):
        if value.lower() == 'me':
            raise ValidationError('Username "me" запрещено')
        if not re.match(r'^[\w.@+-]+$', value):
            raise ValidationError(
                'Username может содержать только буквы, цифры и @/./+/-/_'
            )
        if len(value) > LENGTH_USERNAME:
            raise ValidationError(
                f'Username не может быть длиннее {LENGTH_USERNAME} символов'
            )
        return value

    def validate_email(self, value):
        if len(value) > LENGTH_EMAIL:
            raise ValidationError(
                f'Email не может быть длиннее {LENGTH_EMAIL} символов'
            )
        return value

    def validate(self, data):
        username = data.get('username')
        email = data.get('email')

        existing_account = UserProfile.objects.filter(
            username=username, email=email
        ).first()
        if existing_account is not None:
            data['detail'] = 'Учетная запись уже существует'
            return data
        elif UserProfile.objects.filter(username=username).exists():
            raise serializers.ValidationError(
                {'username': ['Имя пользователя уже занято']}
            )
        elif UserProfile.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                {'email': ['Email уже используется']}
            )
        return data

    def create(self, validated_data):
        detail_message = validated_data.pop('detail', None)

        if detail_message:
            return {'detail': detail_message}

        instance = super().create(validated_data)
        return instance


class TokenSerializer(serializers.Serializer):
    """Сериализатор для получения JWT токена."""

    username = serializers.CharField()
    confirmation_code = serializers.CharField()


class UserProfileSerializer(BaseAllFieldsSerializer):
    """Сериализатор для управления пользователями."""


class UserProfileEditSerializer(BaseAllFieldsSerializer):
    """Сериализатор для редактирования профиля пользователя."""

    class Meta(BaseAllFieldsSerializer.Meta):
        read_only_fields = ('role',)
