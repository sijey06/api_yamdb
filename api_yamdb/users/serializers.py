import re
from django.core.exceptions import ValidationError
from rest_framework import serializers

from .models import UserProfile


class UserProfileCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации пользователей."""

    email = serializers.EmailField()
    username = serializers.CharField()

    class Meta:
        fields = ('username', 'email')
        model = UserProfile

    def validate_username(self, value):
        if value.lower() == 'me':
            raise ValidationError('Username "me" is not allowed')
        if not re.match(r'^[\w.@+-]+$', value):
            raise ValidationError(
                'Username может содержать только буквы, цифры и @/./+/-/_'
            )
        if len(value) > 150:
            raise ValidationError(
                'Username не может быть длиннее 150 символов'
            )
        return value

    def validate_email(self, value):
        if len(value) > 254:
            raise ValidationError(
                'Email не может быть длиннее 254 символов'
            )
        return value


class TokenSerializer(serializers.Serializer):
    """Сериализатор для получения JWT токена."""

    username = serializers.CharField()
    confirmation_code = serializers.CharField()


class UserProfileSerializer(serializers.ModelSerializer):
    """Сериализатор для управления пользователями."""

    class Meta:
        model = UserProfile
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )


class UserProfileEditSerializer(serializers.ModelSerializer):
    """Сериализатор для редактирования профиля пользователя."""

    class Meta:
        model = UserProfile
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )
        read_only_fields = ('role',)
