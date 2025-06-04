from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, permissions, serializers, viewsets

from api.base_components import BaseViewSet
from api.filters import TitleFilter
from api.permissions import IsAdminOrReadOnly
from api.serializers import (CategorySerializer, CommentSerializer,
                             GenreSerializer, ReviewSerializer,
                             TitleReadSerializer, TitleWriteSerializer)
from reviews.models import Category, Comment, Genre, Review, Title
from .base_components import BaseViewSet
from .filters import TitleFilter
from .permissions import IsAdminOrReadOnly
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer,
                          TitleReadSerializer, TitleWriteSerializer)


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с произведениями."""

    queryset = Title.objects.all()
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']

    def get_serializer_class(self):
        """Возвращает класс сериализатора в зависимости от типа запроса."""
        if self.request.method in permissions.SAFE_METHODS:
            return TitleReadSerializer
        return TitleWriteSerializer


class CategoryViewSet(mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    """Вьюсет для работы с категориями произведений."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class GenreViewSet(mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    """Вьюсет для работы с жанрами произведений."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class ReviewViewSet(BaseViewSet):
    """Вьюсет для работы с отзывами."""

    serializer_class = ReviewSerializer

    def _get_title(self):
        """Приватный метод для получения публикации по её идентификатору."""
        return get_object_or_404(Title, id=self.kwargs['title_id'])

    def get_queryset(self):
        """Получает все отзывы по id произведения."""
        return self._get_title().reviews.all()

    def perform_create(self, serializer):
        """Сохраняет новый отзыв с авторством текущего пользователя."""
        serializer.save(author=self.request.user, title=self._get_title())


class CommentViewSet(BaseViewSet):
    """Вьюсет для работы с комментариями."""

    serializer_class = CommentSerializer

    def _get_review(self):
        """Приватный метод для получения отзыва по его идентификатору."""
        return get_object_or_404(
            Review,
            id=self.kwargs['review_id'],
            title_id=self.kwargs['title_id'],
        )

    def get_queryset(self):
        """Возвращает фильтр комментариев, относящихся к конкретному отзыву."""
        review = self._get_review()
        if review is None:
            return Comment.objects.none()
        return review.comments.all()

    def perform_create(self, serializer):
        """Сохраняет комментарий с авторством текущего пользователя."""
        serializer.save(author=self.request.user, review=self._get_review())
