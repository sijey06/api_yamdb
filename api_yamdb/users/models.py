import secrets

from django.contrib.auth.models import AbstractUser
from django.db import models

from reviews.constants import LENGTH_CODE, LENGTH_EMAIL, LENGTH_ROLE


class UserProfile(AbstractUser):
    """Пользовательская модель, расширенная дополнительными полями и ролями."""

    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'

    ROLE_CHOICES = [
        (ADMIN, 'Администратор'),
        (MODERATOR, 'Модератор'),
        (USER, 'Пользователь'),
    ]

    email = models.EmailField(
        max_length=LENGTH_EMAIL,
        unique=True,
        verbose_name='Адрес электронной почты',
    )
    bio = models.TextField(
        blank=True,
        verbose_name='Биография',
    )
    role = models.CharField(
        max_length=LENGTH_ROLE,
        choices=ROLE_CHOICES,
        default=USER,
        verbose_name='Роль пользователя',
    )
    confirmation_code = models.CharField(
        max_length=LENGTH_CODE,
        blank=True,
        null=True,
        verbose_name='Код подтверждения',
    )

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    def set_confirmation_code(self):
        self.confirmation_code = secrets.token_urlsafe(16)
        self.save(update_fields=['confirmation_code'])

    class Meta:
        ordering = ['id']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
