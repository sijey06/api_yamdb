from datetime import datetime

from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from api.base_components import (
    BaseNameSlugSerializer,
    BaseSerializer,
    BaseTitleSerializer,
)
from reviews.models import Category, Comment, Genre, Review, Title


class GenreSerializer(BaseNameSlugSerializer):
    """Сериализатор для работы с жанрами произведений."""

    class Meta(BaseNameSlugSerializer.Meta):
        model = Genre


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для работы с категориями произведений."""

    class Meta(BaseNameSlugSerializer.Meta):
        model = Category


class TitleReadSerializer(BaseTitleSerializer):
    """Сериализатор для чтения произведений."""

    rating = serializers.SerializerMethodField()
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)

    def get_rating(self, obj):
        """Возвращает рейтинг произведений."""
        rating_from_reviews = obj.reviews.aggregate(Avg('score'))
        return rating_from_reviews['score__avg']


class TitleWriteSerializer(BaseTitleSerializer):
    """Сериализатор для записи (создания и обновления) произведений."""

    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        many=True,
        slug_field='slug'
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )

    def validate_year(self, value):
        """Проверяет, чтобы значение года не указывалось в будущем."""
        if value > datetime.now().year:
            raise serializers.ValidationError(
                'Нельзя добавлять произведения из будущего.'
            )
        return value


class ReviewSerializer(BaseSerializer):
    """Сериализатор для работы с отзывами."""

    title = serializers.SlugRelatedField(slug_field='name', read_only=True)

    def validate(self, validated_data):
        """Валидация отзыва: проверка уникальности отзыва от пользователя."""
        request = self.context['request']
        title = get_object_or_404(
            Title, pk=self.context['view'].kwargs['title_id']
        )

        if (
            request.method == 'POST'
            and Review.objects.filter(
                title=title, author=request.user
            ).exists()
        ):
            raise ValidationError('Данный пользователь уже оставил отзыв!')

        return validated_data

    class Meta(BaseSerializer.Meta):
        model = Review


class CommentSerializer(BaseSerializer):
    """Сериализатор для работы с комментариями."""

    review = serializers.SlugRelatedField(slug_field='text', read_only=True)

    class Meta(BaseSerializer.Meta):
        model = Comment
