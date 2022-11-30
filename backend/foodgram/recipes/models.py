from colorfield.fields import ColorField
from django.db import models

from users.models import User


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes'
    )
    name = models.CharField(
        max_length=100,
        verbose_name='Название рецепта',
        help_text='Назови своё блюдо!'
    )

    # https://docs.djangoproject.com/en/4.1/ref/models/fields/#imagefield
    image = models.ImageField(upload_to='uploads/')

    text = models.TextField(
        verbose_name='Текст рецепта',
        help_text='Напиши рецепт блюда!'
    )
    ingridients = models.ManyToManyField(
        'Ingridient',
        related_name='recipes'
    )
    tags = models.ManyToManyField(
        'Tag',
        related_name='recipes'
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время готовки в минутах',
        help_text='Сколько минут займёт готовка?'
    )

class Tag(models.Model):
    name = models.CharField(
        max_length=30,
        unique=True,
        verbose_name='Название тега',
        help_text='Название тега'
    )
    color = ColorField(
        default='#2A6CAA',
        unique=True
    )    # https://pypi.org/project/django-colorfield/
    slug = models.SlugField(
        unique=True
    )


class Ingridient(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='Название ингридиента'
    )
    quantity = models.PositiveSmallIntegerField(
        verbose_name='Количество в юнитах'
    )
    measurement_unit = models.CharField(
        max_length=30,
        default='г',
        verbose_name='Единица измерения'
    )
