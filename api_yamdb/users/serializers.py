import re

from django.core.exceptions import ValidationError
from rest_framework import serializers

from .mixins import BaseAllFieldsSerializer
from .models import UserProfile
from reviews.constants import LENGTH_EMAIL, LENGTH_USERNAME


class UserProfileCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации пользователей."""

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
                'Username не может быть длиннее 150 символов'
            )
        return value

    def validate_email(self, value):
        if len(value) > LENGTH_EMAIL:
            raise ValidationError(
                'Email не может быть длиннее 254 символов'
            )
        return value


class TokenSerializer(serializers.Serializer):
    """Сериализатор для получения JWT токена."""

    username = serializers.CharField()
    confirmation_code = serializers.CharField()


class UserProfileSerializer(BaseAllFieldsSerializer):
    """Сериализатор для управления пользователями."""

    pass


class UserProfileEditSerializer(BaseAllFieldsSerializer):
    """Сериализатор для редактирования профиля пользователя."""

    class Meta(BaseAllFieldsSerializer.Meta):
        read_only_fields = ('role',)
