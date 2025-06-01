from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.viewsets import ModelViewSet

from api.permissions import IsAdminModeratorAuthorOrReadOnly
from reviews.models import Title
from users.models import UserProfile


class BaseViewSet(ModelViewSet):
    """Базовый вьюсет для наследования."""

    permission_classes = (IsAdminModeratorAuthorOrReadOnly,)
    http_method_names = ['get', 'post', 'head', 'options', 'patch', 'delete']


class BaseSerializer(serializers.ModelSerializer):
    """Базовый сериализатор с полем author."""

    author = SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        fields = '__all__'


class BaseNameSlugSerializer(serializers.ModelSerializer):
    """Базовый сериализатор для моделей с полями name и slug."""

    class Meta:
        fields = ('name', 'slug',)


class BaseTitleSerializer(serializers.ModelSerializer):
    """Базовый сериализатор для модели Title."""

    class Meta:
        model = Title
        fields = '__all__'


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
