from colorfield.fields import ColorField
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes'
    )
    name = models.CharField(
        verbose_name='Название рецепта',
        help_text='Назови своё блюдо!'
    )

    # https://docs.djangoproject.com/en/4.1/ref/models/fields/#imagefield
    image = models.ImageField(...)

    text = models.TextField(
        verbose_name='Текст рецепта',
        help_text='Напиши рецепт блюда!'
    )
    # ingridients = models.ManyToManyField(
    #     'Ingridient',
    #     related_name='recipes'
    # )
    # tags = models.ManyToManyField(
    #     'Tag',
    #     related_name='recipes'
    # )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время готовки в минутах',
        help_text='Сколько минут займёт готовка?'
    )

class Tag(models.Model):
    name = models.CharField(
        verbose_name='Название тега',
        help_text='Название тега'
    )
    color = ColorField(default='#2A6CAA')    # https://pypi.org/project/django-colorfield/

    # https://docs.djangoproject.com/en/4.1/ref/contrib/admin/#django.contrib.admin.ModelAdmin.prepopulated_fields
    slug = models.SlugField()


class Ingridient(models.Model):
    name = models.CharField(
        verbose_name='Название ингридиента'
    )
    quantity = models.PositiveSmallIntegerField(
        verbose_name='Количество в юнитах'
    )
    # measurement_unit = models.TextChoices(
    #     verbose_name='Единица измерения'
    # )    # List of units ???
