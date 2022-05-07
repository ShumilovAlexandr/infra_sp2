import datetime

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from users.models import User


class Category(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Категория',
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='Слаг категории',
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Жанр',
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Слаг жанра',
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        max_length=140,
        verbose_name='Название произведения',
    )
    year = models.PositiveIntegerField(
        validators=(MinValueValidator(0),
                    MaxValueValidator(datetime.date.today().year),
                    ),
        db_index=True,
        verbose_name='Год выпуска',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name='category_title',
        verbose_name='Категория',
    )
    description = models.TextField(
        verbose_name='Описание',
    )
    genre = models.ManyToManyField(
        Genre,
        blank=True,
        related_name='genre',
        verbose_name='Жанр',
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор',
    )
    text = models.TextField(
        verbose_name='Текст',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Дата создания',
    )
    score = models.PositiveIntegerField(
        validators=(MinValueValidator(1),
                    MaxValueValidator(10),
                    ),
        verbose_name='Рейтинг',
    )

    class Meta:
        ordering = ['-pub_date']
        unique_together = ('title', 'author')
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Комментарий',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор',
    )
    text = models.TextField(
        verbose_name='Автор',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Дата создания',
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
