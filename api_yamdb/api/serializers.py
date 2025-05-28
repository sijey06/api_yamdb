from reviews.models import Comment, Review
from .base_components import BaseSerializer


class ReviewSerializer(BaseSerializer):
    """Сериализатор для работы с отзывами."""

    class Meta(BaseSerializer.Meta):
        model = Review


class CommentSerializer(BaseSerializer):
    """Сериализатор для работы с комментариями."""

    class Meta(BaseSerializer.Meta):
        model = Comment
