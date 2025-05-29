from rest_framework import filters, viewsets
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import permissions

from .permissions import IsAdminOrReadOnly
from .serializers import (
    CategorySerializer,
    # TitleSerializer,
    TitleReadSerializer,
    TitleWriteSerializer,
    GenreSerializer,
    CommentSerializer,
    ReviewSerializer
)
from .filters import TitleFilter
from reviews.models import Category, Title, Genre, Comment, Review
from .base_components import BaseViewSet


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    # serializer_class = TitleSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = (DjangoFilterBackend,)
    # filterset_fields = (
    #     'category',
    #     'genre__slug',
    #     'name',
    #     'year',
    # )
    # чтобы корректно фильтровать 'genre__slug' используем кастомный FilterSet
    filterset_class = TitleFilter
    # тут исключаем метод PUT
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return TitleReadSerializer
        return TitleWriteSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class ReviewViewSet(BaseViewSet):
    """Вьюсет для работы с отзывами."""

    serializer_class = ReviewSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        """Получает все отзывы по id произведения."""
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        return title.reviews.all()

    def perform_create(self, serializer):
        """Сохраняет новый отзыв с авторством текущего пользователя."""
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(BaseViewSet):
    """Вьюсет для работы с комментариями."""

    serializer_class = CommentSerializer

    def _get_review(self):
        """Приватный метод для получения отзыва по его идентификатору."""
        review_id = self.kwargs['review_id']
        title_id = self.kwargs['title_id']
        return get_object_or_404(Review, id=review_id, title_id=title_id)

    def get_queryset(self):
        """Возвращает фильтр комментариев, относящихся к конкретному отзыву."""
        review = self._get_review()
        if review is None:
            return Comment.objects.none()
        return review.comments.all()

    def perform_create(self, serializer):
        """Сохраняет комментарий с авторством текущего пользователя."""
        serializer.save(author=self.request.user, review=self._get_review())