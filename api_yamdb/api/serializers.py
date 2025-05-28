from reviews.models import Comment, Review
from .base_components import BaseSerializer
from rest_framework import serializers


class ReviewSerializer(BaseSerializer):
    """Сериализатор для работы с отзывами."""

    title = serializers.SlugRelatedField(slug_field='name', read_only=True)
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )

    class Meta(BaseSerializer.Meta):
        model = Review


class CommentSerializer(BaseSerializer):
    """Сериализатор для работы с комментариями."""

    review = serializers.SlugRelatedField(slug_field='text', read_only=True)

    class Meta(BaseSerializer.Meta):
        model = Comment
