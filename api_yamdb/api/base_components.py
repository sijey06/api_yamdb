from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from rest_framework.exceptions import PermissionDenied
from rest_framework.viewsets import ModelViewSet

from .permissions import IsAdminModeratorAuthorOrReadOnly


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
