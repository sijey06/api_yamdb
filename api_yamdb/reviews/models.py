from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from .constants import LENGTH_STR, MIN_SCORE, MAX_SCORE
from users.models import UserProfile


class Genre(models.Model):
    name = models.CharField('название', max_length=256)
    slug = models.SlugField(
        'слаг жанра',
        max_length=50,
        unique=True)

    def __str__(self):
        return self.name[:LENGTH_STR]


class Category(models.Model):
    name = models.CharField('название', max_length=256)
    slug = models.SlugField(
        'слаг категории',
        max_length=50,
        unique=True)

    def __str__(self):
        return self.name[:LENGTH_STR]


class Title(models.Model):
    name = models.CharField('название', max_length=256)
    year = models.IntegerField('год выпуска',)
    description = models.TextField('описание',)
    genre = models.ManyToManyField(
        Genre,
        verbose_name='жанр произведения'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='категория произведения',
    )

    class Meta:
        default_related_name = 'titles'
        verbose_name = 'произведение'
        verbose_name_plural = 'произведения'
        ordering = ['-year']

    def __str__(self):
        return self.name[:LENGTH_STR]


class Review(models.Model):
    text = models.TextField(verbose_name='Текст')
    score = models.IntegerField(
        verbose_name='Оценка',
        help_text=f'Оценка в диапазоне от {MIN_SCORE} до {MAX_SCORE}.',
        validators=[
            MinValueValidator(MIN_SCORE),
            MaxValueValidator(MAX_SCORE),
        ],
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
        constraints = (
            models.UniqueConstraint(
                fields=('author', 'title'),
                name='unique_reviews',
            ),
        )

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
    pub_date = models.DateTimeField(
        verbose_name='Дата добавления',
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text
