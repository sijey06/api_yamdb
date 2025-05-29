from django.db.models import Avg
from rest_framework import serializers
from datetime import datetime

from reviews.models import Category, Title, Genre, Comment, Review
from .base_components import BaseSerializer


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ['name', 'slug']
        model = Genre


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ['name', 'slug']
        model = Category


# class TitleSerializer(serializers.ModelSerializer):
#     rating = serializers.SerializerMethodField(read_only=True)
#     genre = serializers.SlugRelatedField(
#         many=True,
#         slug_field='slug',
#         queryset=Genre.objects.all()
#     )
#     category = serializers.SlugRelatedField(
#         slug_field='slug',
#         queryset=Category.objects.all()
#     )

#     class Meta:
#         fields = '__all__'
#         model = Title

#     def get_rating(self, obj):
#         rating_from_reviews = obj.reviews.aggregate(Avg('score'))
#         return rating_from_reviews['score__avg']

#     def validate_year(self, value):
#         current_year = now().year
#         if value > current_year:
#             raise serializers.ValidationError(
#                 'Нельзя добавлять произведение из будущего.')
#         return value
# переделал на 2 сериализатора - для чтения и для записи
class TitleReadSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Title
        fields = '__all__'

    def get_rating(self, obj):
        rating_from_reviews = obj.reviews.aggregate(Avg('score'))
        return rating_from_reviews['score__avg']


class TitleWriteSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        many=True,
        slug_field='slug'
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )

    class Meta:
        model = Title
        fields = '__all__'

    def validate_year(self, value):
        if value > datetime.now().year:
            raise serializers.ValidationError(
                'Нельзя добавлять произведения из будущего.'
            )
        return value


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