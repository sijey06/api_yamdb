from django.shortcuts import get_object_or_404

from rest_framework.pagination import LimitOffsetPagination

from reviews.models import Comment, Review
from .serializers import (
    CommentSerializer,
    ReviewSerializer,
)

from .base_components import BaseViewSet


class ReviewViewSet(BaseViewSet):
    """Вьюсет для работы с отзывами."""

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        """Сохраняет новый отзыв с авторством текущего пользователя."""
        serializer.save(author=self.request.user)


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
