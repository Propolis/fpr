from django.contrib.auth import get_user_model
from django.db import models
from colorfield.fields import ColorField

User = get_user_model()


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        blank=False,
        verbose_name='Автор',
    )
    name = models.CharField(
        max_length=100,
        verbose_name='Название рецепта',
        help_text='Назови своё блюдо!'
    )
    image = models.ImageField(
        upload_to='recipes/images/',
        blank=True,
        verbose_name='Изображение',
        help_text='Загрузи изображение!'
    )
    text = models.TextField(
        verbose_name='Текст рецепта',
        help_text='Напиши рецепт блюда!'
    )
    ingredients = models.ManyToManyField(
        'Ingredient',
        through='RecipeIngredient',
        related_name='recipes',
        verbose_name='Ингредиенты',
        help_text='Добавь ингредиенты!\nНе забудь нажать кнопку "Добавить"'
    )
    tags = models.ManyToManyField(
        'Tag',
        through='RecipeTag',
        related_name='recipes',
        blank=True,
        verbose_name='Теги',
        help_text='Добавь теги!'
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время готовки в минутах',
        help_text='Сколько минут займёт готовка?'
    ),
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

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
    )
    slug = models.SlugField(
        max_length=30,
        unique=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class Ingredient(models.Model):
    name = models.CharField(
        max_length=254,
        verbose_name='Название ингридиента'
    )
    measurement_unit = models.CharField(
        max_length=30,
        default='г',
        verbose_name='Единица измерения'
    )

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'


class RecipeTag(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE
    )
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'tag'],
                name='unique tag in recipe'
            )
        ]
        verbose_name = 'Теги, привязанные к рецептам'
        verbose_name_plural = 'Связь рецепт-тег'


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество в юнитах'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique ingredient in recipe'
            )
        ]
        verbose_name = 'Ингредиенты в рецепте'
        verbose_name_plural = 'Связь рецепт-ингредиент'


class FavoriteRecipe(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorite_recipes'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='users_favorite_recipes'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_favorite_recipe'
            ),
        ]
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранное'


class ShoppingCart(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_cart_recipes'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_cart_users'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_shopping_cart_recipe'
            ),
        ]
        verbose_name = 'Рецепт в корзине'
        verbose_name_plural = 'Корзина'
