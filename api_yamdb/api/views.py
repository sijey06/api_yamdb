from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.viewsets import (
    ModelViewSet,
)

from reviews.models import Comment, Review
from .serializers import (
    CommentSerializer,
    ReviewSerializer,
)


class BaseViewSet(ModelViewSet):
    """Базовый вьюсет для наследования."""

    def check_ownership(self, instance):
        """Общая проверка владения объектом."""
        if instance.author != self.request.user:
            raise PermissionDenied(
                'Вы можете изменять только собственные записи.'
            )


class ReviewViewSet(BaseViewSet):
    """Вьюсет для работы с отзывами."""

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        """Сохраняет новый отзыв с авторством текущего пользователя."""
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        """Обновляет существующий отзыв с проверкой владельца."""
        instance = self.get_object()
        self.check_ownership(instance)
        super().perform_update(serializer)

    def perform_destroy(self, instance):
        """Удаляет существующий отзыв с проверкой владельца."""
        self.check_ownership(instance)
        super().perform_destroy(instance)


class CommentViewSet(BaseViewSet):
    """Вьюсет для работы с комментариями."""

    serializer_class = CommentSerializer

    def _get_review(self):
        """Приватный метод для получения отзыва по его идентификатору."""
        review_id = self.kwargs.get('review_id')
        return get_object_or_404(Review, pk=review_id)

    def get_queryset(self):
        """Возвращает фильтр комментариев, относящихся к конкретному отзыву."""
        review = self._get_review()
        if review is None:
            return Comment.objects.none()
        return review.comments.all()

    def perform_create(self, serializer):
        """Сохраняет комментарий с авторством текущего пользователя."""
        serializer.save(author=self.request.user, review=self._get_review())

    def perform_update(self, serializer):
        """Обновляет существующий комментарий с проверкой владельца."""
        instance = self.get_object()
        self.check_ownership(instance)
        super().perform_update(serializer)

    def perform_destroy(self, instance):
        """Удаляет существующий комментарий с проверкой владельца."""
        self.check_ownership(instance)
        super().perform_destroy(instance)
