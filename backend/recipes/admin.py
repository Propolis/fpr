from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import (
    FavoriteRecipe,
    Ingredient,
    Recipe,
    RecipeIngredient,
    RecipeTag,
    ShoppingCart,
    Tag
)


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1


class RecipeTagInline(admin.TabularInline):
    model = RecipeTag
    extra = 1


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    list_filter = ('name',)
    search_fields = ('name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'count_favorites')
    list_filter = ('name', 'author__email', 'tags')
    inlines = [
        RecipeIngredientInline,
        RecipeTagInline
    ]

    @admin.display(description='В избранном')
    def count_favorites(self, obj):
        return FavoriteRecipe.objects.filter(recipe=obj).count()


@admin.register(FavoriteRecipe)
class FavoriteRecipeAdmin(admin.ModelAdmin):
    pass


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    pass


@admin.register(RecipeIngredient)
class RecipeIngredientCartAdmin(admin.ModelAdmin):
    pass


@admin.register(RecipeTag)
class RecipeTagAdmin(admin.ModelAdmin):
    pass
