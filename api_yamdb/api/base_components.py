from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from rest_framework.exceptions import PermissionDenied
from rest_framework.viewsets import ModelViewSet

from .permissions import OwnerOrReadOnly


class BaseViewSet(ModelViewSet):
    """Базовый вьюсет для наследования."""

    permission_classes = (OwnerOrReadOnly,)  # заменить кастомным классом по ТЗ

    def check_ownership(self, instance):
        """Общая проверка владения объектом."""
        if instance.author != self.request.user:
            raise PermissionDenied(
                'Вы можете изменять только собственные записи.'
            )


class BaseSerializer(serializers.ModelSerializer):
    """Базовый сериализатор с полем author."""

    author = SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        fields = '__all__'
