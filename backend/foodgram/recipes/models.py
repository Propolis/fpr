from colorfield.fields import ColorField
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        blank=False
    )
    name = models.CharField(
        max_length=100,
        verbose_name='Название рецепта',
        help_text='Назови своё блюдо!'
    )
    image = models.ImageField(
        upload_to='recipes/images/',
        blank=True
    )
    text = models.TextField(
        verbose_name='Текст рецепта',
        help_text='Напиши рецепт блюда!'
    )
    ingredients = models.ManyToManyField(
        'Ingredient',
        through='RecipeIngredient',
        related_name='recipes',
        # blank=False
        # null=False
    )
    tags = models.ManyToManyField(
        'Tag',
        through='RecipeTag',
        related_name='recipes',
        blank=True
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время готовки в минутах',
        help_text='Сколько минут займёт готовка?'
    )

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='Название тега',
        help_text='Название тега'
    )
    color = ColorField(
        default='#2A6CAA',
        unique=True
    )
    slug = models.SlugField(
        max_length=200,
        unique=True
    )

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='Название ингридиента'
    )
    measurement_unit = models.CharField(
        max_length=30,
        default='г',
        verbose_name='Единица измерения'
    )

    def __str__(self):
        return self.name


class RecipeTag(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.DO_NOTHING
    )
    tag = models.ForeignKey(
        Tag,
        on_delete=models.DO_NOTHING
    )


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.DO_NOTHING
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.DO_NOTHING
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество в юнитах'
    )
