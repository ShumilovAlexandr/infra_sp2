import django.contrib.auth.validators
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    USER_ROLE_CHOICES = [
        (USER, 'пользователь'),
        (MODERATOR, 'модератор'),
        (ADMIN, 'администратор'),
    ]
    role = models.TextField(
        choices=USER_ROLE_CHOICES,
        default=USER,
        verbose_name='Пользовательская роль',
    )
    bio = models.TextField(
        blank=True,
        verbose_name='Биография',
    )
    email = models.EmailField(
        unique=True,
        max_length=254,
        verbose_name='Электронная почта',
    )
    username = models.CharField(
        error_messages={
            'unique': 'Пользователь с таким именем уже существует.'
        },
        help_text='Не более 150 символов, буквы, цифры и @/./+/-/_ только.',
        max_length=150,
        unique=True,
        validators=[django.contrib.auth.validators.UnicodeUsernameValidator()],
        verbose_name='Имя пользователя',
    )
    first_name = models.CharField(
        blank=True,
        max_length=150,
        verbose_name='Имя'
    )
    last_name = models.CharField(
        blank=True,
        max_length=150,
        verbose_name='Фамилия'
    )
