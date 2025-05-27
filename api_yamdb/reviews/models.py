from django.contrib.auth import get_user_model  # заменить на кастомный
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

UserProfile = get_user_model()  # заменить на кастомный


class Title(models.Model):  # заменить по готовности
    """Модель публикации."""


class Review(models.Model):
    text = models.TextField(verbose_name='Текст')
    score = models.IntegerField(
        verbose_name="Оценка",
        help_text="Оценка в диапазоне от 1 до 10.",
        validators=[MinValueValidator(1), MaxValueValidator(10)],
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
    )
    author = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор отзыва',
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение',
    )

    class Meta:
        verbose_name = 'отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return self.text


class Comment(models.Model):
    text = models.TextField(verbose_name='Текст')
    author = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор комментария',
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв',
    )
    created = models.DateTimeField(
        verbose_name='Дата добавления',
        auto_now_add=True,
        db_index=True,
    )

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'
