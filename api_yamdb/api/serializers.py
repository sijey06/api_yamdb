from django.db.models import Avg
from rest_framework import serializers

from reviews.models import Category, Title, Genre


class TitleSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()

    class Meta:
        fields = '__all__'
        model = Title

    def get_rating(self, obj):
        # получаем по related_name 'reviews' все отзывы к произведению obj
        # и через функцию aggregate рассчитываем среднее значение рейтинга
        rating_from_reviews = obj.reviews.aggregate(Avg('score'))
        return rating_from_reviews['score__avg']


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Category


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Genre
