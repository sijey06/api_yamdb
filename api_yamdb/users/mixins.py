from rest_framework import serializers

from .models import UserProfile


class BaseAllFieldsSerializer(serializers.ModelSerializer):
    """Базовый сериализатор, использующий нужные поля и модель юзера."""

    class Meta:
        abstract = True
        model = UserProfile
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )
