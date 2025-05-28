from django.db import models
from reviews.constants import LENGTH_STR


class Review(models.Model):
    pass


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
    # rating = models.ForeignKey(
    #     Review,
    #     on_delete=models.SET_NULL,
    #     null=True
    # )
    description = models.TextField('описание',)
    genre = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
        blank=True,  # поле может быть пустым в форме
        null=True,  # в базе данных может быть сохранено значение null
        verbose_name='жанр произведения',
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
