from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.models import Comment, Review, User


class BaseAuthorSerializer(serializers.ModelSerializer):
    """Базовый сериализатор с полем author."""

    author = SlugRelatedField(
        read_only=True,
        slug_field='username',
    )

    class Meta:
        fields = '__all__'


class ReviewSerializer(BaseAuthorSerializer):
    """Сериализатор для работы с отзывами."""

    class Meta(BaseAuthorSerializer.Meta):
        model = Review


class CommentSerializer(BaseAuthorSerializer):
    """Сериализатор для работы с комментариями."""

    class Meta(BaseAuthorSerializer.Meta):
        model = Comment
        read_only_fields = ('review',)
