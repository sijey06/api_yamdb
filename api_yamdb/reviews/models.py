from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from .constants import LENGTH_STR
from users.models import UserProfile


class Genre(models.Model):
    name = models.CharField('название', max_length=256)
    slug = models.SlugField(
        'слаг жанра',
        max_length=50)
        # unique=True)

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
    # rating = models.ForeignKey(
    #     Review,
    #     on_delete=models.SET_NULL,
    #     null=True
    # )
    description = models.TextField('описание',)
    genre = models.ManyToManyField(
        Genre,
        # blank=True,
        # null=True,
        verbose_name='жанр произведения',
        through='GenreTitle'
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


class GenreTitle(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.genre} {self.title}'


class Review(models.Model):
    text = models.TextField(verbose_name='Текст')
    score = models.IntegerField(
        verbose_name="Оценка",
        help_text="Оценка в диапазоне от 1 до 10.",
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10),
        ],  # вынести в константы
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
    )

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text
